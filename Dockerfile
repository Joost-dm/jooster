FROM python:3.6

WORKDIR /jooster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV SECRET_KEY '5bf8x-s^^mq01xum9ro_qv9md0@54v&m#x_-uu(_hyf1rws&ww'
ENV DEBUG True
ENV AWS_ACCESS_KEY_ID 'AKIARQBNDTEHJJ2QDQOZ'
ENV AWS_SECRET_ACCESS_KEY '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'
ENV AWS_STORAGE_BUCKET_NAME 'jooster'
ENV AWS_S3_CUSTOM_DOMAIN 'jooster.s3.amazonaws.com'

RUN pip3 install --upgrade pip

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3"]
CMD ["manage.py", "runserver", "0.0.0.0:8000"]
# copy project

