FROM python:3.8.5

RUN mkdir /intelligait
WORKDIR /intelligait

ENV PATH=":${PATH}"

COPY requirements.txt .

RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
RUN apt-get update && apt-get install -y swig vim
# RUN apt-get install --reinstall libxcb-xinerama0
# RUN apt-get -y install openjdk-7-jre qtcreator build-essential
# RUN apt-get install qt5-default
RUN apt-get install -y libdbus-1-3 libxkbcommon-x11-0 libxcb-icccm4 \
    libxcb-image0 libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 \
    libxcb-xinerama0 libxcb-xinput0 libxcb-xfixes0


RUN pip3 install --upgrade -i https://mirrors.aliyun.com/pypi/simple pip
RUN pip install --upgrade pip setuptools wheel
RUN pip install -r requirements.txt

COPY . .

WORKDIR /intelligait/tf_pose_estimation/tf_pose/pafprocess
RUN swig -python -c++ pafprocess.i && python setup.py build_ext --inplace

WORKDIR /intelligait

EXPOSE 8000

# ENTRYPOINT  ["python", "manage.py"]


ADD entrypoint.sh .
RUN chmod +x entrypoint.sh

CMD ["entrypoint.sh"]
