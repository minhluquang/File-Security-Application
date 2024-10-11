from encryptAES import *  
import os
import struct 

# Tạo khoá 16 byte (128 bit)
key = os.urandom(16) 
key_hex = key.hex() #chuyển sang hex

# Lưu khóa vào file Notepad
with open("key.txt", "w") as file:
  file.write(key_hex)

# Chia chuỗi thành các phần mỗi phần 8 ký tự
w = []
for i in range(0, len(key_hex), 8):
  wi = int("0x" + key_hex[i:i+8], 16)
  w.append(wi)
  
def read_text_file(file_path):
  with open(file_path, "r", encoding='utf-8') as file:
    return file.read()  # Đọc toàn bộ nội dung file

def string_to_states(input_string):
    # Bước 1: Chuyển đổi chuỗi thành bytes
    byte_data = input_string.encode('utf-8')
    
    # In ra độ dài của byte_data để tham khảo
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

def state_to_string(state):
    # Bước 1: Chuyển đổi từng số nguyên 32-bit trong state thành 4 bytes
    byte_data = b''.join([num.to_bytes(4, byteorder='big') for num in state])

    # Bước 2: Loại bỏ các byte đệm (0x00) nếu có
    byte_data = byte_data.rstrip(b'\x00')

    # Bước 3: Chuyển đổi byte_data thành chuỗi ký tự
    return byte_data.decode('utf-8')


file_path = "test.txt"
word_content = read_text_file(file_path)
states = string_to_states(word_content)
previousState = state_to_string(states[0])

for state in states:
  encrypted_content = encrypt(state, w)
  showMatrix(encrypted_content)
  print("\n")

# with open("test.txt", "wb") as file:
#   for i in range(len(encrypted_content)): 
#     word_data = str(showWord(encrypted_content[i]))  
#     file.write(word_data.encode('utf-8'))

# print(f"Đã ghi nội dung mã hóa vào {file_path}")


