FROM gcr.io/ekstepspeechrecognition/text-to-speech-open-api-dependency:2.0


ARG DEBIAN_FRONTEND=noninteractive

RUN mkdir /opt/text_to_speech_open_api/
ENV base_path=/opt/text_to_speech_open_api/
ENV models_base_path=/opt/text_to_speech_open_api/deployed_models/
ENV model_logs_base_path=/opt/text_to_speech_open_api/deployed_models/logs/
RUN echo "export LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/local/lib" >> ~/.bashrc
WORKDIR /opt/text_to_speech_open_api/vakyansh-tts/src/glow_tts/
COPY ./server.py /opt/text_to_speech_open_api/vakyansh-tts/src/glow_tts/
CMD ["python3","/opt/text_to_speech_open_api/vakyansh-tts/src/glow_tts/server.py"]

