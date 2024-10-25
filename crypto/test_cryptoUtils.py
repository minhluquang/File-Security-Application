import os
from cryptoUtils import encryptFile, decryptFile

# Tạo nội dung file mẫu để kiểm tra
def create_test_file(file_path, content):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Kiểm tra mã hóa và giải mã
def test_crypto():
    # Bước 1: Tạo file mẫu để mã hóa
    test_file_path = 'test_sample.txt'
    original_content = "Đây là nội dung thử nghiệm để kiểm tra mã hóa AES và RSA!@@"
    create_test_file(test_file_path, original_content)
    
    # Bước 2: Mã hóa file
    print("Đang mã hóa file...")
    encryptFile(test_file_path)

    # Bước 3: Kiểm tra xem file đã được mã hóa hay chưa
    with open(test_file_path, 'rb') as file:
        encrypted_content = file.read()
        print(f"Nội dung sau khi mã hóa (dưới dạng nhị phân): {encrypted_content}")

    # Bước 4: Giải mã file
    print("Đang giải mã file...")
    decryptFile(test_file_path)

    # # Bước 5: Kiểm tra nội dung sau khi giải mã
    with open(test_file_path, 'r',encoding='utf-8') as file:
        decrypted_content = file.read()
        print(f"Nội dung sau khi giải mã: {decrypted_content}")

    # So sánh kết quả
    if original_content == decrypted_content:
        print("Kiểm tra thành công: Nội dung giải mã khớp với bản gốc.")
    else:
        print("Kiểm tra thất bại: Nội dung giải mã không khớp với bản gốc.")

# Gọi hàm test
if __name__ == '__main__':
    test_crypto()

    # Xóa file sau khi test xong (tùy chọn)
    # os.remove('test_sample.txt')
