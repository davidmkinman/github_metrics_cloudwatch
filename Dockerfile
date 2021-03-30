# Define function directory
ARG FUNCTION_DIR="/function"

# This is the surigate container, preparing the function for its home
FROM ubuntu:18.04 as build-image
ARG FUNCTION_DIR
## Install aws-lambda-cpp build dependencies
RUN apt-get update && \
  apt-get install -y \
  libtool \
  automake \
  m4 \
  autoconf \
  g++ \
  make \
  cmake \
  unzip \
  libcurl4-openssl-dev

RUN apt-get update && apt-get install -y python3  python3-pip python3-venv

RUN mkdir -p ${FUNCTION_DIR}
COPY app/* ${FUNCTION_DIR}

RUN pip3 install --target ${FUNCTION_DIR} awslambdaric
RUN pip3 install --target ${FUNCTION_DIR} -r ${FUNCTION_DIR}/requirements.txt
#RUN python3 -m venv ${FUNCTION_DIR}/venv

# Create the lambda container, without the build fluff
FROM ubuntu:18.04

ARG FUNCTION_DIR
RUN apt-get update && apt-get install -y python3
COPY --from=build-image ${FUNCTION_DIR} ${FUNCTION_DIR}

WORKDIR ${FUNCTION_DIR}
#ENTRYPOINT [ "${FUNCTION_DIR}/venv/bin/python3", "-m", "awslambdaric" ]
ENTRYPOINT [ "python3", "-m", "awslambdaric" ]
CMD [ "app.lambda_handler" ]