from market import db, app, login_manage, bcrypt
from flask_login import UserMixin


@login_manage.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    user = db.Column(db.String(length=30), nullable=False, unique=True)
    email = db.Column(db.String(length=60), nullable=False, unique=True)
    pass_hash = db.Column(db.String(length=60), nullable=False)
    budget = db.Column(db.Integer(), default=1000, nullable=False)
    items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)) >= 4:
            return f'{str(self.budget)[:-3]},{str(self.budget)[-3:]}$'
        else:
            return f"{self.budget}$"

    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_pass):
        self.pass_hash = bcrypt.generate_password_hash(plain_text_pass).decode('utf-8')

    def check_password(self, user_pass):
        return bcrypt.check_password_hash(self.pass_hash, user_pass)

    def can_purchase(self, item_obj):
        return self.budget >= item_obj.price

    def can_sell(self, item_obj):
        return item_obj in self.items


class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(length=30), nullable=False, unique=True)
    barcode = db.Column(db.String(length=12), nullable=False, unique=True)
    price = db.Column(db.Integer(), nullable=False)
    description = db.Column(db.String(length=1024), nullable=False, unique=True)
    owner = db.Column(db.Integer(), db.ForeignKey('user.id'))

    def __repr__(self):
        return f'Item [{self.id}, {self.name}, {self.barcode}, {self.price}, {self.description}]'

    def budget_change(self, item_obj):
        self.owner = item_obj.id
        item_obj.budget -= self.price
        db.session.commit()

    def sell(self, item_obj):
        self.owner = None
        item_obj.budget += self.price
        db.session.commit()