import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Function '{func.__name__}' took {execution_time:.4f} seconds to execute.")
        return result
    return wrapper

@timer
def process_heavy_data(n):
    return sum(i * i for i in range(n))


# User Session
current_user = {
    "username": "alice_dev",
    "is_authenticated": True,
    "role": "admin"
}

def require_admin(func):
    def wrapper(*args, **kwargs):
        if not current_user["is_authenticated"]:
            raise PermissionError("Authentication required.")
        if current_user["role"] != "admin":
            print(f"[SECURITY ALERT] User '{current_user['username']}' denied access to '{func.__name__}")
            return None
        return func(*args,**kwargs)
    return wrapper



@require_admin
def delete_user_account(user_id):
    print(f"[SUCCESS] Account {user_id} has been permanently deleted.")




if __name__ == "__main__":
    delete_user_account(42)
    total = process_heavy_data(10_000_000)
    print(f"Result: {total}")

