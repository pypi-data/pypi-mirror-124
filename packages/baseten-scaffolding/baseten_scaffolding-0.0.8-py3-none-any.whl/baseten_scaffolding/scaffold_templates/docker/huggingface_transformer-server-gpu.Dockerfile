FROM nvidia/cuda:10.2-cudnn7-devel-ubuntu18.04

RUN apt update && \
    apt install -y bash \
                   build-essential \
                   git \
                   curl \
                   ca-certificates \
                   python3 \
                   python3-pip && \
    rm -rf /var/lib/apt/lists

RUN python3 -m pip install --no-cache-dir --upgrade pip && \
    python3 -m pip install --no-cache-dir \
    mkl \
    torch

RUN git clone https://github.com/NVIDIA/apex
RUN cd apex && \
    python3 setup.py install && \
    pip install -v --no-cache-dir --global-option="--cpp_ext" --global-option="--cuda_ext" ./

COPY ./src/server_requirements.txt server_requirements.txt
RUN pip install -r server_requirements.txt

COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt

ENV PORT 8080
ENV APP_HOME /app

WORKDIR $APP_HOME
COPY ./src .

# BaseTen specific build arguments and environment variables
ARG RUNTIME_ENV
ARG SENTRY_URL
ENV RUNTIME_ENV=$RUNTIME_ENV
ENV SENTRY_URL=$SENTRY_URL

ARG hf_task
ARG has_hybrid_args
ARG has_named_args
ENV hf_task=$hf_task
ENV has_hybrid_args=$has_hybrid_args
ENV has_named_args=$has_named_args

CMD exec python3 inference_server.py
