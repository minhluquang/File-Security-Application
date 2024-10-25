from flask import Flask, render_template, request, jsonify
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto.cryptoUtils import *
from crypto.cryptoRSA import *
app = Flask(__name__)
base_dir = os.path.dirname(os.path.abspath(__file__))
app.config['ENCODE_FOLDER'] = os.path.join(base_dir, '../storage/files_encoded') # Thư mục chứa file đã mã hóa là 'files_encoded'
app.config['DECODE_FOLDER'] = os.path.join(base_dir, '../storage/files_decoded') # Thư mục chứa file đã giải mã là 'files_decoded'
if not os.path.exists(app.config['ENCODE_FOLDER']):
    os.makedirs(app.config['ENCODE_FOLDER'])
if not os.path.exists(app.config['DECODE_FOLDER']):
    os.makedirs(app.config['DECODE_FOLDER'])
@app.route('/')
def index():
    return render_template('mainGUI.html')

@app.route('/encode', methods=['POST'])
def encode_file():
    if 'files' not in request.files:
        return jsonify({'message': 'Vui lòng chọn file cần mã hóa'}), 400
    files = request.files.getlist('files')
    for file in files:
        if file.filename == '':
            return jsonify({'message': 'Vui lòng chọn file cần mã hóa'}), 400
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['ENCODE_FOLDER'], filename)
            try:
                file.save(file_path)
                encryptFile(file_path)
            except Exception as e:
                return jsonify({'message': f'Lưu file thất bại: {str(e)}'}), 500
    return jsonify({'message': 'Files đã được mã hóa'}), 200
@app.route('/decode', methods=['POST'])
def decode_file():
    if 'files' not in request.files:
        return jsonify({'message': 'Vui lòng chọn file cần giải mã'}), 400
    files = request.files.getlist('files')
    for file in files:
        if file.filename == '':
            return jsonify({'message': 'Vui lòng chọn file cần giải mã'}), 400
        if file:
            filename = file.filename
            file_path = os.path.join(app.config['DECODE_FOLDER'], filename)
            try:
                file.save(file_path)
                decryptFile(file_path)
            except Exception as e:
                return jsonify({'message': f'Lưu file thất bại: {str(e)}'}), 500
    return jsonify({'message': 'Files đã được giải mã'}), 200

# def encrypt_file(file_path):
#     # Hàm mã hóa file
#     try:
#         # Thực hiện mã hoá
#         file_name = os.path.basename(file_path)
        
#         print(file_name)
#     except Exception as e:
#         raise Exception(f'Mã hóa thất bại: {str(e)}')

if __name__ == '__main__':
    app.run(debug=True)