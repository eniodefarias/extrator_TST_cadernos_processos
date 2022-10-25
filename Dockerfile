#FROM python:3


################################
# temp stage
#FROM python:3.9-slim as builder
FROM python:3.9-slim

LABEL maintaner="eniodefarias@gmail.com"

#env PIP_DISABLE_ROOT_WARNING=1

WORKDIR /app
#WORKDIR /

#COPY . /app
#COPY . /
COPY src /app/src
COPY Requeriments.txt /app/
COPY src/dejt_001_extrator_TST.py /app/
#RUN mkdir -p /app/TMP/log /app/Output_Files

#COPY src/google-chrome /usr/bin/

#RUN apt-get update
#RUN apt-get install ffmpeg libsm6 libxext6  -y
#RUN apt-get update && apt-get install -y --no-install-recommends gcc && apt-get install ffmpeg libsm6 libxext6  -y && apt-get install libgl1 && apt-get install -y python3-opencv && apt install -y libgl1-mesa-glx


#RUN apt-get update && apt-get install -y --no-install-recommends gcc && apt-get install ffmpeg libsm6 libxext6  -y && apt-get install libgl1 -y && apt-get install -y python3-opencv && apt install -y libgl1-mesa-glx


RUN apt-get update && apt-get install -y --no-install-recommends gcc ffmpeg libsm6 libxext6 libgl1 python3-opencv libgl1-mesa-glx xdg-utils wget fonts-liberation default-jdk tzdata

#https://dev.to/0xbf/set-timezone-in-your-docker-image-d22
ENV TZ="America/Sao_Paulo"
RUN dpkg -i /app/src/106.0.5249.119-1_google-chrome-stable_current_amd64.deb
#google-chrome

#RUN dpkg -i /app/src/google-chrome-stable_current_amd64.deb

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip && cat Req*.txt|sort|uniq | xargs -n 1 pip install && pip install --upgrade pip

#WORKDIR /
#VOLUME TMP /TMP
#VOLUME Output_Files /Output_Files

#ENV IS_DOCKER=true
#ENV PYTHONPATH "/"

#CMD python3 /app/dejt_001_extrator_TST.py
CMD python3 /app/src/dejt_001_extrator_TST.py
#CMD python3 /app/src/dejt_001_extrator_TST.py  | perl -pe 's/^.*SSH.*$/\e[1;34;40m$&\e[0m/g;s/^.*MYSQL.*$/\e[1;35;40m$&\e[0m/g;s/^.*SHELL.*$/\e[1;32;40m$&\e[0m/g;s/^.*FTP.*$/\e[1;33;40m$&\e[0m/g;s/^.*FATAL.*$/\e[1;37;41m$&\e[0m/g; s/^.*ERROR.*$/\e[1;31;40m$&\e[0m/g; s/^.*WARN.*$/\e[0;33;40m$&\e[0m/g; s/^.*INFO.*$/\e[0;36;40m$&\e[0m/g; s/^.*DEBUG.*$/\e[105m$&\e[0m/g;s/\n/\n\n/g'

##########################
# final stage
#FROM python:3.9-slim

#WORKDIR /
#COPY . /
#COPY --from=builder /opt/venv /opt/venv

#WORKDIR /app
#COPY src /app
#COPY Requeriments.txt /app
#COPY dejt_001_extrator_TST.py /app
#ENV PATH="/opt/venv/bin:$PATH"

#VOLUME /app
#ENV IS_DOCKER=true
#ENV PYTHONPATH "/app"

#CMD python3 dejt_001_extrator_TST.py