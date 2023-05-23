FROM --platform=linux/amd64 python:3.9.6
MAINTAINER Chandan Mishra
WORKDIR /runner
COPY requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt
RUN mkdir -p /app
RUN mkdir -p /static
COPY app/ ./app/
COPY static/ ./static/
COPY main.py .
ENV PYTHONPATH /runner
ARG AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-""}
ARG AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-""}
ENV AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID}
ENV AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY}
CMD ["python", "main.py"]
EXPOSE 8000
