import os
import sys
import struct
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
max_workers=os.cpu_count()
from encryptAES import encrypt as aes_encrypt
from decryptAES import decrypt as aes_decrypt
from encryptAES import * 
from decryptAES import *
from cryptoRSA import *
def check_and_generate_key_if_empty():
    key_file_path = "crypto/key.txt"
    # Kiểm tra nếu file trống hoặc không tồn tại
    if not os.path.exists(key_file_path) or os.stat(key_file_path).st_size == 0:
        print("Key file is empty or doesn't exist. Generating new key.")
        generate_and_encrypt_key()
    else:
        print("Key file exists and is valid.")

# Tạo khoá 16 byte (128 bit)
# key = os.urandom(16)
# key_hex = key.hex() #chuyển sang hex

# Lưu khóa vào file Notepad
# with open("key.txt", "w") as file:
#   file.write(key_hex)

# key_hex = "32df43dc72149ac2e06bacdee6264b9f"

# Chia chuỗi thành các phần mỗi phần 8 ký tự
# w = []
# for i in range(0, len(key_hex), 8):
#   wi = int("0x" + key_hex[i:i+8], 16)
#   w.append(wi)
  
def read_text_file(file_path):
  with open(file_path, "rb") as file:
    return file.read()  # Đọc toàn bộ nội dung file

def binary_to_states(byte_data):
    # Bước 1: In ra độ dài của byte_data để tham khảo
    # print(f"Độ dài ban đầu của byte_data: {len(byte_data)} bytes")
    
    # Bước 2: Đệm thêm bytes nếu độ dài byte_data không đủ 16
    if len(byte_data) % 16 != 0:
        padding_length = 16 - (len(byte_data) % 16)  # Số byte đệm cần thêm
        byte_data += bytes([0] * padding_length)  # Đệm thêm các byte `0x00`
    
    # Bước 3: Chia byte_data thành các block 16 bytes
    blocks = [byte_data[i:i+16] for i in range(0, len(byte_data), 16)]

    # Bước 4: Chuyển từng block thành state (4 phần tử, mỗi phần tử là 4 bytes)
    states = []
    for block in blocks:
        state = []
        for i in range(0, 16, 4):  # Mỗi lần lấy 4 bytes trong block
            # Chuyển 4 byte này thành một số nguyên 32-bit
            num = int.from_bytes(block[i:i+4], byteorder='big')
            state.append(num)
        states.append(state)

    return states


def states_to_binary(state):
     # Bước 1: Khởi tạo chuỗi byte rỗng
    byte_data = b''
    # Bước 2: Chuyển đổi từng state thành chuỗi byte và ghép lại
    for num in state:
        # Chuyển từng số nguyên 32-bit trong state thành 4 bytes
        byte_data += num.to_bytes(4, byteorder='big')

    # Bước 3: Loại bỏ các byte đệm nếu có (ví dụ: 0x00 ở cuối)
    # byte_data = byte_data.rstrip(b'\x00')

    return byte_data
def states_to_binary1(states):
     # Bước 1: Khởi tạo chuỗi byte rỗng
    byte_data = b''
    # Bước 2: Chuyển đổi từng state thành chuỗi byte và ghép lại
    for state in states:
        for num in state:
        # Chuyển từng số nguyên 32-bit trong state thành 4 bytes
            byte_data += num.to_bytes(4, byteorder='big')

    # Bước 3: Loại bỏ các byte đệm nếu có (ví dụ: 0x00 ở cuối)
    byte_data = byte_data.rstrip(b'\x00')

    return byte_data

# def encryptFile(file_path):
#   contentFile = read_text_file(file_path)
#   states = binary_to_states(contentFile)
  
#   # Mã hóa AES
#   encrypted_states = []
#   for state in states:
#     encrypted_content = encrypt(state, w)
#     encrypted_states.append(encrypted_content)

#   # Chuyển đổi các encrypted_states thành dữ liệu nhị phân
#   encrypted_binary = states_to_binary(encrypted_states)

#   # Đường dẫn lưu file mã hoá
#   output_directory = "storage/files_encoded/"

#   # Ghi dữ liệu nhị phân vào file
#   # with open(output_directory + file_path + '.enc', 'wb') as file:
#   #   file.write(encrypted_binary)
#   with open(file_path, 'wb') as file:
#     file.write(encrypted_binary)
import concurrent.futures
def encryptFile(file_path, encrypted_key, private_key):
    # Gọi kiểm tra khóa trước khi mã hóa (chỉ khi mã hóa cần tạo khóa)
    # check_and_generate_key_if_empty()

    
    contentFile = read_text_file(file_path)
    # print("contentFile ", contentFile)
    states = binary_to_states(contentFile)

    # Load khóa AES từ file (đã mã hóa bằng RSA) và giải mã
    # encrypted_key = load_ciphertext_from_file()  # Load khóa AES mã hóa
    # private_key = load_private_key_from_file()   # Load khóa riêng RSA
    key_hex = decryptRSA(encrypted_key, private_key)  # Giải mã khóa AES bằng RSA
    # Chuyển key_hex thành mảng w
    w = []
    for i in range(0, len(key_hex), 8):
        wi = int("0x" + key_hex[i:i+8], 16)
        w.append(wi)
    
        # Mã hóa AES từng block
    encrypted_states = []
    # print(max_workers)
    with concurrent.futures.ThreadPoolExecutor(max_workers= max_workers) as executor:
        futures = [executor.submit(generateStates,state,w) for state in states]
        encrypted_states = [future.result() for future in futures]
    # Chuyển đổi các encrypted_states thành dữ liệu nhị phân
    with concurrent.futures.ThreadPoolExecutor(max_workers= max_workers) as executor:
        futures = [executor.submit(states_to_binary,state) for state in encrypted_states]
        encrypted_binary = b''.join([future.result() for future in futures])
    # encrypted_binary = states_to_binary1(encrypted_states)
    # print(f"encrypted_binary: {encrypted_binary}")

    # Ghi dữ liệu nhị phân đã mã hóa vào file
    with open(file_path, 'wb') as file:
        file.write(encrypted_binary)
    # print("END")

