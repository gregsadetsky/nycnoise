FROM python:3.12.1

# docker will not re-pip install if requirements.txt doesn't change
WORKDIR /code
ADD ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

ADD . /code

RUN --mount=type=secret,id=.env env $(cat /run/secrets/.env | xargs) python manage.py compilescss
RUN --mount=type=secret,id=.env env $(cat /run/secrets/.env | xargs) python manage.py collectstatic --no-input

CMD ["bin/serve.sh"]
