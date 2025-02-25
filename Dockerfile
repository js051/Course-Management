# Dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
COPY .env ./
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
HEALTHCHECK --interval=30s --timeout=3s CMD curl --fail http://localhost:8000/health || exit 1
