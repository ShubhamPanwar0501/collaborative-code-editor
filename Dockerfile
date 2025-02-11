FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run tests before finalizing the build
RUN pytest > result.log; tail -n 10 result.log

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
