from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()


class Category(db.Model):
    c_id= db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    description=db.Column(db.String(300),nullable=False)
    products=db.relationship("Product",backref="section",secondary='association',cascade="all, delete", passive_deletes=True)

    def __repr__(self):
        return f"<Category {self.name}>"

class Product(db.Model):
    p_id= db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    manufacture_date = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.String(100), nullable=False)
    rate_per_unit = db.Column(db.Float(), nullable=False)
    unit=db.Column(db.Integer(),nullable=False)


    def __repr__(self):
        return f"<Product {self.name}>"

class Association(db.Model):
    Category_id=db.Column(db.Integer(), db.ForeignKey("category.c_id"), primary_key=True)
    Product_id = db.Column(db.Integer(), db.ForeignKey("product.p_id"), primary_key=True)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

class Cart(db.Model):
    p_id=db.Column(db.Integer(),primary_key=True)
    p_name=db.Column(db.String(50),nullable=False)
    quantity=db.Column(db.Integer(),nullable=False)
    price=db.Column(db.Float(),nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"), nullable=False)


class Orders(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(50),nullable=False)
    quantity=db.Column(db.Integer(),nullable=False)
    price=db.Column(db.Float(),nullable=False)
    user_id=db.Column(db.Integer(),db.ForeignKey("user.id"),nullable=False)