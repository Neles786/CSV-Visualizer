FROM python:3.10-slim

WORKDIR /

RUN mkdir apps

COPY results/*.csv apps/results/

COPY debugger.py /apps/

COPY requirements.txt /apps/

RUN pip install -r /apps/requirements.txt

ENTRYPOINT ["python3", "/apps/debugger.py"]