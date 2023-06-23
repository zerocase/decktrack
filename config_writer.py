from configparser import ConfigParser
import os
config = ConfigParser()

def create_default_config():
    config["DEFAULT"] = {
        "Music Library": "C:\\Users\\<NAME>\\Music\\",
        "Always Analyse": False,
        "Spotify Client ID": "ExampleID",
        "Spotify Client Secret": "ExampleSecret"
    }

    with open("dtconfig.ini", "w") as configfile:
        config.write(configfile)

    print("Config file created.")


def modify_config(option, value):
    config.set("DEFAULT", str(option), str(value))

    with open("dtconfig.ini", "w") as configfile:
        config.write(configfile)

