from encryptAES import *  
from decryptAES import *
import os
import struct 

# Tạo khoá 16 byte (128 bit)
# key = os.urandom(16) 
# key_hex = key.hex() #chuyển sang hex

# Lưu khóa vào file Notepad
# with open("key.txt", "w") as file:
#   file.write(key_hex)

key_hex = "32df43dc72149ac2e06bacdee6264b9f"

# Chia chuỗi thành các phần mỗi phần 8 ký tự
w = []
for i in range(0, len(key_hex), 8):
  wi = int("0x" + key_hex[i:i+8], 16)
  w.append(wi)
  
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


def states_to_binary(states):
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


def encryptFile(file_path):
  contentFile = read_text_file(file_path)
  states = binary_to_states(contentFile)

  # Mã hóa AES
  encrypted_states = []
  for state in states:
    encrypted_content = encrypt(state, w)
    encrypted_states.append(encrypted_content)

  # Chuyển đổi các encrypted_states thành dữ liệu nhị phân
  encrypted_binary = states_to_binary(encrypted_states)

  # Ghi dữ liệu nhị phân vào file
  with open(file_path + '.enc', 'wb') as file:
    file.write(encrypted_binary)


def decryptFile(file_path):
  # Đọc dữ liệu nhị phân từ file
  with open(file_path, 'rb') as file:
    encrypted_binary = file.read()

  # Chuyển đổi dữ liệu nhị phân thành các state
  encrypted_states = binary_to_states(encrypted_binary)

  # Giải mã AES
  decrypted_states = []
  for encryptState in encrypted_states:
    decrypted_content = decrypt(encryptState, w)
    decrypted_states.append(decrypted_content)

  # Chuyển đổi state sang binary
  binary_data = states_to_binary(decrypted_states)

  # Ghi bản rõ vào file
  with open(file_path.replace('.enc', '_decrypted.txt'), 'wb') as file:
    file.write(binary_data)

file_path = "test.txt"

encryptFile(file_path)
decryptFile(file_path + '.enc')


#Note:
#Chạy fnc encryptFile để mã hoá file cần mã hoá
#Chạy fnc decrypteFile để giải mã file bị mã hoá trước đó