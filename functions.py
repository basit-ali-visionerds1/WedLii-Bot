from users_data import users_data, save_users

def update_user_detail(user_id: str, field: str, value):
    if user_id not in users_data:
        return {"error": f"User {user_id} not found."}
    if field not in users_data[user_id]:
        return {"error": f"Field '{field}' not recognized."}

    # For guest_count and budget, convert to int if possible
    if field in ("guest_count", "budget"):
        try:
            value = int(value)
        except ValueError:
            return {"error": f"Invalid value for {field}. Must be a number."}

    users_data[user_id][field] = value
    save_users(users_data)  # Persist to JSON
    return {"message": f"{field} updated to {value} for user {user_id}."}


def get_user_detail(user_id: str, field: str):
    if user_id not in users_data:
        return {"error": f"User {user_id} not found."}
    if field not in users_data[user_id]:
        return {"error": f"Field '{field}' not recognized."}

    return {field: users_data[user_id][field]}
