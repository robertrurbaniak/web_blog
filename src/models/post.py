import uuid
from src.common.database import Database
from datetime import datetime

class Post(object):

    def __init__(self, blog_id, title, content, author, created_date=datetime.utcnow(), _id=None):
        self.blog_id = blog_id
        self.title = title
        self.content = content
        self.author = author
        self.created_date = created_date
        self._id = uuid.uuid4().hex if _id is None else _id

    def save_to_mongo(self):
        Database.insert(collection='posts', data=self.json())

    def json(self):
        return {
            '_id': self._id,
            'blog_id': self.blog_id,
            'author': self.author,
            'content': self.content,
            'title': self.title,
            'created_date': self.created_date
        }

    @classmethod
    def from_mongo(cls, _id):
        # Ex: Post.from_mongo('123') returns a post with that id
        post_data = Database.find_one(collection='posts', query={'_id':id})

        return cls(**post_data) # for each element in post_data, get the name of the element and say the objects element is equal to that.

    @staticmethod
    def from_blog(id):
        return [post for post in Database.find(collection='posts', query={'blog_id': id})]
