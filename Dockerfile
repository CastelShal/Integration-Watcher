FROM python:3.14

WORKDIR /application

COPY ./app ./app
COPY ./static ./static 
COPY requirements.txt run.py ./
RUN mkdir logs/
RUN pip install -r requirements.txt

ENV RUNNING_IN_DOCKER=True
EXPOSE 5000

# CMD ["sleep", "infinity"]
CMD ["python", "run.py"]