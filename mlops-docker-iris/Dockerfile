FROM python:3.11-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
COPY train.py predict.py ./
RUN python train.py
ENTRYPOINT ["python", "predict.py"]
