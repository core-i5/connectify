FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /connectify/user_service

COPY requirements.txt /connectify/user_service/

RUN pip install --upgrade pip setuptools wheel && \    
    python -m venv /py && \
    /py/bin/pip install --no-cache-dir -r requirements.txt && \
    rm -f requirements.txt && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user
        
COPY . /connectify/user_service/

ENV PATH="/py/bin:$PATH"
USER django-user

CMD ["gunicorn", "--workers=3", "--bind", "0.0.0.0:8000", "user_service.wsgi:application"]
