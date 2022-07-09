from app.models.user import User


def authenticated(session):
    return session.get("user")

def check(user_email, permission):
    query = User.query.filter(User.email == user_email).first()
    user_id = query.id
    return User.has_permission(user_id,permission)
