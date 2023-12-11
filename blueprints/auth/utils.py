import uuid

def generate_password_reset_token():
    """
    Generates a password reset token for the user with the given email.
    """
    token = str(uuid.uuid4())
    
    return token
