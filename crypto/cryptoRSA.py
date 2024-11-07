import random
import math
import os


# Optimized prime checking function
def is_prime(number):
    if number <= 1:
        return False
    if number == 2 or number == 3:
        return True
    if number % 2 == 0 or number % 3 == 0:
        return False
    for i in range(5, int(math.sqrt(number)) + 1, 6):
        if number % i == 0 or number % (i + 2) == 0:
            return False
    return True


# Prime generator function (use larger primes for real-world usage)
def generate_prime(min_value, max_value):
    while True:
        prime = random.randint(min_value, max_value)
        if is_prime(prime):
            return prime


# Modular inverse using pow() from standard library
def mod_inverse(e, phi):
    return pow(e, -1, phi)


# RSA Key Generation
def generate_keys():
    p = generate_prime(1000, 5000)
    q = generate_prime(1000, 5000)
    while p == q:
        q = generate_prime(1000, 5000)

    n = p * q
    phi_n = (p - 1) * (q - 1)

    # Fixed public exponent
    e = 65537
    if math.gcd(e, phi_n) != 1:
        raise ValueError("Public exponent e is not coprime with φ(n)")

    d = mod_inverse(e, phi_n)
    return (e, n), (d, n)  # Return public and private keys


# RSA Encryption
def encrypt(message, public_key):
    e, n = public_key
    # Convert message to ASCII
    message_encoded = [ord(ch) for ch in message]
    # Encrypt each character using (m ^ e) mod n
    ciphertext = [pow(ch, e, n) for ch in message_encoded]
    return ciphertext


# RSA Decryption
def decryptRSA(ciphertext, private_key):
    d, n = private_key
    # Decrypt each character using (c ^ d) mod n
    message_decoded = [pow(ch, d, n) for ch in ciphertext]
    # Convert back to string
    message = "".join(chr(ch) for ch in message_decoded)
    return message


# Save and load ciphertext to/from file
def save_ciphertext_to_file(ciphertext):
    ciphertext_str = ":".join(map(str, ciphertext))
    with open("crypto/key.txt", "w") as file:
        file.write(ciphertext_str)


def load_ciphertext_from_file():
    with open("crypto/key.txt", "r") as file:
        ciphertext_str = file.read()
    ciphertext = list(map(int, ciphertext_str.split(":")))
    return ciphertext


# Save and load private key to/from file
def save_private_key_to_file(private_key):
    with open("crypto/private.txt", "w") as file:
        file.write(f"{private_key[0]}\n")  # Write 'd'
        file.write(f"{private_key[1]}\n")  # Write 'n'


def load_private_key_from_file():
    with open("crypto/private.txt", "r") as file:
        d = int(file.readline().strip())  # Read 'd'
        n = int(file.readline().strip())  # Read 'n'
    return (d, n)


# Function to generate RSA keys and encrypt the key_hex
def generate_and_encrypt_key():
    # Generate RSA keys
    public_key, private_key = generate_keys()

    # Save private key
    # save_private_key_to_file(private_key)

    # Key to be encrypted
    key = os.urandom(16)
    key_hex = key.hex() #chuyển sang hex
    # print(f"Key Hex before encryption: {key_hex}")

    # Encrypt the key_hex
    encrypted_key = encrypt(key_hex, public_key)

    # Save encrypted key to file
    # print(encrypted_key)
    # save_ciphertext_to_file(encrypted_key)
    # print("Key has been encrypted and saved to file.")
    return private_key, encrypted_key


# Function to decrypt the key from file using RSA
def decrypt_key_from_file():
    # Load private key
    private_key = load_private_key_from_file()

    # Load encrypted key from file
    encrypted_key = load_ciphertext_from_file()

    # Decrypt the key
    decrypted_key = decrypt(encrypted_key, private_key)

    print(f"Decrypted Key Hex: {decrypted_key}")


# Main Execution
if __name__ == "__main__":
    # Check if key already exists, otherwise generate a new one
    if os.stat("crypto/key.txt").st_size == 0:
        generate_and_encrypt_key()  # Generate and encrypt key
    else:
        decrypt_key_from_file()  # Decrypt the key
