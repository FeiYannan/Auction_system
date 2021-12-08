from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_json(self):        
        return {"name": self.name,
                "email": self.email}

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_id(self):         
        return str(self.id)


