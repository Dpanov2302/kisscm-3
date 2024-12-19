import json

def parse_json(input_json: str):
    try:
        return json.loads(input_json)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON format: {e}")
