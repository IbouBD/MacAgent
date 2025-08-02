import math
import torch
import torch.nn as nn
import torch.nn.functional as F
from sentence_transformers import SentenceTransformer


actor_path = 'Models/actor4.pth'
critic_path = 'Models/critic3.pth'
vision_path = 'Models/mousse_net.pth'
device = torch.device('mps' if torch.mps.is_available() else 'cpu')
encoder = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
IMG_SIZE = 448


class ResidualFFN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_blocks=2):
        super(ResidualFFN, self).__init__()
        
        # Projection initiale
        self.input_proj = nn.Linear(input_dim, hidden_dim)
        
        # Blocs résiduels
        self.res_blocks = nn.ModuleList([
            ResidualBlock(hidden_dim) for _ in range(num_blocks)
        ])
        
        # Projection finale
        self.output_proj = nn.Linear(hidden_dim, output_dim)
        
    def forward(self, x):
        x = self.input_proj(x)
        
        # Appliquer les blocs résiduels
        for block in self.res_blocks:
            x = block(x)
            
        return self.output_proj(x)
        
class ResidualBlock(nn.Module):
    def __init__(self, dim, dropout=0.3):
        super(ResidualBlock, self).__init__()
        self.layers = nn.Sequential(
            nn.Linear(dim, dim * 4),
            nn.GELU(),
            nn.Dropout(dropout),
            nn.Linear(dim * 4, dim)
        )
        self.norm = nn.LayerNorm(dim)
        
    def forward(self, x):
        return self.norm(x + self.layers(x))
    
class PositionalEncoding(nn.Module):
    def __init__(self, dim, max_len=512):
        super().__init__()
        pe = torch.zeros(max_len, dim)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, dim, 2).float() * (-math.log(10000.0) / dim))
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(1)  # (max_len, 1, dim)
        self.register_buffer('pe', pe)

    def forward(self, x):
        # x shape: (seq_len, batch_size, dim)
        x = x + self.pe[:x.size(0)]
        return x

class Actor(nn.Module):
    def __init__(self, dim, hidden, vocab_size, max_len=128):
        super().__init__()
        self.encoder = encoder # pretrained SentenceTransformer
        self.rffn = ResidualFFN(384, hidden, dim)
        self.embedding = nn.Embedding(vocab_size, dim)
        self.pos_encoding = PositionalEncoding(dim, max_len=max_len)
        self.decoder_layer = nn.TransformerDecoderLayer(d_model=dim, nhead=16, dim_feedforward=hidden, dropout=0.3)
        self.transformer_decoder = nn.TransformerDecoder(self.decoder_layer, num_layers=2) # passage de 6 à 2 layers
        self.final_projection = nn.Linear(dim, vocab_size)
        self.max_len = max_len
        self.dim = dim
        self.vocab_size = vocab_size
        self.device = device
        self.load_state_dict(torch.load(actor_path))

    def forward(self, x_text: list[str], tgt: torch.Tensor):
        """
        x_text: liste d'instructions (batch_size,)
        tgt: séquence cible (batch_size, seq_len), excluant BOS
        Retourne : logits (batch_size, seq_len, vocab_size)
        """
        with torch.no_grad():
            x = self.encoder.encode(x_text, convert_to_tensor=True)

        # projection
        x = self.rffn(x)  # (batch_size, dim)
        x = x.unsqueeze(0)  # (1, batch_size, dim)


        # embedding + positional encoding
        tgt = self.embedding(tgt)  # (batch_size, seq_len, dim)
        tgt = tgt.unsqueeze(0)
        tgt = tgt.permute(1, 0, 2)  # (seq_len, batch_size, dim)
        tgt = self.pos_encoding(tgt)
        
        # masquage
        seq_len = tgt.size(0)
        tgt_mask = nn.Transformer.generate_square_subsequent_mask(seq_len).to(tgt.device)

        # decoder
        z = self.transformer_decoder(tgt, x, tgt_mask=tgt_mask)  # (seq_len, batch_size, dim)
        z = self.final_projection(z)  # (seq_len, batch_size, vocab_size)
        z = z.permute(1, 0, 2)  # (batch_size, seq_len, vocab_size)
        return z
    
    
    @torch.no_grad()
    def generate(self, x_text:list[str], max_len=32, start_token_id=1, end_token_id=2):
        """
        x_text : liste de string
        Retourne une liste de listes contenant les ID générés
        """
        # Encode input texts
        with torch.no_grad():
            x = self.encoder.encode(x_text, convert_to_tensor=True)
        x = self.rffn(x)  # (batch_size, dim)
        memory = x.unsqueeze(0)  # (1, batch_size, dim)


        batch_size = x.size(0)
        device = x.device

        # Initialiser avec <BOS>
        generated = torch.full((batch_size, 1), start_token_id, dtype=torch.long, device=device)

        for _ in range(max_len):
            # Embed + position
            tgt_embed = self.embedding(generated)  # (batch_size, seq_len, dim)
            tgt_embed = tgt_embed.permute(1, 0, 2)  # (seq_len, batch_size, dim)
            tgt_embed = self.pos_encoding(tgt_embed)

            # masque causal
            seq_len = generated.size(1)
            tgt_mask = nn.Transformer.generate_square_subsequent_mask(seq_len).to(device)

            # decode
            output = self.transformer_decoder(tgt_embed, memory, tgt_mask=tgt_mask)
            logits = self.final_projection(output)  # (seq_len, batch_size, vocab_size)
            next_token_logits = logits[-1, :, :]  # dernier pas de temps (batch_size, vocab_size)

            next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)  # (batch_size, 1)

            generated = torch.cat([generated, next_token], dim=1)

            if (next_token == end_token_id).all():
                break

        return generated  # (batch_size, seq_len_generated)
    
