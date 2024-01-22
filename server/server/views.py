from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
from PIL import Image
from io import BytesIO
import base64
import json
import numpy as np
import os
face_detector = cv2.CascadeClassifier('../haarcascade_frontalface_default.xml')
@csrf_exempt
def processar_frames(request):
    if request.method == 'OPTIONS':
        response = HttpResponse()
        response['Access-Control-Allow-Origin'] = '*'  # ou adicione seu domínio específico
        response['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    if request.method == 'GET':
        return HttpResponse("Testando")
    if request.method == 'POST':
        # Obter o frame do corpo da solicitação
        frame_data_url = json.loads(request.body.decode('utf-8'))
        base64_data = frame_data_url.get("frame", "")
        image_data = base64.b64decode(base64_data)
        image = Image.open(BytesIO(image_data))
        
        image_grey = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        image_grey = cv2.resize(image_grey, (640, 480))
        # Converter a imagem PIL para um array numpy
        frame_np = face_detector.detectMultiScale(image_grey,
                                                minNeighbors=3)

        # Detectar faces na imagem
        nome_arquivo = 'imagem_recebida.jpg'
        caminho_arquivo = os.path.join('./', nome_arquivo)
        for (x, y, w, h) in frame_np:
            cv2.rectangle(image_grey, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imwrite(caminho_arquivo, image_grey)        # Retornar as localizações das faces em formato JSON
        print(frame_np)
        
        return JsonResponse({'faces': [{'x': int(x), 'y': int(y), 'w': int(w), 'h': int(h)} for x, y, w, h in frame_np]})

    return JsonResponse({'error': 'Método não permitido'}, status=405)