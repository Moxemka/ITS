FROM python

WORKDIR /app

COPY . .

CMD ["python", "PythonApplication1.py"]