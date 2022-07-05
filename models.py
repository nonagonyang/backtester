"""Models for Python-Trader app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()
db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class Stock(db.Model):
    """Stock"""
    __tablename__="stocks"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    symbol=db.Column(db.Text, nullable=False)
    name=db.Column(db.Text, nullable=False)
    exchange=db.Column(db.Text, nullable=False)
    shortable=db.Column(db.Boolean,nullable=True)
    prices=db.relationship("StockPrice",backref="stock")

class StockPrice(db.Model): 
    """StockPrice"""
    __tablename__="stockprices"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    stock_id=db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    date=db.Column(db.DateTime, nullable=False)
    open=db.Column(db.Float, nullable=False)
    high=db.Column(db.Float, nullable=False)
    low=db.Column(db.Float, nullable=False)
    close=db.Column(db.Float, nullable=False)
    volume=db.Column(db.Integer,nullable=False)
    

class Strategy(db.Model):
    """Strategy"""
    __tablename__="strategies"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    name=db.Column(db.Text, nullable=False)
    

class Backtest(db.Model):
    """Backtest"""
    __tablename__="backtests"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    stock_id=db.Column(db.Integer, db.ForeignKey('stocks.id'), nullable=False)
    strategy_id=db.Column(db.Integer, db.ForeignKey('strategies.id'),nullable=False)
    start_date=db.Column(db.DateTime, nullable=False)
    end_date=db.Column(db.DateTime, nullable=False)
    initial_cash=db.Column(db.Integer,nullable=False)
    result_cash=db.Column(db.Float,nullable=True)
    trading_logs=db.Column(db.Text, nullable=True)
    result=db.Column(db.Text, nullable=True)
    note=db.Column(db.Text, nullable=True)
    strategy=db.relationship('Strategy',backref='backtests',cascade="all, delete")
    stock=db.relationship('Stock',backref='backtests',cascade="all, delete")
    user=db.relationship('User',backref='backtests',cascade="all,delete")



class User(db.Model):
    """User in the system."""

    __tablename__ ="users"

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.Text,nullable=False,unique=True)
    username = db.Column(db.Text,nullable=False,unique=True)
    password = db.Column(db.Text,nullable=False)

    @classmethod
    def signup(cls, username, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
        )
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


