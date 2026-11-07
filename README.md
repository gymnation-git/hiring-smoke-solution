# hiring-smoke-solution

A correct solution to the **smoke** take-home, the pipeline test of the
GymNation hiring grader. Not a hiring task: it only proves that a public repo
goes through clone, sandboxed build, test stage, health check, checks and
report.

- `GET /health` → 200
- `POST /echo {"text": "…"}` → `{"text": "…", "length": <characters>}`
- `GET /sum?a=<int>&b=<int>` → `{"sum": a + b}`
- `GET /upper?text=…` → `{"text": "…"}` (interview extension E1)
- Invalid input → `422 {"error": {"code": "VALIDATION", "message": "…"}}`

```sh
docker build -t smoke . && docker run -p 8080:8080 smoke
docker build --target test .
```
