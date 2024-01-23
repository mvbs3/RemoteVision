from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
from PIL import Image
from io import BytesIO
import base64
import json
import numpy as np
import os

app = Flask(__name__)
CORS(app)

face_detector = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')

@app.route('/processar_frames/', methods=['GET', 'POST', 'OPTIONS'])
def processar_frames():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    if request.method == 'GET':
        return "Testando"

    if request.method == 'POST':
        # Obter o frame do corpo da solicitação
        frame_data_url = json.loads(request.data.decode('utf-8'))
        base64_data = frame_data_url.get("frame", "")
        image_data = base64.b64decode(base64_data)
        image = Image.open(BytesIO(image_data))
        
        image_grey = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        image_grey = cv2.resize(image_grey, (640, 480))
        
        # Converter a imagem PIL para um array numpy
        frame_np = face_detector.detectMultiScale(image_grey, minNeighbors=3)

        # Detectar faces na imagem
        nome_arquivo = 'imagem_recebida.jpg'
        caminho_arquivo = os.path.join('./', nome_arquivo)
        for (x, y, w, h) in frame_np:
            cv2.rectangle(image_grey, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imwrite(caminho_arquivo, image_grey)

        # Retornar as localizações das faces em formato JSON
        return jsonify({'faces': [{'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)} for x, y, w, h in frame_np]})

    return jsonify({'error': 'Método não permitido'}), 405

if __name__ == '__main__':
    ssl_cert_path = './cert.pem'
    ssl_key_path = './key.pem'

    app.run(ssl_context=(ssl_cert_path, ssl_key_path), host='0.0.0.0', port=8000, debug=True)
    