import os

root = "app"

for dirpath, dirnames, filenames in os.walk(root):
    for name in filenames:
        if not name.endswith(".py"):
            continue
        path = os.path.join(dirpath, name)
        with open(path, "rb") as f:
            data = f.read()
        if b"\x00" in data:
            print("NULL BYTES:", path)