#dim, hidden, vocab_size = 512, 512, 1785
#model = Actor(dim, hidden, vocab_size).to(device)
#model.load_state_dict(torch.load(model_path))

#def generate_action(x:list[str]):
#    y = model.generate(x, max_len=32)
#    return y

class Critic(nn.Module):
    def __init__(self):
        super(Critic, self).__init__()
        self.encoder = encoder  # pretrained SentenceTransformer
        self.linear1 = nn.Linear(384, 256)
        self.linear2 = nn.Linear(256, 512)
        self.linear3 = nn.Linear(512, 1)
        self.load_state_dict(torch.load(critic_path))

    def forward(self, state):
        
        x = self.encoder.encode(state, convert_to_tensor=True)
        output = F.relu(self.linear1(x))
        output = F.relu(self.linear2(output))
        value = self.linear3(output)
        return value

class MouseNet(nn.Module):
    def __init__(self, in_channels, num_classes=2, input_size=IMG_SIZE):
        super(MouseNet, self).__init__()
        self.input_size = input_size
        
        # Couches convolutionnelles
        self.conv1 = nn.Conv2d(in_channels=in_channels, out_channels=8, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2)
        self.conv2 = nn.Conv2d(in_channels=8, out_channels=16, kernel_size=3, padding=1)
        self.conv3 = nn.Conv2d(in_channels=16, out_channels=32, kernel_size=3, padding=1)
        
        # Calcul de la taille après convolutions
        # input_size -> /2 -> /2 = input_size // 4
        self.feature_size = self._get_conv_output_size(in_channels, input_size)
        
        # Couches fully connected
        self.fc1 = nn.Linear(self.feature_size, 64)
        self.fc2 = nn.Linear(64, 128)
        self.out = nn.Linear(128, num_classes)
        self.load_state_dict(torch.load(vision_path))
        
    def _get_conv_output_size(self, in_channels, input_size):
        """Calcule la taille de sortie des couches convolutionnelles"""
        x = torch.randn(1, in_channels, input_size, input_size)
        x = self.pool(F.relu(self.conv1(x)))
        x = self.pool(F.relu(self.conv2(x)))
        x = F.relu(self.conv3(x))
        return x.view(1, -1).size(1)

    def forward(self, x, features_only=False):
        # x shape attendue: (batch_size, in_channels, height, width)
        batch_size = x.size(0)
        
        # Couches convolutionnelles
        x = F.relu(self.conv1(x))  # (batch, 8, H, W)
        x = self.pool(x)           # (batch, 8, H/2, W/2)
        x = F.relu(self.conv2(x))  # (batch, 16, H/2, W/2)
        x = self.pool(x)           # (batch, 16, H/4, W/4)
        x = F.relu(self.conv3(x))  # (batch, 32, H/4, W/4)
        
        # Aplatissement pour les couches fully connected
        x = x.view(batch_size, -1)  # (batch, 32 * H/4 * W/4)
        
        # Couches fully connected
        x = F.relu(self.fc1(x))    # (batch, 64)
        x = F.relu(self.fc2(x))    # (batch, 128)
        if features_only==True:
            return x
        else:
            x = self.out(x)            # (batch, num_classes)
            return torch.sigmoid(x).to(torch.float32)


