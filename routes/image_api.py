# routes/image_api.py
from flask import Blueprint, request, jsonify
import os

image_bp = Blueprint("image_bp", __name__)

@image_bp.post("/character-image")
def character_image():
    b = request.get_json(silent=True) or {}
    days = int(b.get("days", 0))
    achieved = bool(b.get("isTargetAchieved", False))

    if days >= 60:
        fitness = "a god-like bodybuilder, extremely muscular, full chrome armor, epic lighting"
    elif days >= 30:
        fitness = "a very muscular, toned body, in a heroic pose, dynamic shadows"
    elif days >= 7:
        fitness = "a slightly defined and athletic body, standing confidently"
    else:
        fitness = "a slim, casual person, looking determined"
    env = ("in a luxurious, futuristic marble gym with gold accents"
           if achieved else "in a simple, functional concrete gym")
    prompt = (f"A fantasy warrior character, male, standing {env}, with {fitness}, "
              f"wearing simple training gear, digital art, high detail, no text, clean background. "
              f"The warrior looks determined and proud.")

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return jsonify({"imageBase64": ""}), 200

    try:
        import requests
        url = "https://generativelanguage.googleapis.com/v1beta/models/imagen-3.0-generate-002:predict"
        payload = {"instances": [{"prompt": prompt}], "parameters": {"sampleCount": 1}}
        resp = requests.post(f"{url}?key={api_key}", json=payload, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        b64 = (data.get("predictions") or [{}])[0].get("bytesBase64Encoded","")
        return jsonify({"imageBase64": f"data:image/png;base64,{b64}"}), 200
    except Exception as e:
        return {"error": f"image generation failed: {e}"}, 502
