FROM python:3.13

RUN mkdir /app
RUN mkdir /files
RUN mkdir /var/static

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1 

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic

EXPOSE 8001

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "tarsashaz.wsgi:application"]