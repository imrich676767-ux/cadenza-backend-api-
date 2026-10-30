import os
from flask import Flask, request, jsonify, send_file
import UnityPy

app = Flask(__name__)

@app.route('/')
def home():
    return "Cadenza Python Backend is running!"

@app.route('/convert', methods=['POST'])
def convert_asset():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    # บันทึกไฟล์ชั่วคราว
    input_path = os.path.join('/tmp', file.filename)
    file.save(input_path)

    try:
        # ដំណើរការ UnityPy សម្រាប់អាន Asset Bundle
        env = UnityPy.load(input_path)
        extracted_files = []

        for obj in env.objects:
            if obj.type.name in ["TextAsset", "Texture2D", "Sprite"]:
                data = obj.read()
                # ឧទាហរណ៍៖ ទាញយកទិន្នន័យ ឬកែច្នៃតាមតម្រូវការ
                
        # ត្រឡប់លទ្ធផលជា File ឬ JSON ទៅឱ្យ Frontend
        return jsonify({
            'status': 'success',
            'message': 'File converted successfully using UnityPy!'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
