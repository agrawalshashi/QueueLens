import os
from pathlib import Path

import joblib
from flask import Flask, jsonify, render_template, request

from src.model_utils import (
    get_category_options,
    predict_delay_risk,
    validate_model_features,
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "queuelens_model.joblib"

app = Flask(__name__)
app.config["JSON_SORT_KEYS"] = False

# The model file is created in the research notebook and copied into models/.
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Trained model not found: {MODEL_PATH}\n"
        "Save your trained notebook pipeline as models/queuelens_model.joblib."
    )

model = joblib.load(MODEL_PATH)
validate_model_features(model)

# Use the threshold selected after evaluating precision/recall in the notebook.
# Default is 0.50; change QUEUELENS_THRESHOLD if your analysis supports another value.
THRESHOLD = float(os.getenv("QUEUELENS_THRESHOLD", "0.50"))


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "project": "QueueLens",
        "model_loaded": model is not None,
        "threshold": THRESHOLD,
    })


@app.route("/api/options", methods=["GET"])
def options():
    try:
        return jsonify(get_category_options(model))
    except (KeyError, AttributeError, ValueError) as exc:
        app.logger.exception("Could not read model categories")
        return jsonify({"error": f"Could not load dropdown options: {exc}"}), 500


@app.route("/api/predict", methods=["POST"])
def predict():
    payload = request.get_json(silent=True)

    if not isinstance(payload, dict):
        return jsonify({"error": "Send the input as a JSON object."}), 400

    # Support created_hours alias for backward compatibility
    if "created_hour" not in payload and "created_hours" in payload:
        payload["created_hour"] = payload["created_hours"]

    required = [
        "agency", "complaint_type", "borough",
        "created_hour", "created_day", "created_month",
    ]
    missing = [key for key in required if key not in payload or payload[key] in (None, "")]
    if missing:
        return jsonify({
            "error": "Please provide all required fields.",
            "missing_fields": missing,
        }), 400

    try:
        result = predict_delay_risk(model, payload, threshold=THRESHOLD)
        return jsonify(result)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Prediction failed. Check the server terminal for details."
        }), 500


if __name__ == "__main__":
    # Local development only. Use a production WSGI server when deploying.
    app.run(debug=True)
