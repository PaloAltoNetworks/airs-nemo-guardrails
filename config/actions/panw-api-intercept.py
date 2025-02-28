import os
import json
import requests
from nemoguardrails.actions import action

# Add this at the beginning of the file
DEBUG_LOGS = []

API_INTERCEPT_URL = "https://service.api.aisecurity.paloaltonetworks.com/v1/scan/sync/request"
AIRS_API_KEY = os.environ.get("AIRS_API_KEY")  # AIRS API Intercept key from env
SECURITY_PROFILE = "dev-block-all-profile"     # Your security profile

@action(name="CallAPIInterceptAction")
async def call_api_intercept(prompt: str, events: list, context: dict, config: dict):
    """
    Custom action to call the API Intercept endpoint.
    Sends the prompt to the API and returns a summary result.
    """
    # Get message from events if prompt is empty
    if not prompt or prompt == "No message found":
        for event in reversed(events):
            if event["type"] == "user_message":
                prompt = event["text"]
                break
        else:
            raise ValueError("No user message found in events")

    print(f"✅ Scanning message: '{prompt}'")

    payload = {
        "tr_id": context.get("transaction_id", "default_id"),
        "ai_profile": {"profile_name": SECURITY_PROFILE},
        "metadata": {
            "app_name": config.app_name if hasattr(config, "app_name") else os.environ.get("APP_NAME", "DemoApp"),
            "app_user": context.get("user_id", "anonymous"),
            "ai_model": context.get("model_name") or (
                config.models[0].model  # Get first model from config
                if config.models
                else "default-model"
            )
        },
        "contents": [{
            "prompt": prompt,
            "response": "N/A"
        }]
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "x-pan-token": AIRS_API_KEY
    }
    try:
        # Add request debugging
        print(f"Sending to API Intercept:\n{json.dumps(payload, indent=2)}")
        DEBUG_LOGS.append(f"Sending to API Intercept:\n{json.dumps(payload, indent=2)}")

        response = requests.post(API_INTERCEPT_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        result = response.json()
        print(f"API Intercept response:\n{json.dumps(result, indent=2)}")  # Debug response
        DEBUG_LOGS.append(f"API Intercept response:\n{json.dumps(result, indent=2)}")

        # Verify the expected block condition
        if result.get("action").lower() in ["block", "deny"]:
            return f"Threat Detected: {result.get('category', 'unknown')}"
        else:
            return "No Threat Detected"

    except requests.HTTPError as e:
        print(f"API Error: {e}\nResponse: {e.response.text}")  # Detailed error
        DEBUG_LOGS.append(f"API Error: {e}\nResponse: {e.response.text}")
        return f"API Error: {e.response.status_code}"
    except Exception as e:
        print(f"Unexpected error: {str(e)}")  # General error logging
        DEBUG_LOGS.append(f"Unexpected error: {str(e)}")
        return f"Error calling API Intercept: {e}"
