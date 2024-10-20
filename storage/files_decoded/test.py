import RSA
file = open("key.txt")
key = file.read()
print(key)

public_key, private_key = RSA.generate_keys()

cipherText = RSA.encrypt(key, public_key)
print(f"cipherText: {cipherText}")

decryptMessage = RSA.decrypt(cipherText , private_key)
print("Decrypted Message:", decryptMessage)

file.close()