class VisionActor(nn.Module):
    def __init__(self, in_channels, dim, hidden, vocab_size):
        super(VisionActor, self).__init__()
        self.in_channels = in_channels
        self.encoder = encoder # pretrained SentenceTransformer
        self.dim = dim
        self.hidden = hidden
        self.vocab_size = vocab_size
        self.actor = Actor(self.dim, self.hidden, self.vocab_size)
        self.mousenet = MouseNet(self.in_channels)
        self.vision_rffn = ResidualFFN(self.mousenet.out.in_features, hidden, dim)
        self.rffn = self.actor.rffn
        self.fusion = nn.MultiheadAttention(dim, num_heads=8)
        self.pointer_head = nn.Sequential(
            nn.Linear(dim, 128),
            nn.ReLU(),
            self.mousenet.out,  # x, y normalisés
            nn.Sigmoid()       # borné entre [0, 1]
        )

    def forward(self, x, tgt, screenshots=None):
        """
        x: encoder output (batch_size, dim),

        tgt: tensor of shape (batch_size, seq_len),

        screenshot: image converti en niveau de gris,
        
        Retourne une liste de listes contenant les ID générés ainsi que des coordonnées (x, y)
        """
        if screenshots is not None:
            # encoder le text
            txt_encoded = self.actor.rffn(x) # shape: (batch_size, dim)
            txt_encoded = txt_encoded.unsqueeze(0) # shape: (1, batch_size, dim)
            
            # encoder l'image
            vision_features = self.mousenet.forward(screenshots, features_only=True) # shape: (batch_size, 128)
            vision_encoded = self.vision_rffn(vision_features) # shape: (batch_size, dim)
            vision_encoded = vision_encoded.unsqueeze(0) # shape: (1, batch_size, dim)
            fused, _ = self.fusion(txt_encoded, vision_encoded, vision_encoded) # shape (1, batch_size, dim)

            # traiter target sequence
            tgt = tgt.to(device)
            tgt = self.actor.embedding(tgt)  # (batch_size, seq_len, dim)
            tgt = tgt.permute(1, 0, 2)  # (seq_len, batch_size, dim)
            tgt = self.actor.pos_encoding(tgt)  #  positional encoding

            # masque auto-régressif pour le décodeur
            seq_len = tgt.size(0)
            tgt_mask = nn.Transformer.generate_square_subsequent_mask(seq_len).to(tgt.device)

            # passage au decoder
            z = self.actor.transformer_decoder(tgt, fused, tgt_mask=tgt_mask)  # (seq_len, batch_size, dim)
            z = self.actor.final_projection(z)  # (seq_len, batch_size, vocab_size)
            z = z.permute(1, 0, 2)  # (batch_size, seq_len, vocab_size)
            pointer_out = self.pointer_head(vision_encoded.squeeze(0))  # (batch_size, 2)

            return z, pointer_out
        else:
            return self.actor.forward_training(x, tgt), screenshots


    @torch.no_grad()
    def generate(self, x_text:list[str], screenshots=None, max_len=32, start_token_id=1, end_token_id=2):
        """
        x_text : liste de string
        Retourne une liste de listes contenant les ID générés
        """
        if screenshots is not None:
            # Encode input texts
            with torch.no_grad():
                txt_features = self.encoder.encode(x_text, convert_to_tensor=True) # shape: (batch_size, 384)
            txt_encoded = self.actor.rffn(txt_features) # shape: (batch_size, dim)
            txt_encoded = txt_encoded.unsqueeze(0) # shape: (1, batch_size, dim)

            # encoder l'image
            vision_features = self.mousenet.forward(screenshots, features_only=True) # shape: (batch_size, 128)
            vision_encoded = self.vision_rffn(vision_features) # shape: (batch_size, dim)
            vision_encoded = vision_encoded.unsqueeze(0) # shape: (1, batch_size, dim)
            x, _ = self.fusion(txt_encoded, vision_encoded, vision_encoded) # shape (1, batch_size, dim)
            pointer_out = self.pointer_head(vision_encoded.squeeze(0))  # (batch_size, 2)

            batch_size = x.size(0)
            device = x.device

            # Initialiser avec <BOS>
            generated = torch.full((batch_size, 1), start_token_id, dtype=torch.long, device=device)

            for _ in range(max_len):
                # Embed + position
                tgt_embed = self.actor.embedding(generated)  # (batch_size, seq_len, dim)
                tgt_embed = tgt_embed.permute(1, 0, 2)  # (seq_len, batch_size, dim)
                tgt_embed = self.actor.pos_encoding(tgt_embed)

                # masque causal
                seq_len = generated.size(1)
                tgt_mask = nn.Transformer.generate_square_subsequent_mask(seq_len).to(device)

                # decode
                output = self.actor.transformer_decoder(tgt_embed, x, tgt_mask=tgt_mask)
                logits = self.actor.final_projection(output)  # (seq_len, batch_size, vocab_size)
                next_token_logits = logits[-1, :, :]  # dernier pas de temps (batch_size, vocab_size)

                next_token = torch.argmax(next_token_logits, dim=-1, keepdim=True)  # (batch_size, 1)

                generated = torch.cat([generated, next_token], dim=1)

                if (next_token == end_token_id).all():
                    break

            return generated, pointer_out  # ((batch_size, seq_len_generated), (batch_size, 2))
        else:
            return self.actor.generate(x_text), screenshots