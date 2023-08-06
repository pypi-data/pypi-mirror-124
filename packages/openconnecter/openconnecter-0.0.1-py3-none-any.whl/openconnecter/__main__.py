import json
from json.decoder import JSONDecodeError
import os

from pyotp import TOTP
import pyotp

CONFIG_PATH = os.environ.get("OPENCONNECTOR_CONFIG", "~/.config/.openconnector.json")
CONFIG_PATH = os.path.expanduser(CONFIG_PATH)


def initiate():
    config = {}

    server = input("Please enter openconnect server ip: ")
    servercert = input("Please enter your servercert: ")
    username = input("Please enter your username: ")
    password = input("Please enter your password: ")
    seed = input("Please Enter your totp seed (leave empty if 2fa is not needed): ")

    config = {
        "server": server,
        "servercert": servercert,
        "username": username,
        "password": password,
        "seed": seed,
    }

    with open(CONFIG_PATH, "w") as config_file:
        json.dump(config, config_file)

    return config


def read_config():
    try:
        with open(CONFIG_PATH) as config_file:
            config = json.load(config_file)
    except (FileNotFoundError, JSONDecodeError):
        config = initiate()

    return config


def get_otp(seed):
    totp = pyotp.TOTP(seed)
    return totp.now()


def main():
    config = read_config()

    server = config["server"]
    servercert = config["servercert"]
    username = config["username"]
    password = config["password"]
    otp = get_otp(config["seed"])

    command = f"echo '{password}\n{otp}' | sudo openconnect {server} --servercert={servercert} --user={username} --passwd-on-stdin"

    os.system(command)
