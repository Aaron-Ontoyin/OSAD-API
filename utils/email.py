def send_email(recipient, subject, message):
    """
    Sends an email to the recipient with the subject and message
    """
    # TODO: Implement logic
    with open("reset_password_token.txt", "w") as f:
        f.write(message)

    return
