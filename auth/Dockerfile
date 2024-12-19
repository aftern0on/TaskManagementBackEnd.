FROM python:3.11-slim
RUN apt update && apt clean
RUN pip install pipenv
WORKDIR /
COPY .. .
RUN pipenv install --system --deploy --ignore-pipfile
ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /usr/local/bin/wait-for-it.sh
RUN chmod +x /usr/local/bin/wait-for-it.sh
EXPOSE 8000
CMD ["sh", "-c", "/usr/local/bin/wait-for-it.sh db:5432 -- \
    && alembic revision --autogenerate -m 'Initial migration' \
    && alembic upgrade head \
    && alembic history \
    && uvicorn app.main:app --host 0.0.0.0 --port 8000"]