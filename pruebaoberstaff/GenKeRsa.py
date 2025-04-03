import json
from Crypto.PublicKey import RSA





def main():
    key = RSA.generate(2048)
    # private_key = key.export_key()
    secret_code = "-+eve7*cnx)earc7*w4t%rgnj7e9&+pbn)46m2vh73xj&hoam1!"
    private_key = key.export_key()
    with open("apps/system/private_back.pem", "wb") as f:
        f.write(private_key)


    public_key = key.publickey().export_key()

    with open("apps/system/public_back.pem", "wb") as f:
        f.write(public_key)
