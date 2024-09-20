import configparser

def get_current_version_from_cfg(file_path="setup.cfg"):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config["bumpversion"]["current_version"]


if __name__ == '__main__':
    version = get_current_version_from_cfg()
    print(f"Current version: {version}")
