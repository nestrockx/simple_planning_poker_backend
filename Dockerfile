FROM python:3.11.9-alpine

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

ENV PORT=8000

EXPOSE 8000

CMD ["daphne", "simple_planning_poker.asgi:application", "--bind", "0.0.0.0", "--port", "8000"]
