import configparser


config = configparser.ConfigParser()
config.read("./config.ini")
print(config["DEFAULT"]["APP_VERSION"])
