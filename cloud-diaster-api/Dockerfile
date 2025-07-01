FROM python:3.11-slim
#use python image as base

WORKDIR /app
#set our working directory

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#copy requirements and install

COPY ./app ./app
#copy apps source code

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]