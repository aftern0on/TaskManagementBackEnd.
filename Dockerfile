FROM python:3.11-slim
#RUN apt update && apt install build-essential libpg-dev && apt clean
RUN pip install pipenv
WORKDIR /app
COPY . /app
RUN pipenv install --system --deploy --ignore-pipfile
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]