from flask import Blueprint


auth = Blueprint("auth", __name__)


from .routes import (
    register,
    login,
    get_user,
    update_user,
    delete_user,
    change_password,
    get_password_reset_token,
    reset_password,
    logout,
    refresh_token,
    get_all_users,
    make_admin,
)

auth.post("/register")(register)
auth.post("/login")(login)
auth.get("/user")(get_user)
auth.patch("/user")(update_user)
auth.delete("/user")(delete_user)
auth.delete("/logout")(logout)
auth.patch("/change-password")(change_password)
auth.get("/refresh-token")(refresh_token)
auth.get("/password-reset-token")(get_password_reset_token)
auth.patch("/reset-password")(reset_password)
auth.patch("/make-admin")(make_admin)
auth.get("/users")(get_all_users)
