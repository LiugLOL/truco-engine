from fastapi import FastAPI

app = FastAPI(title="Truco Engine API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
