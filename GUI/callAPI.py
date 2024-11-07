import requests


def save_Key(private_key, key_aes):
    try:
        response = requests.post(
            "http://localhost:3006/api/user/save-Key",
            json={"privateKey_rsa": private_key, "key_aes": key_aes},
        )
        return response.json()
    except Exception as e:
        return None

def get_Key():
    try:
        response = requests.get("http://localhost:3006/api/user/get-Key")
        return response.json()
    except Exception as e:
        return None