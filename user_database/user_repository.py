from .user_db_model import User

class UserRepository:

    def __init__(self, db):
        self.db = db

    def get_by_email(self, email):
        return self.db.query(User).filter(
            User.email == email
        ).first()

    def add_user(self, user):
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)