from src.common.database import Database
import uuid
from src.models.blog import Blog
from datetime import datetime
from flask import session


class User(object):
    def __init__(self, email, password, _id=None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id


    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {"email": email})

        if data is not None:
            return cls(**data)
        return None


    @classmethod
    def get_by_id(cls, _id):
        data = Database.find_one("users", {"_id": _id})

        if data is not None:
            return cls(**data)

    @staticmethod
    def login_valid(email,password):
        # Ex User.login_valid("robert@me.com", "1234") returns TRUE is email/password combo is correct.
        # check whether a user's email matches the password they sent us
        user = User.get_by_email(email)
        if user is not None:
            # Check the password from the user object in the database against what they entered into the password field
            return user.password == password
        return False

    @classmethod
    def register(cls, email, password):
        user = User.get_by_email(email)
        if user is None:
            # User does not exist, create user
            new_user = cls(email, password)
            new_user.save_to_mongo()
            session['email'] = email
            return True
        else:
            #  User exists
            return False


    @staticmethod
    def login(user_email):
        #login_valid has already been called, now we store their email in the session
        session['email']= user_email

    @staticmethod
    def logout():
        session['email']= None

    def get_blogs(self):
        return Blog.find_by_author_id(self._id)

    def new_blog(self, title, description):
        # author, title, description, author_id
        blog = Blog(author = self.email,
                    title=title,
                    description = description,
                    author_id=self._id)
        blog.save_to_mongo()

    @staticmethod
    def new_post(blog_id, title, content, date=datetime.utcnow()):
        # title, content, author, created_date=datetime.utcnow()
        blog = Blog.from_mongo(blog_id)
        blog.new_post(title= title,
                      content=content,
                      date=date)


    def json(self):
        return{
            "email": self.email,
            "_id": self._id,
            "password": self.password
        }


    def save_to_mongo(self):
        Database.insert("users", self.json())