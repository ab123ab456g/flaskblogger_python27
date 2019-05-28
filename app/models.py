# -*- coding: UTF-8 -*-

from datetime import datetime
from app import db

#應該進行多載設計

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), unique=True)
    email = db.Column(db.String(128), unique=True)
    permission = db.Column(db.Integer, default=0)
    password = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    posts = db.relationship('Post', backref='user', lazy='dynamic')
    coments = db.relationship('Comment', backref='user', lazy='dynamic')
    temp_posts = db.relationship('TempPost', backref='user', lazy='dynamic')

    def __repr__(self):
       return '<User {0}>'.format(self.name)

    @staticmethod
    def queryOneMail(mail):
       return User.query.filter_by(email=mail).first()

    @staticmethod
    def queryOneName(name):
       return User.query.filter_by(name=name).first()

    @staticmethod
    def queryOneid(id):
       return User.query.filter_by(id=id).first()

    @staticmethod
    def queryAll():
       return User.query.all()

    @staticmethod
    def insert(name, mail, password):
       user = User(name=name, email=mail,password=password)
       db.session.add(user)
       db.session.commit()

    @staticmethod
    def adminInsert(name, mail, password):
       user = User(name=name,email=mail, password=password, permission=1)
       db.session.add(user)
       db.session.commit()

    @staticmethod
    def update(name, password):
       user = User.queryOneName(name)
       user.password = password
       db.session.commit()

    @staticmethod
    def delete(name):
       user = User.queryOneName(name)
       db.session.delete(user)
       db.session.commit()



class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)
    content = db.Column(db.String(128))
    tags = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='post',lazy='dynamic')

    def __repr__(self):
       return '<Post {0}>'.format(self.title)

    @staticmethod
    def queryOnetitle(title):
       return Post.query.filter_by(title=title).first_or_404()

    @staticmethod
    def queryOneid(id):
       return Post.query.filter_by(id=id).first_or_404()

    @staticmethod
    def queryAll():
       return Post.query.all()

    @staticmethod
    def insert(title, content, tags, author):
       user = User.queryOneName(name=author)
       post = Post(title=title, content=content, tags =tags, user=user)
       db.session.add(post)
       db.session.commit()

    @staticmethod
    def update(title, new_title, new_content ,new_tag=None):
       post = Post.queryOnetitle(title)
       post.title = new_title
       post.content = new_content
       if new_tag != None:
         post.tags = new_tag
       db.session.commit()

    @staticmethod
    def delete(title):
       post = Post.queryOnetitle(title)
       db.session.delete(post)
       db.session.commit()

    class post:
      def __init__(self, post):
        self.id = post.id
        self.title = post.title
        self.content = post.content
        self.tags = post.tags
        self.timestamp = post.timestamp
        self.author = post.author.name
        self.comments = post.comments.order_by(db.desc(Comment.id))

class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), index=True, unique=True)
    num = db.Column(db.Integer)

    def __repr__(self):
       return '<Tag {0}>'.format(self.tag_name)

    @staticmethod
    def queryOneid(id):
       return Tag.query.filter_by(id=id).first_or_404()

    @staticmethod
    def queryOneTag(tag):
       return Tag.query.filter_by(tag_name=tag).first_or_404()

    @staticmethod
    def queryAll():
       return Tag.query.all()

    @staticmethod
    def insert(tag):
       tag = Tag(tag_name=tag)
       db.session.add(tag)
       db.session.commit()

    @staticmethod
    def update(tag, new_tag):
       tag = Tag.queryOneTag(tag)
       tag.tag_name = new_tag
       db.session.commit()

    @staticmethod
    def delete(tag):
       tag = Tag.queryOneTag(tag)
       db.session.delete(tag)
       db.session.commit()

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(128))
    post_id = db.Column(db.String(128), db.ForeignKey('post.id'))
    user_id = db.Column(db.String(128), db.ForeignKey('user.id'))
    
    def __repr__(self):
       return '<Comment for {0}>'.format(self.post_id)

    @staticmethod
    def queryOne(post_id,user_id):
       return Comment.query.filter_by(post_id=post_id,user_id=user_id).first_or_404()

    @staticmethod
    def queryOneid(id):
       return Comment.query.filter_by(id=id).first_or_404()

    @staticmethod
    def queryOneTitle(title):
        post = Post.QueryOne(title)
        comments = Comment.query.filter_by(post_id=post.id)
        return comments
    @staticmethod
    def queryAll():
       return Comment.query.all()

    @staticmethod
    def insert(content, name, post):
       post = Post.queryOnetitle(post)
       user = User.queryOneName(name)
       content = Comment(content=content, user=user, post=post)
       db.session.add(content)
       db.session.commit()

    @staticmethod
    def update(content_id, new_content):
       comment = Comment.queryOneid(content_id)
       comment.content = new_content
       db.session.commit()

    @staticmethod
    def delete(id):
       comment = Comment.queryOneid(id)
       db.session.delete(comment)
       db.session.commit()

class TempPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), unique=True)
    content = db.Column(db.String(128))
    tags = db.Column(db.String(128))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id'))

    @staticmethod
    def queryOneid(id):
       return TempPost.query.filter_by(id=id).first_or_404()

    @staticmethod
    def queryOnetitle(title):
       return TempPost.query.filter_by(title=titile).first_or_404()

    @staticmethod
    def queryAll():
       return TempPost.query.all()

    @staticmethod
    def insert(title, content, tag, username):
       user = User.queryOneName(username)
       temp = TempPost(title=title, content=content, tags=tag, user=user)
       db.session.add(temp)
       db.session.commit()

    @staticmethod
    def update(id, new_title, new_content, new_tag=None):
       temp = TempPost.queryOneid(id)
       temp.title = new_title
       temp.content = new_content
       if new_tag != None:
         temp.tags = new_tag
       db.session.commit()

    @staticmethod
    def delete(id):
       temp = TempPost.queryOneid(id)
       db.session.delete(temp)
       db.session.commit()

    def __repr__(self):
       return '<TempPost {0}>'.format(self.title)