def generateStates(state,w):
    return aes_encrypt(state,w)
   
# def encryptFile(file_path, encrypted_key, private_key):
#     # Gọi kiểm tra khóa trước khi mã hóa (chỉ khi mã hóa cần tạo khóa)
#     # check_and_generate_key_if_empty()

    
#     contentFile = read_text_file(file_path)
#     # print("contentFile ", contentFile)
#     states = binary_to_states(contentFile)

#     # Load khóa AES từ file (đã mã hóa bằng RSA) và giải mã
#     # encrypted_key = load_ciphertext_from_file()  # Load khóa AES mã hóa
#     # private_key = load_private_key_from_file()   # Load khóa riêng RSA
#     key_hex = decryptRSA(encrypted_key, private_key)  # Giải mã khóa AES bằng RSA

#     # Chuyển key_hex thành mảng w
#     w = []
#     for i in range(0, len(key_hex), 8):
#         wi = int("0x" + key_hex[i:i+8], 16)
#         w.append(wi)
#     print(f"w : {w}")
#     print(states)
#     # Mã hóa AES từng block
#     encrypted_states = []
#     for state in states:
#         encrypted_content = aes_encrypt(state, w)
#         encrypted_states.append(encrypted_content)

#     print(f"encrypted_states : {encrypted_states}")
#     # Chuyển đổi các encrypted_states thành dữ liệu nhị phân
#     encrypted_binary = states_to_binary(encrypted_states)

#     # Ghi dữ liệu nhị phân đã mã hóa vào file
#     with open(file_path, 'wb') as file:
#         file.write(encrypted_binary)

# def decryptFile(file_path):
#   # Đọc dữ liệu nhị phân từ file
#   with open(file_path, 'rb') as file:
#     encrypted_binary = file.read()

#   # Chuyển đổi dữ liệu nhị phân thành các state
#   encrypted_states = binary_to_states(encrypted_binary)

#   # Đường dẫn lưu file sau khi mã hoá
#   output_directory = "storage/files_decoded/"

#   #Kiểm tra và tạo thư mục nếu không tồn tại
#   os.makedirs(output_directory, exist_ok=True)

#   # Giải mã AES
#   decrypted_states = []
#   for i, encryptState in enumerate(encrypted_states):
#     decrypted_content = decrypt(encryptState, w)
#     decrypted_states.append(decrypted_content)
 
#   # Chuyển đổi state sang binary
#   binary_data = states_to_binary(decrypted_states)
  
#   # Ghi bản rõ vào file
#   # file_path = file_path[:-4] #Loại bỏ .enc
#   # base_name, ext = os.path.splitext(file_path)
#   # base_name = base_name.replace("GUI/files_encoded/", "")
  
#   # Đường dẫn lưu file
#   output_directory = 'storage/files_decoded/'
  
#   # Kiểm tra và tạo thư mục nếu không tồn tại
#   os.makedirs(output_directory, exist_ok=True)

#   # with open(f'{output_directory}{base_name}_decrypted{ext}', 'wb') as file:
#   #   file.write(binary_data)
#   with open(file_path, 'wb') as file:
#     file.write(binary_data)
def Generate_AES_DECRYPTSTATES(encryptState, w):
    return aes_decrypt(encryptState, w)

# Hàm giải mã file
def decryptFile(file_path, encrypted_key, private_key):
    with open(file_path, 'rb') as file:
        encrypted_binary = file.read()

    encrypted_states = binary_to_states(encrypted_binary)

    # Load khóa AES từ file (đã mã hóa bằng RSA) và giải mã
    # encrypted_key = load_ciphertext_from_file()  # Load khóa AES mã hóa
    # private_key = load_private_key_from_file()   # Load khóa riêng RSA
    key_hex = decryptRSA(encrypted_key, private_key)  # Giải mã khóa AES bằng RSA

    # Chuyển key_hex thành mảng w
    w = []
    for i in range(0, len(key_hex), 8):
        wi = int("0x" + key_hex[i:i+8], 16)
        w.append(wi)

    # Giải mã AES từng block
    decrypted_states = []
    with concurrent.futures.ThreadPoolExecutor(max_workers= max_workers) as executor:
        futures = [executor.submit(Generate_AES_DECRYPTSTATES,encryptState,w) for encryptState in encrypted_states]
        decrypted_states = [future.result() for future in futures]
    # for encryptState in encrypted_states:
    #     decrypted_content = aes_decrypt(encryptState, w)
    #     decrypted_states.append(decrypted_content)

    # Chuyển state đã giải mã sang binary
    # binary_data = states_to_binary1(decrypted_states)
    with concurrent.futures.ThreadPoolExecutor(max_workers= max_workers) as executor:
        futures = [executor.submit(states_to_binary,state) for state in decrypted_states]
        binary_data = b''.join([future.result() for future in futures])
    # Ghi bản rõ vào file
    with open(file_path, 'wb') as file:
        file.write(binary_data)
# file_path = "VOCABS.docx"

# encryptFile(file_path)
# decryptFile(file_path + '.enc')
