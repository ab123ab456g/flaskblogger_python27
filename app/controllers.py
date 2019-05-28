from app.models import *


import hashlib 

m = hashlib.sha256()



class Register:
    @staticmethod
    def mail_not_exist(mail):
        if User.queryOneMail(mail) == None:
            return True
        return False

    @staticmethod
    def username_not_exist(name):
        if User.queryOneName(name) == None:
            return True
        return False

    @staticmethod
    def register(name, mail, password):
        if Register.username_not_exist(name):
            if Register.mail_not_exist(mail):
                password_hash = hashlib.sha256(password).hexdigest()
                User.insert(name,mail,password_hash)
                return True
        return False

class PostIt:
    @staticmethod
    def public(title, content, tags, author):
        if PostIt.checkPermission(author):
            post = Post.insert(title=title, content=content, tags=tags, author=author)
            return True
        return False

    @staticmethod
    def save(title, content, tags, author):
        if PostIt.checkPermission(author):
            tmep = TempPost.insert(title=title, content=content, tags=tags, author=author)
            return True
        return False

    @staticmethod
    def edit():
        pass

    @staticmethod
    def delete():
        pass

    @staticmethod
    def temp_edit():
        pass

    @staticmethod
    def temp_delete():
        pass

    @staticmethod
    def get(id):
        return Post.queryOneid(id=id)

    @staticmethod
    def get_all():
        return Post.queryAll()

    @staticmethod
    def temp_get():
        return TempPost.queryOneid(id=id)

    @staticmethod
    def checkPermission(name):
        if User.queryOneName(name).permission == 1:
            return True
        return False

class Login:

    @staticmethod
    def isLogin(name, password):
        if Login.checkUsername(name):
            if Login.checkPw(name, password):
                return True
        return False

    @staticmethod
    def checkPw(name, password):
        password_hash = hashlib.sha256(password).hexdigest()
        if User.queryOneName(name).password == password_hash:
            return True
        return False

    @staticmethod
    def checkUsername(name):
        user = User.queryOneName(name)
        if user:
            if user.name == name:
                return True
        return False