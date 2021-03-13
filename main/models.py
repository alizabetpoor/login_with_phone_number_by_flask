from main import db,app,login_manager
from itsdangerous import TimedJSONWebSignatureSerializer as serializer
from datetime import datetime
from flask_login import UserMixin
@login_manager.user_loader
def load_user(user_id):
	return User.query.get(int(user_id))
class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(30),unique=True,nullable=False)
    phonenumber=db.Column(db.String(30),unique=True,nullable=False)
    password=db.Column(db.String(80),nullable=False)
    code=db.Column(db.String(10),nullable=True)
    def get_login_token(self,expiretime=120):
        s=serializer(app.config['SECRET_KEY'],expiretime)
        return s.dumps({"user_id":self.id}).decode("utf-8")
    @staticmethod
    def check_token(token):
        s=serializer(app.config['SECRET_KEY'])
        try:
            user_id=s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)