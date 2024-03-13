FROM python
WORKDIR /app
COPY requirements.txt .
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
