from users_data import users_data

def build_system_prompt(user_id: str) -> str:
    # Load user details into system prompt for personalized context
    valid_users = list(users_data.keys())
    if user_id in users_data:
        details = users_data[user_id]
        details_text = ", ".join([f"{k}: {v}" for k, v in details.items()])
        return f"""
        You are a friendly wedding assistant 'Wedlii'. 
        CURRENT USER ID: {user_id}  # Explicitly highlight the user_id
        CURRENT USER DETAILS are: {details_text}.
        ALWAYS use the CURRENT USER ID ({user_id}) when making function calls
        Respond in a warm, helpful tone, modern slang, and must be Human-Like respond.
        """
    else:
        return f"""
        You are a friendly wedding assistant bot. 
        Valid user IDs: {valid_users}.
        Please specify a valid user ID to proceed.
        """

def fallback_message():
    return "Let me check that for you!"
