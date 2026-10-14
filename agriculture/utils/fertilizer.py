def recommend_fertilizer(crop, nitrogen, phosphorus, potassium):
    # Educational rule-of-thumb only; values alone are not enough for a safe recommendation.
    low = []
    if nitrogen < 40: low.append("nitrogen (N)")
    if phosphorus < 20: low.append("phosphorus (P)")
    if potassium < 20: low.append("potassium (K)")
    if low:
        suggestion = "Nutrient levels entered are relatively low for this demo rule: " + ", ".join(low) + "."
    else:
        suggestion = "The entered NPK values are above this demo's low-value thresholds."
    return {
        "crop": crop,
        "suggestion": suggestion,
        "message": "Do not apply fertilizer based only on this demo. Get a soil test and follow crop-specific local agricultural guidance for rates and timing."
    }
