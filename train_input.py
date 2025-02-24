
user_inpt = []
with open("examples.txt", "r") as f:
   lines = f.readlines()
   for line in lines:
      if line != "\n":
        user_inpt.append(line)

print(user_inpt[1]) 