# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from utils import build_system_prompt, fallback_message
from openai_client import chat_completion, functions
from functions import update_user_detail, get_user_detail
from users_data import users_data

import json

app = FastAPI(title="Wedding Bot")

class ChatRequest(BaseModel):
    user_id: str
    message: str



@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    user_id = request.user_id
    user_msg = request.message

    system_prompt = build_system_prompt(user_id)
    print("---------------------\n", system_prompt)

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_msg},
    ]

    # First call to OpenAI to get response or function call
    try:
        response = chat_completion(messages, functions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    message = response.choices[0].message
    # print("-----------", message)

    # Check if OpenAI wants to call a function
    if message.function_call is not None:
        func_name = message.function_call.name
        arguments_str = message.function_call.arguments
        # print("\nFunction name", func_name)
        # print("\n\nRaw arguments:", arguments_str)
        try:
            arguments = json.loads(arguments_str)
        except json.JSONDecodeError:
            return {"reply": fallback_message()}
        

        valid_user_ids = list(users_data.keys())
        if arguments.get("user_id") not in valid_user_ids:
            return {"reply": f"Invalid user ID. Valid options: {valid_user_ids}"}

        # Call respective function and get result
        if func_name == "update_user_detail":
            result = update_user_detail(
                arguments["user_id"], arguments["field"], arguments["value"]
            )
        elif func_name == "get_user_detail":
            result = get_user_detail(
                arguments["user_id"], arguments["field"]
            )
        else:
            return {"reply": fallback_message()}

        # Append function result to messages and ask OpenAI to finalize reply
        messages.append(message)  # assistant message with function call
        messages.append(
            {"role": "function", "name": func_name, "content": json.dumps(result)}
        )

        # Call OpenAI again to get final user-friendly reply
        try:
            final_response = chat_completion(messages, functions)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        final_msg = final_response.choices[0].message.content
        return {"reply": final_msg}

    else:
        # No function call, just reply normally or fallback if empty
        reply = message.content or fallback_message()
        return {"reply": reply}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)