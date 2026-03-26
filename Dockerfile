FROM python:3.14

WORKDIR /application

COPY ./app ./app
COPY ./static ./static 
COPY requirements.txt run.py ./

RUN pip install -r requirements.txt

EXPOSE 5000

# CMD ["sleep", "infinity"]
CMD ["python", "run.py"]