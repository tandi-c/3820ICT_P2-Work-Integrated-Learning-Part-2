FROM python:3.9-alpine

ENV PATH="/scripts:${PATH}"

COPY ./requirements.txt /requirements.txt
RUN apk add build-base
RUN apk add --update --no-cache --virtual .tmp gcc g++ libstdc++ musl-dev lapack-dev freetype-dev python3-dev libc-dev linux-headers gfortran
RUN apk add git
RUN apk add py3-scipy
RUN pip3 install --upgrade -i https://mirrors.aliyun.com/pypi/simple pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /requirements.txt
RUN python3 -m pip install --upgrade https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.12.0-py3-none-any.whl

RUN apk del .tmp

RUN mkdir /intelligait_app
COPY ./intelligait_app /intelligait_app
WORKDIR /intelligait_app
COPY ./scripts /scripts

RUN chmod +x /scripts/*

RUN mkdir -p /vol/web/media
RUN mkdir -p /vol/web/static

RUN adduser -D user
RUN chown -R user:user /vol
RUN chmod -R 755 /vol/web
USER user

CMD ["entrypoint.sh"]
