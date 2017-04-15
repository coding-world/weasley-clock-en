FROM python:3-onbuild
RUN pip install paho-mqtt
RUN pip install geopy

CMD ["python", "-u", "-d", "/app/test.py"]
