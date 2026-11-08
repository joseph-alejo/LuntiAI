"""Complete, class-specific explanations shared by the API and course notebook."""
import numpy as np

FEATURE_NAMES = ["N", "P", "K", "temperature", "humidity", "ph", "rainfall", "OM"]


def explain_prediction(explainer, features, probabilities, class_names, predicted_index):
    features = np.asarray(features, dtype=float)
    probabilities = np.asarray(probabilities, dtype=float)
    if features.shape != (1, len(FEATURE_NAMES)) or not np.isfinite(features).all():
        raise ValueError("Expected one finite, eight-feature input")
    if probabilities.shape != (len(class_names),) or not np.isfinite(probabilities).all():
        raise ValueError("Class probabilities and names do not match")
    if len(class_names) < 2 or predicted_index != int(np.argmax(probabilities)):
        raise ValueError("Explanation class must match the selected prediction")

    values = explainer.shap_values(features)
    if isinstance(values, list):
        values = np.stack(values, axis=-1)
    values = np.asarray(values, dtype=float)
    base = np.asarray(explainer.expected_value, dtype=float)
    if values.shape != (1, len(FEATURE_NAMES), len(class_names)) or base.shape != probabilities.shape:
        raise ValueError("Unexpected multiclass SHAP dimensions")
    reconstructed = base + values[0].sum(axis=0)
    residual = np.abs(reconstructed - probabilities)
    if not np.isfinite(values).all() or not np.isfinite(residual).all() or residual.max() > 1e-5:
        raise ValueError("SHAP does not reconstruct the model probabilities")

    alternative_index = max((i for i in range(len(class_names)) if i != predicted_index),
                            key=lambda i: probabilities[i])
    contributions = [
        {"feature": name, "input_value": float(features[0, i]),
         "value": float(values[0, i, predicted_index]),
         "alternative_value": float(values[0, i, alternative_index]),
         "difference": float(values[0, i, predicted_index] - values[0, i, alternative_index])}
        for i, name in enumerate(FEATURE_NAMES)
    ]
    contributions.sort(key=lambda item: abs(item["value"]), reverse=True)
    # Retain the old summary keys for saved-history consumers; the UI uses every contribution.
    legacy_names = {"temperature": "Temp", "humidity": "Humidity", "ph": "pH", "rainfall": "Rainfall"}
    summary = [{"feature": legacy_names.get(item["feature"], item["feature"]), "value": item["value"]}
               for item in contributions]
    return {
        "method": "TreeSHAP", "scope": "local", "output_space": "probability",
        "feature_perturbation": explainer.feature_perturbation,
        "explained_class": str(class_names[predicted_index]),
        "base_value": float(base[predicted_index]),
        "prediction_value": float(probabilities[predicted_index]),
        "reconstructed_value": float(reconstructed[predicted_index]),
        "max_additivity_error": float(residual.max()),
        "contributions": contributions,
        "alternative": {"class": str(class_names[alternative_index]),
                        "base_value": float(base[alternative_index]),
                        "prediction_value": float(probabilities[alternative_index]),
                        "probability_gap": float(probabilities[predicted_index] - probabilities[alternative_index]),
                        "base_gap": float(base[predicted_index] - base[alternative_index])},
        "top_positive": [item for item in summary if item["value"] > 0][:3],
        "top_negative": [item for item in summary if item["value"] < 0][:3],
    }
