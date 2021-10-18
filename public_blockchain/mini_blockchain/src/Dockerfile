# > docker build -t mini_blockchain .
# > docker run -it -p 5000:5000 mini_blockchain
FROM python:2.7-alpine

RUN pip install flask rsa==3.4.2

COPY serve.py .

EXPOSE 5000

CMD ["python", "./serve.py"]
