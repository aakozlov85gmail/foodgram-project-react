FROM python:3.8-slim
WORKDIR /app
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]