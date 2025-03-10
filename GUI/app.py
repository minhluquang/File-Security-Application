from flask import Flask, render_template, request, jsonify
import os
import sys
import time
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto.cryptoUtils import *
from crypto.cryptoRSA import *
import requests
from callAPI import *

app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))
app.config["ENCODE_FOLDER"] = os.path.join(
    base_dir, "../storage/files_encoded"
)  # Thư mục chứa file đã mã hóa là 'files_encoded'
app.config["DECODE_FOLDER"] = os.path.join(
    base_dir, "../storage/files_decoded"
)  # Thư mục chứa file đã giải mã là 'files_decoded'
if not os.path.exists(app.config["ENCODE_FOLDER"]):
    os.makedirs(app.config["ENCODE_FOLDER"])
if not os.path.exists(app.config["DECODE_FOLDER"]):
    os.makedirs(app.config["DECODE_FOLDER"])


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/mainPage")
def mainPage():
    return render_template("mainPage.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/encode", methods=["POST"])
def encode_file():
    if "files" not in request.files:
        return jsonify({"message": "Vui lòng chọn file cần mã hóa"}), 400
    files = request.files.getlist("files")
    for file in files:
        if file.filename == "":
            return jsonify({"message": "Vui lòng chọn file cần mã hóa"}), 400
        if file:
            filename = file.filename
            file_path = os.path.join(app.config["ENCODE_FOLDER"], filename)
            try:
                # save_Key("private_key", "key_aes")
                key = get_Key()
                if key is None:
                    return jsonify({"message": "Không thể lấy khóa mã hóa"}), 500
                private_key = key["privateKey_rsa"]
                key_aes = key["key_aes"]
                # print(private_key)
                # print(key_aes)
                if private_key is None or key_aes is None:
                    generate_keys = generate_and_encrypt_key()
                    # print("ge", generate_keys)
                    private_key = generate_keys[0]
                    key_aes = generate_keys[1]
                    save_Key_res = save_Key(generate_keys[0], generate_keys[1])
                    if save_Key_res is None:
                        return jsonify({"message": "Không thể lưu khóa mã hóa"}), 500
                # print("key", private_key)
                # print("key", key_aes)
                file.save(file_path)
                start_time = time.perf_counter()
                encryptFile(file_path, key_aes, private_key)
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                print(f"Thời gian mã hóa là: {execution_time} giây")
            except Exception as e:
                return jsonify({"message": f"Lưu file thất bại: {str(e)}"}), 500
    return jsonify({"message": "Files đã được mã hóa"}), 200


@app.route("/decode", methods=["POST"])
def decode_file():
    if "files" not in request.files:
        return jsonify({"message": "Vui lòng chọn file cần giải mã"}), 400
    files = request.files.getlist("files")
    for file in files:
        if file.filename == "":
            return jsonify({"message": "Vui lòng chọn file cần giải mã"}), 400
        if file:
            filename = file.filename
            file_path = os.path.join(app.config["DECODE_FOLDER"], filename)
            try:
                key = get_Key()
                if key is None:
                    return jsonify({"message": "Không thể lấy khóa mã hóa"}), 500
                private_key = key["privateKey_rsa"]
                key_aes = key["key_aes"]
                file.save(file_path)
                start_time = time.perf_counter()
                decryptFile(file_path, key_aes, private_key)
                end_time = time.perf_counter()
                execution_time = end_time - start_time
                print(f"Thời gian giải mã là: {execution_time} giây")
            except Exception as e:
                return jsonify({"message": f"Lưu file thất bại: {str(e)}"}), 500
    return jsonify({"message": "Files đã được giải mã"}), 200


@app.route("/changePassword")
def changePassword():
    return render_template("changePassword.html")


# def encrypt_file(file_path):
#     # Hàm mã hóa file
#     try:
#         # Thực hiện mã hoá
#         file_name = os.path.basename(file_path)

#         print(file_name)
#     except Exception as e:
#         raise Exception(f'Mã hóa thất bại: {str(e)}')

if __name__ == "__main__":
    app.run(debug=True)
