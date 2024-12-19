FROM python:3.11-slim
RUN apt update && apt clean
RUN pip install pipenv
WORKDIR /
COPY .. .
RUN pipenv install --system --deploy --ignore-pipfile
COPY wait_for_db.py /usr/local/bin/wait_for_db.py
RUN chmod +x /usr/local/bin/wait_for_db.py
EXPOSE 8000
CMD ["sh", "-c", "python /usr/local/bin/wait_for_db.py \
    && alembic upgrade head \
    && alembic history \
    && uvicorn app.main:app --host 0.0.0.0 --port 8000"]