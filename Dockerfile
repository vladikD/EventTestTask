FROM python:3.12

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV DJANGO_SETTINGS_MODULE=EventTestTask.settings

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "EventTestTask.wsgi:application"]
