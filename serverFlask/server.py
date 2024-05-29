from flask import Flask, request, jsonify
from flask_cors import CORS
import cv2
from PIL import Image
from io import BytesIO
import io
import base64
import json
import numpy as np
import os
import uuid
import time
from fer import FER
import csv
import sys
from threading import Lock
lock = Lock()


    
app = Flask(__name__)

CORS(app)

ip = "150.161.121.253"
#ip = "10.0.0.200"

my_port=5001
lastData = {}

def generate_service_id():
    # Gerar um UUID (identificador único universal)
    service_id = uuid.uuid4()
    # Formatando o UUID para o formato desejado
    formatted_service_id = str(service_id).replace('-', '')[:23]
    return formatted_service_id

# Exemplo de uso
service_id = generate_service_id()
#print(service_id)
# Endpoint GET que retorna "ola"

# Função para registrar na API 

def salvar_dados_csv(data):
    # Verificar se o arquivo CSV já existe
    csv_file = 'data.csv'

    # Verifica se o arquivo CSV já existe
    file_exists = os.path.isfile(csv_file)

    # Abre o arquivo CSV no modo de adição (append)
    with open(csv_file, mode='a', newline='') as file:
        writer = csv.writer(file)

        # Se o arquivo não existe, escreve o cabeçalho
        if not file_exists:
            writer.writerow(['rttTimer(ms)', 'latencyTime(ms)', 'packetSizeUp(B)', 'packetSizeDown(B)', 'Throughput(B/s)', 'processTime(ms)'])

        # Escreve os dados no CSV
        writer.writerow([data['rttTimer'], data['latencyTime'], data['packetSizeUp'], data['packetSizeDown'], data['Throughput'], data['processTime']])

def register_mec():
    import requests

    # Detalhes da API Flask
    flask_host = ip  # ou "0.0.0.0" para acesso externo
    flask_port = my_port
    flask_sid = service_id
    flask_path = "/apiFlask/v1"

    # JSON da API MEC com detalhes da API Flask preenchidos
    mec_data = {
        "description": "API Flask de processamento de imagem com visão computacional",
        "endpoints": [
            {
                "description": "Metodo para testar se a api esta funcionando corretamente",
                "method": "GET",
                "name": "Processar frame",
                "path": "/processar_frames",
                
            },
            {
                "description": "Metodo para enviar uma imagem e o frame ser processado e retornar posicao do rosto.",
                "method": "POST",
                "name": "Processar frame",
                "path": "/processar_frames",
                
            }
        ],
        "host": flask_host,
        "name": "remoteComputation",
        "path": flask_path,
        "port": flask_port,
        "protocol" :"http",
        "sid": "sid",
        "type": "ImgProc"
    }

    # URL de registro na API MECdef generate_service_id():
  

# Exemplo de uso
    mec_url = "http://172.22.0.169/service_registry/v1/register"

    try:
        # Fazendo a solicitação POST para registrar na API MEC
        response = requests.post(mec_url, json=mec_data)
        response.raise_for_status()  # Verifica se houve algum erro na solicitação

        # Extraindo e imprimindo a resposta
        response_data = response.json()
        print("Registro na API MEC bem-sucedido:", response_data)
    except Exception as e:
        print("Erro ao registrar na API MEC:", e)

# Registrar na API MEC ao iniciar o aplicativo Flask
register_mec()

face_detector = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
emotion_detector = FER(mtcnn=True)



