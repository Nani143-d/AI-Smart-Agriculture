import re


def ask_agriculture_ai(question, conversation_history=None):
    """
    Free rule-based agriculture chatbot.
    Does not require an API key or internet connection.
    """

    if not question or not question.strip():
        return "Please enter your farming question."

    message = question.lower().strip()
    message = re.sub(r"\s+", " ", message)

    # Greetings
    if any(word in message for word in [
        "hello", "hi", "hey", "good morning", "good evening"
    ]):
        return (
            "Hello! 🌱 Welcome to AgriAI Assistant.\n\n"
            "I can help you with:\n"
            "🌾 Crop recommendations\n"
            "🦠 Plant diseases\n"
            "💧 Irrigation\n"
            "🌿 Fertilizers\n"
            "🌦️ Weather-related farming tips\n"
            "🌱 Soil health\n\n"
            "What would you like to know?"
        )

    # Crop recommendations
    if any(word in message for word in [
        "which crop", "best crop", "crop recommendation",
        "recommend crop", "grow which", "suitable crop"
    ]):
        return (
            "🌾 Crop Recommendation\n\n"
            "The best crop depends on your soil, rainfall, "
            "temperature, water availability, and season.\n\n"
            "Examples:\n"
            "• Rice: generally suited to areas with reliable water.\n"
            "• Groundnut: often suitable for well-drained sandy loam soils.\n"
            "• Cotton: needs a suitable warm climate and soil conditions.\n"
            "• Maize: requires appropriate temperatures and water.\n"
            "• Millets: some varieties tolerate relatively dry conditions.\n\n"
            "Tell me your location, soil type, and available water "
            "for more specific guidance."
        )

    # Plant diseases
    if any(word in message for word in [
        "disease", "yellow leaves", "yellow leaf",
        "plant infection", "leaf spots", "fungus", "fungal"
    ]):
        return (
            "🦠 Plant Disease Guidance\n\n"
            "Yellow leaves, spots, wilting, or fungal growth can have "
            "different causes, including pests, disease, nutrient "
            "deficiency, or watering problems.\n\n"
            "What you can do:\n"
            "1. Check both sides of the leaves for pests or spots.\n"
            "2. Inspect the roots and soil moisture.\n"
            "3. Remove severely affected plant material when appropriate.\n"
            "4. Avoid unnecessary pesticide application.\n"
            "5. Ask a local agricultural officer to confirm the cause.\n\n"
            "Which crop is affected, and what symptoms can you see?"
        )

    # Fertilizer
    if any(word in message for word in [
        "fertilizer", "fertiliser", "urea", "npk",
        "nutrient", "manure"
    ]):
        return (
            "🌿 Fertilizer Guidance\n\n"
            "The right fertilizer depends on the crop, soil nutrient "
            "levels, and growth stage.\n\n"
            "Recommendations:\n"
            "• Get a soil test before choosing fertilizer.\n"
            "• Use the recommended nutrient dose for your crop.\n"
            "• Apply compost or well-decomposed organic manure when suitable.\n"
            "• Avoid excessive fertilizer, which can damage crops "
            "and pollute water.\n\n"
            "Tell me your crop name and growth stage for more relevant advice."
        )

    # Irrigation
    if any(word in message for word in [
        "irrigation", "watering", "water my crop",
        "how much water", "water requirement", "drip"
    ]):
        return (
            "💧 Irrigation Guidance\n\n"
            "Water requirements vary with crop, soil, temperature, "
            "rainfall, and growth stage.\n\n"
            "Useful practices:\n"
            "• Check soil moisture before irrigating.\n"
            "• Prefer drip irrigation where suitable and affordable.\n"
            "• Avoid waterlogging and unnecessary overwatering.\n"
            "• Water during cooler hours when practical.\n"
            "• Consider recent rainfall before scheduling irrigation.\n\n"
            "Which crop are you growing, and what type of soil do you have?"
        )

    # Soil health
    if any(word in message for word in [
        "soil", "soil health", "soil pH",
        "sandy soil", "clay soil", "loamy"
    ]):
        return (
            "🌱 Soil Health Guidance\n\n"
            "Healthy soil supports strong roots and better crop growth.\n\n"
            "Suggestions:\n"
            "• Test soil pH and nutrient levels.\n"
            "• Add organic matter where appropriate.\n"
            "• Avoid excessive fertilizer application.\n"
            "• Improve drainage if waterlogging occurs.\n"
            "• Use crop rotation to support soil health.\n\n"
            "Tell me your soil type and crop for more specific suggestions."
        )

    # Weather
    if any(word in message for word in [
        "weather", "rain", "rainfall", "temperature",
        "forecast", "climate"
    ]):
        return (
            "🌦️ Weather and Farming Guidance\n\n"
            "I cannot access live weather forecasts in this free "
            "rule-based version.\n\n"
            "Before farming activities:\n"
            "• Check your local weather forecast.\n"
            "• Avoid spraying pesticides when rain or strong winds "
            "could make it unsafe or ineffective.\n"
            "• Adjust irrigation based on rainfall and soil moisture.\n"
            "• Protect crops when extreme weather warnings are issued.\n\n"
            "Tell me your location and crop for general weather-related "
            "farming guidance."
        )

    # Pest management
    if any(word in message for word in [
        "pest", "insect", "worm", "caterpillar",
        "aphid", "crop damage"
    ]):
        return (
            "🐛 Pest Management Guidance\n\n"
            "1. Inspect the crop regularly for pests and damage.\n"
            "2. Identify the pest before selecting a treatment.\n"
            "3. Use integrated pest management practices where suitable.\n"
            "4. Encourage beneficial insects when possible.\n"
            "5. Follow local agricultural recommendations and product labels.\n\n"
            "Which crop is affected, and what insect or damage do you see?"
        )

    # Crop yield
    if any(word in message for word in [
        "yield", "production", "increase harvest",
        "crop growth", "low harvest"
    ]):
        return (
            "📈 Crop Yield Improvement\n\n"
            "To support better crop yields:\n"
            "• Select a variety suited to your region.\n"
            "• Plant at the recommended time and spacing.\n"
            "• Maintain suitable soil nutrients and moisture.\n"
            "• Monitor weeds, pests, and diseases.\n"
            "• Use quality seeds from a reliable source.\n\n"
            "Which crop are you growing, and what problem are you facing?"
        )

    # Thanks
    if any(word in message for word in [
        "thank you", "thanks", "thank u"
    ]):
        return (
            "You're welcome! 🌱\n"
            "I'm happy to help with your farming questions."
        )

    # Default response
    return (
        "🌱 I'm your AgriAI Farming Assistant.\n\n"
        "I can currently help with:\n"
        "• Crop recommendations\n"
        "• Plant diseases\n"
        "• Fertilizers and nutrients\n"
        "• Irrigation and watering\n"
        "• Soil health\n"
        "• Weather-related farming tips\n"
        "• Pest management\n"
        "• Crop yield improvement\n\n"
        "Please ask a more specific question, such as:\n"
        "\"Which fertilizer is suitable for rice?\"\n"
        "\"Why are my plant leaves turning yellow?\"\n"
        "\"How can I improve crop yield?\""
    )