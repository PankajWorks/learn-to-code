FROM python:alpine3.18
COPY requirements.txt ~/
RUN pip install -r requirements.txt
COPY server.py /app/
WORKDIR /app
EXPOSE 5000
ENTRYPOINT ["python", "server.py"]