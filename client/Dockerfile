FROM python:3.12.0

RUN mkdir -p /home/app

COPY . /home/app

RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r /home/app/requirements.txt

CMD ["python", "/home/app/client.py"]