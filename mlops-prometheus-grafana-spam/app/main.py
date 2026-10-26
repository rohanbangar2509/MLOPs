import time
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field
from prometheus_client import Counter, Histogram, make_asgi_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

app = FastAPI(title="SMS Spam Detection API", version="1.0.0")

# Tiny built-in teaching dataset: no external dataset download required.
# Educational demo only; not a production spam filter.
texts = [
    "Congratulations you won a free prize claim now",
    "Claim your cash reward now click this link",
    "Urgent you have won a free vacation",
    "Free entry in our contest text WIN now",
    "You have been selected for a cash prize",
    "Get cheap loans instantly call now",
    "Limited offer buy now and get free gifts",
    "Winner claim your reward by calling this number",
    "Earn money fast from home click here",
    "Your account won a bonus claim immediately",
    "Hey are we still meeting for lunch today",
    "Can you call me when you reach home",
    "Please send me the notes from class",
    "Thanks for helping me with the assignment",
    "I will be late for the meeting today",
    "Are you coming to cricket practice tomorrow",
    "Your package will arrive this afternoon",
    "Let's catch up over coffee this weekend",
    "I have shared the project document with you",
    "Please remember to bring your laptop",
    "The lecture starts at ten in the morning",
    "Can we reschedule our call for tomorrow",
    "I am on my way to the college",
    "Happy birthday hope you have a great day",
]
labels = ["spam"] * 10 + ["ham"] * 14
model = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1, 2), lowercase=True)),
    ("classifier", LogisticRegression(max_iter=1000, random_state=42)),
])
model.fit(texts, labels)

REQUESTS = Counter(
    "model_http_requests_total", "HTTP requests handled by the API",
    ["method", "endpoint", "status"],
)
LATENCY = Histogram(
    "model_http_request_duration_seconds", "HTTP request duration in seconds",
    ["method", "endpoint"],
    buckets=(0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1, 2.5, 5),
)
PREDICTIONS = Counter(
    "model_predictions_total", "Successful predictions by class", ["predicted_class"]
)
PREDICTION_ERRORS = Counter(
    "model_prediction_errors_total", "Prediction errors by type", ["error_type"]
)
CONFIDENCE = Histogram(
    "model_prediction_confidence", "Maximum class probability for predictions",
    buckets=(0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0),
)

app.mount("/metrics", make_asgi_app())


class PredictionInput(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    if request.url.path == "/metrics" or request.url.path.startswith("/metrics/"):
        return await call_next(request)
    started = time.perf_counter()
    status = "500"
    try:
        response = await call_next(request)
        status = str(response.status_code)
        return response
    finally:
        elapsed = time.perf_counter() - started
        route = request.scope.get("route")
        endpoint = getattr(route, "path", "unmatched")
        REQUESTS.labels(request.method, endpoint, status).inc()
        LATENCY.labels(request.method, endpoint).observe(elapsed)


@app.get("/")
def root():
    return {"message": "SMS Spam Detection API is running", "docs": "/docs", "metrics": "/metrics"}


@app.get("/health")
def health():
    return {"status": "healthy", "model": "TF-IDF + Logistic Regression"}


@app.post("/predict")
def predict(payload: PredictionInput):
    try:
        probabilities = model.predict_proba([payload.text])[0]
        idx = int(probabilities.argmax())
        predicted_class = str(model.classes_[idx])
        confidence = float(probabilities[idx])
        PREDICTIONS.labels(predicted_class=predicted_class).inc()
        CONFIDENCE.observe(confidence)
        return {
            "text": payload.text,
            "prediction": predicted_class,
            "confidence": round(confidence, 4),
            "model": "TF-IDF + Logistic Regression",
            "note": "Educational demo trained on a tiny sample dataset; not for real spam filtering.",
        }
    except Exception as exc:
        PREDICTION_ERRORS.labels(error_type="prediction_failure").inc()
        raise HTTPException(status_code=500, detail="Prediction failed") from exc