@app.route('/processar_frames', methods=['GET', 'POST', 'OPTIONS'])
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
        frame_data = request.json['frame']
    
    # Converter o vetor tridimensional em uma matriz numpy
        frame_array = np.array(frame_data)
    
    # Converter a matriz numpy em uma imagem PIL
        image = Image.fromarray(frame_array.astype('uint8'))
        #print(image)
        image_grey = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        image_resized = cv2.resize(np.array(image), (640, 480))
        image_grey = cv2.resize(image_grey, (640, 480))
        
        # Converter a imagem PIL para um array numpy
        start_time = time.time()
        frame_np = face_detector.detectMultiScale(image_grey, minNeighbors=3)
        timeProcess = (time.time() - start_time) * 1000 
        #analysis = emotion_detector.detect_emotions(image_resized)
        #print(analysis)
        # Detectar faces na imagemx 
        nome_arquivo = 'imagem_recebida.jpg'
        caminho_arquivo = os.path.join('./', nome_arquivo)
        for (x, y, w, h) in frame_np:
            cv2.rectangle(image_grey, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imwrite(caminho_arquivo, image_grey)

        # Retornar as localizações das faces em formato JSON
        return jsonify({'faces': [{'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)} for x, y, w, h in frame_np], "timeProcess" : timeProcess})
        

    return jsonify({'error': 'Método não permitido'}), 405
@app.route('/processar_emotion', methods=['GET', 'POST', 'OPTIONS'])
def processar_emotions():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    if request.method == 'GET':
        return "Testando"

    if request.method == 'POST':
        global lastData
        # Obter o frame do corpo da solicitação
        frame_data = request.json
        #server_time = time.time()
        #client_time = frame_data.get("time")
        #print(server_time, client_time, "tempos")
        #tempoUpload = server_time - (client_time/1000)
        #print(tempoUpload *1000)
        rawFrame = frame_data.get("frame")
        teste = frame_data.get("csvSaver")
        sampleIterable = frame_data.get("sample")
        frame_array = np.array(rawFrame)
    
    # Converter a matriz numpy em uma imagem PIL
        image = Image.fromarray(frame_array.astype('uint8'))
        #print(image)
        
        image_resized = cv2.resize(np.array(image), (640, 480))
        
        # Converter a imagem PIL para um array numpy
        start_time = time.time()
        analysis = emotion_detector.detect_emotions(image_resized)
        timeProcess = (time.time() - start_time) * 1000 
        #print("timer ",teste['rttTimer'])
        lock.acquire()
        try:
            if(teste['rttTimer'] == 0):
                lastData = teste
                #print("last Data " , lastData)
                tamanho_bytes = sys.getsizeof(rawFrame)
                lastData["packetSizeUp"] = tamanho_bytes
                
            else:
                salva = teste
                teste = lastData
                teste['rttTimer'] = salva["rttTimer"]
                teste["Throughput"] =((teste["packetSizeUp"] +teste["packetSizeDown"]) /teste["rttTimer"]) *(1000)
                lastData = salva
                tamanho_bytes = len(rawFrame)
                lastData["packetSizeUp"] = tamanho_bytes
                if(sampleIterable<=100):

                    salvar_dados_csv(teste)
            lastData["processTime" ] =timeProcess
        finally:
            lock.release()
        #print(teste)
    # Converter o vetor tridimensional em uma matriz numpy
        

        #print(analysis)
        # Detectar faces na imagemx 
        
        faces_data = []
        max_emotions = []
        max_values = []

        for face in analysis:
            # Obtém os dados do rosto
            face_data = {'x': int(face['box'][0]), 'y': int(face['box'][1]), 'w': int(face['box'][2]), 'h': int(face['box'][3])}
            faces_data.append(face_data)

            # Obtém a emoção dominante e seu valor associado
            max_emotion = max(face['emotions'], key=face['emotions'].get)
            max_value = face['emotions'][max_emotion]

            max_emotions.append(max_emotion)
            max_values.append(max_value)
        # Retornar as localizações das faces em formato JSON
        response ={'faces': faces_data, "timeProcess" : timeProcess, 'emotion' : max_emotions, 'emotionValue': max_values} 
       
        return jsonify(response)
        

    return jsonify({'error': 'Método não permitido'}), 405
@app.route('/ping', methods=['GET', 'OPTIONS'])
def pring():
    if request.method == 'OPTIONS':
        response = jsonify()
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    if request.method == 'GET':

        return "pong"

        

    return jsonify({'error': 'Método não permitido'}), 405
if __name__ == '__main__':
    ssl_cert_path = './cert.pem'
    ssl_key_path = './key.pem'

    app.run( host=ip, port=my_port)
    