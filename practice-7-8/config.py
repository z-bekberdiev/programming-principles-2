import sys
from pathlib import Path
from configparser import ConfigParser

PATH = Path(__file__).parent

def load_config(path: str = f"{PATH}/credentials.ini", section: str = "postgresql") -> dict[str, str]:
    parser = ConfigParser()
    parser.read(path)
    config = {}
    if parser.has_section(section):
        parameters = parser.items(section)
        for parameter in parameters:
            config[parameter[0]] = parameter[1]
        return config
    else:
        print(f"\033[91m[section \"{section}\" not found in the \"{path}\" file]\033[0m\n")
        sys.exit(1)
