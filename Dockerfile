FROM python:3.8
LABEL MAINTAINER="ImanSedgh | Iman.sedgh@yahoo.com "

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /home/dongchiapp
WORKDIR /home/dongchiapp
COPY  ./requirements.txt /home/dongchiapp
RUN pip install -r requirements.txt
COPY . /home/dongchiapp


RUN python manage.py collectstatic --no-input

CMD ["gunicorn","--chdir","/home/dongchiapp","--bind",":8000","config.wsgi:application"]