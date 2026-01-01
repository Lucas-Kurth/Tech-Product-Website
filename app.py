from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'techfinder.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# Session security configuration
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to session cookie
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # CSRF protection
# app.config['SESSION_COOKIE_SECURE'] = True  # Uncomment in production (requires HTTPS)

# Initialize database
db = SQLAlchemy(app)

@app.route("/")
def home():
    from backend.db_utils import get_all_products

    # Fetch all products from database
    products = get_all_products()

    return render_template("index.html", products=products)

# Renders login page
@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/wishlist")
def wishlist():
    from flask import session, redirect, url_for

    # Redirect to login if not authenticated
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template("wishlist.html")

@app.route("/profile")
def profile():
    from flask import session, redirect, url_for

    # Redirect to login if not authenticated
    if 'user_id' not in session:
        return redirect(url_for('login'))

    return render_template("profile.html")

# Backend Logic for login; recieves a json object and
@app.route("/api/login", methods=["POST"])
def api_login():
    from backend.db_utils import authenticate_user
    from flask import session

    data = request.get_json()

    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'success': False, 'error': 'Missing credentials'})

    user = authenticate_user(username, password)

    if user:
        # Store user info in session
        session['user_id'] = user.id
        session['username'] = user.username

        return jsonify({
            'success': True,
            'user_id': user.id,
            'username': user.username
        })
    else:
        return jsonify({
            'success': False,
            'error': 'Invalid username or password'
        }), 401


@app.route("/api/register", methods=['POST'])
def api_register():
    
    from backend.db_utils import create_user

    data = request.get_json()

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not password or not email:
        return jsonify({'success': False, 'error': 'Missing credentials'})
    
    user_data = create_user(username, email, password)

    if user_data:
        return jsonify({
            'success': True,
            'user_id': user_data['id'],
            'username': user_data['username']
        })
    else:
        return jsonify({
            'success': False,
            'error': 'User already exists'
        }), 409
    
@app.route("/api/logout", methods=['POST'])
def api_logout():
    from flask import session

    # Clear the session data
    session.clear()

    return jsonify({
        'success': True,
        'message': 'Logged out successfully'
    })

@app.route("/api/auth/status", methods=['GET'])
def auth_status():
    from flask import session

    if 'user_id' in session:
        return jsonify({
            'authenticated': True,
            'user_id': session['user_id'],
            'username': session['username']
        })
    else:
        return jsonify({
            'authenticated': False
        })


# Product Endpoints
@app.route("/api/products", methods=['GET'])
def get_products():
    from backend.db_utils import get_all_products

    # Get all products from database
    products = get_all_products()

    # Convert each product to a dictionary
    products_list = []
    for product in products:
        products_list.append({
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'price': product.price,
            'description': product.description,
            'image_url': product.image_url,
            'external_link': product.external_link
        })

    return jsonify({
        'success': True,
        'products': products_list,
        'count': len(products_list)
    })
    

@app.route("/api/products/<int:product_id>", methods=['GET'])
def get_product(product_id):
    from backend.db_utils import get_product_by_id

    product = get_product_by_id(product_id)

    if not product:
        return jsonify({
            'success': False,
            'error': 'Product not found'
        }), 404

    return jsonify({
        'success': True,
        'product': {
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'price': product.price,
            'description': product.description,
            'image_url': product.image_url,
            'external_link': product.external_link
        }
    })

@app.route("/api/products/search", methods=['GET'])
def search_products():
    pass

@app.route("/api/products", methods=['POST'])
def create_product():
    from backend.db_utils import add_product

    data = request.get_json()

    # Validate required fields
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    image_url = data.get('image_url')

    if not all([name, description, price, image_url]):
        return jsonify({
            'success': False,
            'error': 'Missing required fields: name, description, price, image_url'
        }), 400

    # Optional fields
    external_link = data.get('external_link')
    category = data.get('category')

    # Add product to database
    product = add_product(
        name=name,
        description=description,
        price=float(price),
        image_url=image_url,
        external_link=external_link,
        category=category
    )

    if product:
        return jsonify({
            'success': True,
            'product': {
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'image_url': product.image_url,
                'external_link': product.external_link,
                'category': product.category
            }
        }), 201
    else:
        return jsonify({
            'success': False,
            'error': 'Product already exists'
        }), 409

@app.route("/api/products/<int:product_id>", methods=['PUT'])
def update_product(product_id):
    pass

@app.route("/api/products/<int:product_id>", methods=['DELETE'])
def delete_product(product_id):
    pass


# Wishlist Endpoints
@app.route("/api/wishlist", methods=['POST'])
def add_to_wishlist():
    pass

@app.route("/api/wishlist/<int:user_id>", methods=['GET'])
def get_user_wishlist(user_id):
    pass

@app.route("/api/wishlist", methods=['DELETE'])
def remove_from_wishlist():
    pass


# User Endpoints
@app.route("/api/users/<int:user_id>", methods=['GET'])
def get_user(user_id):
    from backend.db_utils import get_user_by_id
    from flask import session

    # Security check: ensure logged-in user can only access their own profile
    if 'user_id' not in session:
        return jsonify({
            'success': False,
            'error': 'Not authenticated'
        }), 401

    if session['user_id'] != user_id:
        return jsonify({
            'success': False,
            'error': 'Unauthorized access'
        }), 403

    # Get user from database
    user = get_user_by_id(user_id)

    if not user:
        return jsonify({
            'success': False,
            'error': 'User not found'
        }), 404

    # Return user data (extract from database object, not session)
    return jsonify({
        'success': True,
        'user': {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at.strftime('%Y-%m-%d')
        }
    })


@app.route("/api/users/<int:user_id>", methods=['PUT'])
def update_user(user_id):
    pass

@app.route("/api/users/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    pass


# Category Endpoints
@app.route("/api/categories", methods=['GET'])
def get_categories():
    pass

if __name__ == "__main__":
    app.run(debug=True, port=5001)
