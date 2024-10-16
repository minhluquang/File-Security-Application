import random
import math

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
def decrypt(ciphertext, private_key):
    d, n = private_key
    # Decrypt each character using (c ^ d) mod n
    message_decoded = [pow(ch, d, n) for ch in ciphertext]
    # Convert back to string
    message = ''.join(chr(ch) for ch in message_decoded)
    return message

