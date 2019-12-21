from extensions.db import db


class User(db.Model):
    user_id = db.Column(db.String(60), primary_key=True)
    token = db.Column(db.String(60), unique=True, index=True)

    @staticmethod
    def find(user_id: str):
        return User.query.filter_by(user_id=user_id).first()

    @staticmethod
    def find_by_token(token: str):
        return User.query.filter_by(token=token).first()
