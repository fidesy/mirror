import yaml


def load_config(filepath: str) -> any:
    with open(filepath, "r", encoding="utf8") as f:
        try:
            return yaml.safe_load(f)
        except yaml.YAMLError as err:
            print(err)


config = load_config("./configs/config.yaml")