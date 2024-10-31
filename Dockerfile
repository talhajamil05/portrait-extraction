FROM python:3.9-slim

COPY requirements.txt /tmp/

RUN pip install -U pip && \
    pip install -r /tmp/requirements.txt

COPY . /src

WORKDIR /src

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
