FROM python:3.9-alpine

WORKDIR /code
ADD ./app /code/

COPY requirements.txt /code/

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

CMD ["python", "main.py"]

