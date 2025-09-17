from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import datetime
from sqlalchemy.orm import relationship

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(120))
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def authenticate(cls, email, password):
        user = cls.query.filter_by(email=email).first()
        if user and user.check_password(password):
            access_token = create_access_token(identity=str(user.id))
            return access_token, user
        return None, None   # <- Fix: explicit return if authentication fails

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("login_info.id"))
    user = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post", lazy="dynamic")

    def to_dic(self):
        return {   # <- Fix: add return
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H-%M-%S"),
        }

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("login_info.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def to_dic(self):
        return {   # <- Fix: add return
            "id": self.id,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H-%M-%S"),
            "author_id": self.user_id,
        }
