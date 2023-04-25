from utils.loader import client, configData
from funcs.derivadas import getdotenv

if __name__ == "__main__":
    client.run(getdotenv("token"))
