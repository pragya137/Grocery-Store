from flask import Flask, render_template,request,redirect,flash,session,jsonify,request,session
from flask_cors import CORS



from model import *

from resources import *

app = Flask(__name__)
app.secret_key = "super secret key"

#======================= Configuration =======================

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///manymanydata.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS(app)
api.init_app(app)
db.init_app(app)
app.app_context().push()



#======================= Controller ==========================

@app.route('/',methods=['GET','POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = user.username
            return redirect('/user_home_page')

        flash('Invalid username or password', 'error')
    return render_template('login.html')



@app.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash("Username already taken. Please choose a different username.")
            return render_template('signup.html')
        else:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            flash("Registration Done!!")
            return redirect('/')
    return render_template('signup.html')


@app.route('/admin_login',methods=['GET','POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user.username == "pragyasingh" and user.password == password:
            session['username'] = user.username
            return redirect('/homepage_admin')

        flash('Invalid username or password', 'error')
    return render_template('admin_login.html')

@app.route('/logout',methods=['GET','POST'])
def logout():
    session.pop('username', None)
    return redirect('/')

#=======================================Admin====================================



@app.route('/homepage_admin', methods = ['GET','POST'])
def homepage_admin():
    if session.get('username') == 'pragyasingh':
         categories = Category.query.all()
         return render_template('homepage_admin.html', categories = categories)
    else:
        flash('Invalid User !!')
        return redirect('/')


@app.route('/add_category', methods =["GET","POST"])
def add_category():
    if session.get('username') == 'pragyasingh':
        if request.method == "GET":
            return render_template('add_cate_form.html')
        if request.method == "POST":
            c_name= request.form.get('c_name')
            c_description=request.form.get('c_description')
            c1= Category(name=c_name,description=c_description)
            db.session.add(c1)
            db.session.commit()
            return redirect('/homepage_admin')
    else:
        flash('Invalid User !!')
        return redirect('/')

@app.route('/all_products', methods = ['GET','POST'])
def all_products():
    if session.get('username') == 'pragyasingh':
        products = Product.query.all()
        return render_template('all_product.html', products = products)
    else:
        flash('Invalid User !!')
        return redirect('/')

@app.route('/add_product', methods =["GET","POST"])
def add_product():
    if session.get('username') == 'pragyasingh':
        if request.method == "GET":
            categories=Category.query.all()
            return render_template('add_prod_form.html',categories=categories)
        if request.method == "POST":
            p_name = request.form.get('p_name')
            manufacture = request.form.get('manufacture')
            expiry = request.form.get('expiry')
            rate = request.form.get('rate')
            c_id = request.form.get('c_id')
            unit=request.form.get('unit')
            category=Category.query.get(int(c_id))
            p1= Product(name=p_name,manufacture_date= manufacture,expiry_date=expiry,rate_per_unit=rate,unit=unit)
            db.session.add(p1)
            p1.section.append(category)
            db.session.commit()
            return redirect('/all_products')
    else:
        flash('Invalid User !!')
        return redirect('/')



@app.route("/see_products/<int:id>", methods =["GET","POST"])
def see_products(id):
    if session.get('username') == 'pragyasingh':
        c1=Category.query.get(id)
        products= c1.products
        return render_template("cate_prod.html",c1=c1,products=products)
    else:
        flash('Invalid User !!')
        return redirect('/')


@app.route("/update_cate/<int:id>",methods = ["GET","POST"])
def update_cate(id):
    if session.get('username') == 'pragyasingh':
        if request.method == "POST":
            c1=Category.query.get(id)
            name= request.form.get('new_name')
            description=request.form.get('new_description')
            c1.name=name
            c1.description=description
            db.session.add(c1)
            db.session.commit()
            return redirect("/homepage_admin")
        return render_template("update_cate.html", id=id)
    else:
        flash('Invalid User !!')
        return redirect('/')


@app.route("/delete_cate/<int:id>")
def delete_cate(id):
    if session.get('username') == 'pragyasingh':
        c1=Category.query.get(id)
        for product in c1.products:
            db.session.delete(product)
        db.session.delete(c1)
        db.session.commit()
        return redirect('/homepage_admin')
    else:
        flash('Invalid User !!')
        return redirect('/')



@app.route("/update_prod/<int:id>", methods=["GET", "POST"])
def update_prod(id):
    if session.get('username') == 'pragyasingh':
        categories = Category.query.all()
        if request.method == "POST":
            p1 = Product.query.get(id)
            name = request.form.get('new_name')
            manufacture_date = request.form.get('new_manufacture_date')
            expiry_date = request.form.get('new_expiry_date')
            rate_per_unit = request.form.get('new_rate')
            c_id = request.form.get('c_id')
            units = request.form.get('units')
            category = Category.query.get(int(c_id))
            p1.name = name
            p1.manufacture_date = manufacture_date
            p1.expiry_date = expiry_date
            p1.rate_per_unit = rate_per_unit
            p1.unit = units
            p1.section.append(category)
            db.session.commit()
            return redirect("/all_products")
        return render_template("update_prod.html", id=id, categories=categories)
    else:
        flash('Invalid User !!')
        return redirect('/')


@app.route("/delete_prod/<int:id>")
def delete_prod(id):
    if session.get('username') == 'pragyasingh':
        p1=Product.query.get(id)
        db.session.delete(p1)
        db.session.commit()
        return redirect('/all_products')
    else:
        flash('Invalid User !!')
        return redirect('/')


@app.route("/search",methods=["GET","POST"])
def search():
    if session.get('username') == 'pragyasingh':
        if request.method == "POST":
            search_query = request.form.get('search_query')
            search_option = request.form.get('search_option')
        if search_query:
            if search_option == 'category':
                n2=request.form.get('search_query')
                c1 = Category.query.filter_by(name=n2).first()
                if c1:
                    prod = c1.products
                    return render_template('prod_in_this_cate.html', category=c1, products=prod)
                else:
                    return render_template('no_category.html')
            elif search_option == 'product':
                n1 = request.form.get('search_query')
                p1 = Product.query.filter_by(name=n1).all()
                return render_template('prod.html',products=p1)
    else:
        flash('Invalid User !!')
        return redirect('/')




#================================User=============================





@app.route('/user_home_page',methods=['GET','POST'])
def user_home_page():
    if 'username' in session:
        name=session.get('username')
        user=User.query.filter_by(username=name).first()
        categories = Category.query.all()
        return render_template('all_cate_user.html', categories=categories,user=user)
    else:
        flash('Invalid User !!')
        return redirect('/')

@app.route('/user_prod_page',methods=['GET','POST'])
def user_prod_page():
    if 'username' in session:
        name = session.get('username')
        user = User.query.filter_by(username=name).first()
        products = Product.query.all()
        return render_template('all_prod_user.html', products=products,user=user)
    else:
        flash('Invalid User !!')
        return redirect('/')

@app.route("/see_product_user/<int:id>", methods =["GET","POST"])
def see_product_user(id):
    if 'username' in session:
        name = session.get('username')
        user = User.query.filter_by(username=name).first()
        category=Category.query.get(id)
        products= category.products
        return render_template("cate_prod_user.html",category=category,products=products,user=user)
    else:
        flash('Invalid User !!')
        return redirect('/')

@app.route("/search_user", methods=["GET", "POST"])
def search_user():
    if 'username' in session:
        name = session.get('username')
        user = User.query.filter_by(username=name).first()
        if request.method == "POST":
            search_query = request.form.get('search_query')
            search_option = request.form.get('search_option')
            if search_query:
                if search_option == 'category':
                    name = request.form.get('search_query')
                    c1 = Category.query.filter_by(name=name).first()
                    if c1:
                        prod = c1.products
                        return render_template('prod_in_this_cate_user.html', category=c1, products=prod,user=user)
                    else:
                        return render_template('no_category_user.html',user=user)
                elif search_option == 'product':
                    n1 = request.form.get('search_query')
                    p1 = Product.query.filter_by(name=n1).all()
                    return render_template('prod_user.html', products=p1,user=user)
    else:
        flash('Invalid User !!')
        return redirect('/')


@app.route('/add_to_cart/<int:id>',methods=['GET','POST'])
def add_to_cart(id):
    if 'username' in session:
        name = session.get("username")
        user = User.query.filter_by(username=name).first()
        if user:
            product = Product.query.get(id)
            if product:
                if request.method == 'POST':
                    requested_quantity = int(request.form.get('quantity'))
                    if requested_quantity <= product.unit:
                        cart_item = Cart(p_name=product.name,quantity=requested_quantity,price=product.rate_per_unit,user_id=user.id)
                        db.session.add(cart_item)
                        db.session.commit()
                        return redirect('/cart')
                    else:
                        flash('Quantity exceeds available units.')
                        return render_template('quantity.html', id1=id, user=user)

                elif request.method == 'GET':
                    return render_template('quantity.html', id1=id,user=user)

    else:
        flash('Invalid User !!')
        return redirect('/')



@app.route('/cart')
def cart():
    if 'username' in session:
        username = session.get("username")
        user = User.query.filter_by(username=username).first()
        if user:
            cart_items = Cart.query.filter_by(user_id=user.id).all()
            return render_template('cart.html', cart=cart_items,user=user)
        else:
            flash('Invalid User !!')
            return redirect('/')
    else:
        flash('Invalid User !!')
        return redirect('/')


@app.route("/remove_prod/<int:id>",methods=['GET','POST'])
def remove_prod(id):
    if 'username' in session:
        cart_item = Cart.query.get(id)
        if cart_item:
            db.session.delete(cart_item)
            db.session.commit()
            return redirect('/cart')
        else:
            flash('Product not found in the cart.')
            return redirect('/cart')
    else:
        flash('Invalid User !!')
        return redirect('/')

@app.route('/buy_prod',methods=['GET','POST'])
def buy_prod():
    if 'username' in session:
        username = session.get("username")
        user = User.query.filter_by(username=username).first()
        c1=Cart.query.filter_by(user_id=user.id).all()
        total_price = sum(item.price* item.quantity for item in c1)
        return render_template('buy_prod.html',cart=c1,total_price=total_price,user=user)
    else:
        flash('Invalid User !!')
        return redirect('/')
@app.route('/address',methods=['GET','POST'])
def address():
    if 'username' in session:
        username = session.get("username")
        user = User.query.filter_by(username=username).first()
        if request.method == "POST":
            return redirect('/buy_prod')
        else:
            return render_template('address.html',user=user)
    else:
        flash('Invalid User !!')
        return redirect('/')

@app.route('/order_place',methods=['GET','POST'])
def order_place():
    if 'username' in session:
        username = session.get("username")
        user = User.query.filter_by(username=username).first()

        if user:
            cart_items = Cart.query.filter_by(user_id=user.id).all()

            if cart_items:
                for cart_item in cart_items:
                    name=cart_item.p_name
                    quantity=cart_item.quantity
                    price=cart_item.price
                    id=user.id
                    p1=Orders(name=name,quantity=quantity,price=price,user_id=id)
                    db.session.add(p1)
                    db.session.commit()
                for cart_item in cart_items:
                    product = Product.query.filter_by(name=cart_item.p_name).first()
                    if product and product.unit >= cart_item.quantity:
                        product.unit = product.unit - cart_item.quantity
                        db.session.add(product)
                        db.session.commit()
                for cart_item in cart_items:
                    db.session.delete(cart_item)
                db.session.commit()
                name = session.get("username")
                user1 = User.query.filter_by(username=name).first()
                return render_template('order_successful.html',user1=user1)
            else:
                flash("Your cart is empty. Add some products before placing an order.")
                return redirect('/cart')
        else:
            flash('Invalid User !!')
            return redirect('/')
    else:
        flash('Invalid User !!')
        return redirect('/')



@app.route('/my_profile/<int:id>',methods=['GET','POST'])
def my_profile(id):
    if 'username' in session:
        username=session.get('username')
        user = User.query.filter_by(username=username).first()
        items=Orders.query.filter_by(user_id=id).all()
        return render_template('My_profile.html',name=username,items=items,user=user)
    else:
        flash('Invalid User !!')
        return redirect('/')





if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
















