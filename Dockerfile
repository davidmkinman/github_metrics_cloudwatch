FROM amazon/aws-lambda-python:3.8

RUN /var/lang/bin/python3.8 -m pip install --upgrade pip

COPY app/requirements.txt .

RUN /var/lang/bin/python3.8 -m pip install -r requirements.txt
COPY app/app.py .

CMD ["app.lambda_handler"]