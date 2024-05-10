import React, { useRef, useEffect, useState } from "react";
import axios from "axios";

const position = {
  top: 0,
  left: 0,
};
const VideoCapture = () => {
  const videoRef = useRef(null);
  const canvasRef = useRef(null);

  const [faceLocations, setFaceLocations] = useState([]);

  useEffect(() => {
    const processFrame = async () => {
      const video = videoRef.current;
      const canvas = canvasRef.current;
      const context = canvas.getContext("2d");
      context.drawImage(video, 0, 0, canvas.width, canvas.height);

      try {
        // Capturar o quadro como uma imagem em base64
        const frameDataUrl = canvas.toDataURL("image/jpeg");
        const base64Data = frameDataUrl.split(",")[1]; // Extrair a parte codificada em base64
        //console.log("Conteúdo do arquivo enviado:", frameDataUrl);

        // Enviar o quadro para o servidor Django

        const response = await axios.post(
          "http://192.168.1.144:5001/processar_frames/",
          {
            frame: base64Data,
          }
        );
        //console.log(response);

        // Atualizar as localizações das faces
        setFaceLocations(response.data.faces);
      } catch (error) {
        console.error("Erro ao processar quadro:", error);
      }

      requestAnimationFrame(processFrame);
    };

    processFrame();
  }, []);
  const startVideo = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: "true", // Use 'user' for the front camera or 'environment' for the back camera
      });
      videoRef.current.srcObject = stream;
    } catch (error) {
      console.error("Erro ao iniciar vídeo:", error);
    }
  };
  const handleStartVideo = () => {
    const response1 = axios.get(
      "http://192.168.154.229:5001/processar_frames/"
    );
    console.log(response1);
  };
  startVideo();
  return (
    <div
      style={{
        position: "relative",
        display: "flex",
        justifyContent: "flex-end",
      }}
    >
      <button onClick={handleStartVideo}>Iniciar Câmera</button>

      {/* Vídeo da câmera */}
      <video
        ref={videoRef}
        style={{ position: "absolute", top: "-9999px" }}
        width="640"
        height="480"
        autoPlay
      ></video>
      {/* Canvas para desenhar retângulos sobre as faces */}
      <canvas
        ref={canvasRef}
        width="640"
        height="480"
        style={{ position: "absolute", top: position.top, left: position.left }}
      ></canvas>

      {/* Exibir retângulos sobre as faces detectadas */}
      <div
        style={{
          display: "flex",
          justifyContent: "center",
          flexDirection: "column",
        }}
      >
        {faceLocations.map((face, index) => (
          <div
            key={index}
            style={{
              position: "absolute",
              left: face.x + position.left,
              top: face.y + position.top,
              width: face.w,
              height: face.h,
              border: "2px solid red",
              pointerEvents: "none",
              // Centralizar o retângulo
              boxSizing: "border-box", // Incluir a largura da borda no cálculo
            }}
          ></div>
        ))}
      </div>
    </div>
  );
};

export default VideoCapture;
