# python mysql

from configparser import RawConfigParser, Error
import os


def readConfig():
    """
    Return 
    ------
    `(variable) config: ConfigParser`
    """

    # Deal with path issue
    folder = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(folder, 'localConfig.env')

    config = RawConfigParser()
    res = config.read(config_file)

    return config


if __name__ == "__main__":
    config = readConfig()
    print(config)

    print(config.get('DB', 'host'))