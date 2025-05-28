import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Function definitions sent to OpenAI for function calling

functions = [
    {
        "name": "update_user_detail",
        "description": "Update a detail (celebrant, venue, date, guest_count, budget) for a user",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User ID"},
                "field": {
                    "type": "string",
                    "enum": ["celebrant", "venue", "date", "guest_count", "budget"],
                    "description": "Field to update",
                },
                "value": {"type": "string", "description": "New value for the field"},
            },
            "required": ["user_id", "field", "value"],
        },
    },
    {
        "name": "get_user_detail",
        "description": "Retrieve a detail (celebrant, venue, date, guest_count, budget) for a user",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {"type": "string", "description": "User ID"},
                "field": {
                    "type": "string",
                    "enum": ["celebrant", "venue", "date", "guest_count", "budget"],
                    "description": "Field to retrieve",
                },
            },
            "required": ["user_id", "field"],
        },
    },
]


def chat_completion(messages, functions):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    return response
