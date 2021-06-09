import configparser


def read_db_params():
    # reading the env file
    config = configparser.ConfigParser()
    config.read('config/local.env')
    return config
