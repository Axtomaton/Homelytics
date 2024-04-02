import os

for files in os.listdir("charts/"):
    if files.endswith(".png"):
        os.remove("charts/"+files)
