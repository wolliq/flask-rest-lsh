ARG IMAGE_VARIANT=slim-buster
ARG OPENJDK_VERSION=8
ARG PYTHON_VERSION=3.8.14

FROM python:${PYTHON_VERSION}-${IMAGE_VARIANT} AS py3
FROM openjdk:${OPENJDK_VERSION}-${IMAGE_VARIANT}

COPY --from=py3 / /

ARG PYSPARK_VERSION=3.3.1
RUN pip --no-cache-dir install pyspark==${PYSPARK_VERSION}

EXPOSE 5000

COPY ./requirements.txt requirements.txt
WORKDIR /app
COPY . /app

RUN cd /app

RUN apt-get update && apt-get install -y --no-install-recommends build-essential vim
RUN pip install --trusted-host pypi.python.org -r requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0"]