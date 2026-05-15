FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir pytest pytest-json-report

COPY . .

CMD ["pytest", "test_generated.py", "--json-report", "--json-report-file=.report.json", "-v"]
