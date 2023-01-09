

def load_txt(filepath):
    with open(filepath, "r", encoding="utf8") as f:
        return f.read().splitlines()