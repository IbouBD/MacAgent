import os
import subprocess
import time
from datetime import datetime, timedelta
from pynput.keyboard import Key, Controller

kb = Controller()

CRITICAL_SERVICES = [
    'Spotlight', 'loginwindow', 'SystemUIServer', 'Dock', 'ControlCenter',
    'NotificationCenter', 'CoreServicesUIAgent', 'WindowManager', 'IOUIAgent',
    'UserNotificationCenter', 'System Events', 'chronod', 'SoftwareUpdateNotificationManager',
    'talagent', 'CoreLocationAgent', 'AppSSODaemon', 'QuickLookUIService',
    'ThemeWidgetControlViewService', 'com.apple.WebKit.WebContent',
    'com.apple.WebKit.Networking', 'AirPlayUIAgent', 'TextInputMenuAgent',
]

DELAY_MINUTES = 2
time_threshold = datetime.now() - timedelta(minutes=DELAY_MINUTES)

def log_error(context, e):
    print(f"[ERREUR] {context}: {type(e).__name__} - {e}")

def get_open_apps():
    try:
        result = subprocess.run(
            ["osascript", "-e", 'tell application "System Events" to get name of every process'],
            capture_output=True, text=True, check=True
        )
        return result.stdout.strip().split(", ")
    except subprocess.CalledProcessError as e:
        log_error("Échec récupération des applications ouvertes", e)
        return []

def close_apps():
    open_apps = get_open_apps()
    for app in open_apps:
        if app not in CRITICAL_SERVICES:
            try:
                subprocess.run(["osascript", "-e", f'tell application "{app}" to quit'], check=True)
                print(f"Fermé : {app}")
            except subprocess.CalledProcessError as e:
                log_error(f"Fermeture échouée pour {app}", e)
            except Exception as e:
                log_error(f"Erreur inattendue lors de la fermeture de {app}", e)

def delete_recent_files():
    home_dirs = ["~/Desktop", "~/Documents", "~/Downloads"]
    for directory in home_dirs:
        expanded_dir = os.path.expanduser(directory)
        if not os.path.exists(expanded_dir):
            continue
        for root, _, files in os.walk(expanded_dir):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    creation_time = datetime.fromtimestamp(os.path.getctime(file_path))
                    if creation_time > time_threshold:
                        os.remove(file_path)
                        print(f"Supprimé : {file_path}")
                except FileNotFoundError:
                    # Le fichier a peut-être déjà été supprimé
                    continue
                except PermissionError as e:
                    log_error(f"Permission refusée pour supprimer {file_path}", e)
                except Exception as e:
                    log_error(f"Erreur suppression {file_path}", e)

def restore_deleted_files():
    trash_path = os.path.expanduser("~/.Trash")
    if not os.path.exists(trash_path):
        return
    for file in os.listdir(trash_path):
        file_path = os.path.join(trash_path, file)
        try:
            deletion_time = datetime.fromtimestamp(os.path.getctime(file_path))
            if deletion_time > time_threshold:
                restored_path = os.path.expanduser(f"~/Desktop/{file}")
                os.rename(file_path, restored_path)
                print(f"Restauré : {restored_path}")
        except FileNotFoundError:
            continue
        except PermissionError as e:
            log_error(f"Permission refusée pour restaurer {file_path}", e)
        except Exception as e:
            log_error(f"Erreur restauration {file_path}", e)

def reset():
    time.sleep(0.5)
    kb.press(Key.esc)
    time.sleep(0.5)
    kb.press(Key.esc)

    print("Fermeture des applications...")
    close_apps()

    print("Suppression des fichiers récents...")
    delete_recent_files()

    print("Restauration des fichiers supprimés...")
    restore_deleted_files()

    print("Opération terminée.")