FROM python:3.9-slim

WORKDIR /connectify/user_service

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["gunicorn", "--workers=3", "--bind", "0.0.0.0:8000", "user_service.wsgi:application"]
