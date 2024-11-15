# Bazowy obraz TensorFlow (w wersji z GPU lub CPU)
#FROM tensorflow/tensorflow:2.12.0-gpu-jupyter
FROM tensorflow/tensorflow:2.10.1-gpu-jupyter

# Instalacja PyTorch i zależności
RUN apt-get update && apt-get install -y libgl1-mesa-glx
#RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
#RUN pip install torch==1.12.0+cu102 torchvision==0.13.0+cu102 torchaudio==0.12.0 --extra-index-url https://download.pytorch.org/whl/cu102
#RUN pip install torch==1.10.0+cu111 torchvision==0.11.0+cu111 torchaudio==0.10.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 torchaudio==0.11.0 --extra-index-url https://download.pytorch.org/whl/cu113
# (Opcjonalnie) Ustaw dodatkowe zależności lub konfiguracje
RUN pip install ultralytics

# Punkt wejścia do kontenera
CMD ["bash"]
