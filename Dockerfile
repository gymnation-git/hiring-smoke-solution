FROM python:3.14-slim AS base
WORKDIR /app
COPY app.py .

# `docker build --target test .` runs the tests.
FROM base AS test
COPY test_app.py .
RUN python -m unittest -v test_app

FROM base
EXPOSE 8080
CMD ["python", "app.py"]
