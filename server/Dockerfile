FROM python:3.12.0

RUN mkdir -p /home/app

COPY . /home/app

RUN pip install --upgrade pip
RUN pip3 install --no-cache-dir -r /home/app/requirements.txt

EXPOSE 8025

CMD ["python", "/home/app/src/index.py"]