from __future__ import annotations

import pandas as pd


CATEGORICAL_FEATURES = ["agency", "complaint_type", "borough"]
NUMERIC_FEATURES = ["created_hour", "created_day", "created_month"]
ALL_FEATURES = CATEGORICAL_FEATURES + NUMERIC_FEATURES


def validate_model_features(model) -> None:
    """Fail early if the saved pipeline does not match the app's expected columns."""
    expected = set(ALL_FEATURES)
    actual = set(getattr(model, "feature_names_in_", []))

    if actual and actual != expected:
        raise ValueError(
            "Saved model features do not match the API. "
            f"Expected {sorted(expected)}, found {sorted(actual)}. "
            "Update the API feature names to match the notebook pipeline."
        )

    if not hasattr(model, "predict_proba"):
        raise ValueError("Saved model must support predict_proba().")


def get_category_options(model) -> dict:
    """Read valid dropdown values from the trained OneHotEncoder."""
    try:
        preprocessor = model.named_steps["preprocessor"]
        encoder = preprocessor.named_transformers_["categorical"]
        categories = encoder.categories_
    except (AttributeError, KeyError) as exc:
        raise ValueError(
            "Could not find the 'preprocessor' step and 'categorical' encoder "
            "inside the saved model. Check the pipeline names in the notebook."
        ) from exc

    options = {}
    for feature, values in zip(CATEGORICAL_FEATURES, categories):
        options[feature] = sorted(
            {str(value) for value in values if pd.notna(value)}
        )

    return {"options": options}


def predict_delay_risk(model, payload: dict, threshold: float = 0.50) -> dict:
    """Validate user input and return the model's estimated long-resolution risk."""
    row = {}

    for feature in CATEGORICAL_FEATURES:
        value = payload.get(feature)
        if not isinstance(value, str) or not value.strip():
            raise ValueError(f"'{feature}' must be a non-empty string.")
        row[feature] = value.strip()

    hour_val = payload.get("created_hour")
    if hour_val is None:
        hour_val = payload.get("created_hours")
    if hour_val is None:
        raise ValueError("'created_hour' must be provided.")

    try:
        hour = int(hour_val)
        day = int(payload["created_day"])
        month = int(payload["created_month"])
    except (KeyError, TypeError, ValueError):
        raise ValueError("Hour, day, and month must be whole numbers.") from None

    if not 0 <= hour <= 23:
        raise ValueError("Hour must be between 0 and 23.")
    if not 1 <= day <= 31:
        raise ValueError("Day must be between 1 and 31.")
    if not 1 <= month <= 12:
        raise ValueError("Month must be between 1 and 12.")

    row["created_hour"] = hour
    row["created_day"] = day
    row["created_month"] = month

    X = pd.DataFrame([row], columns=ALL_FEATURES)
    probabilities = model.predict_proba(X)[0]
    classes = list(model.classes_)

    # The positive class is 1: resolution time greater than seven days.
    if 1 not in classes:
        raise ValueError(
            f"Expected class label 1 for long-resolution requests; found {classes}."
        )

    probability = float(probabilities[classes.index(1)])
    is_high_risk = probability >= threshold

    return {
        "probability": round(probability, 4),
        "probability_percent": round(probability * 100, 1),
        "threshold": round(float(threshold), 4),
        "risk_level": "High" if is_high_risk else "Lower",
        "prediction": int(is_high_risk),
        "message": (
            "The model estimates an elevated chance that this request may take "
            "more than seven days to resolve."
            if is_high_risk else
            "The model estimates a lower chance of this request taking more "
            "than seven days to resolve."
        ),
        "disclaimer": (
            "This is a model estimate based on historical data, not a guarantee "
            "or an official NYC agency prediction."
        ),
    }
