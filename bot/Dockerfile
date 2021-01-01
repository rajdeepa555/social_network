FROM python:3
ENV PYTHONUNBUFFERED=1
ADD . / 

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "./run.py" ]