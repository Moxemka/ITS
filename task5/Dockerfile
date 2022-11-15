FROM python

RUN pip install numpy

RUN pip install paho-mqtt

RUN pip install opencv-python

WORKDIR /app

COPY . .


CMD ["python", "hw_5.py"]