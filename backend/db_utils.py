"""
Database utility functions for backend operations
Use these functions to interact with the database programmatically
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from backend.models import User, Product, WishlistItem


def create_user(username, email, password):
    """
    Create a new user
    Returns: dict with user data if successful, None if user already exists
    """
    with app.app_context():
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            print(f"Error: Username '{username}' already exists")
            return None
        if User.query.filter_by(email=email).first():
            print(f"Error: Email '{email}' already exists")
            return None

        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        # Extract data before session closes
        user_data = {
            'id': user.id,
            'username': user.username,
            'email': user.email
        }

        print(f"User '{username}' created successfully!")
        return user_data


def get_user_by_username(username):
    """Get a user by username"""
    with app.app_context():
        return User.query.filter_by(username=username).first()


def get_user_by_email(email):
    """Get a user by email"""
    with app.app_context():
        return User.query.filter_by(email=email).first()
    
    
def get_user_by_id(user_id):
    """Get a user by ID"""
    with app.app_context():
        return User.query.filter_by(id=user_id).first()


def authenticate_user(username_or_email, password):
    """
    Authenticate a user
    Returns: User object if credentials are valid, None otherwise
    """
    with app.app_context():
        # Try to find user by username or email
        user = User.query.filter_by(username=username_or_email).first()
        if not user:
            user = User.query.filter_by(email=username_or_email).first()

        if user and user.check_password(password):
            print(f"Authentication successful for '{username_or_email}'")
            return user
        else:
            print(f"Authentication failed for '{username_or_email}'")
            return None


def get_all_products():
    """Get all products from the database"""
    with app.app_context():
        return Product.query.all()


def get_product_by_id(product_id):
    """Get a specific product by ID"""
    with app.app_context():
        return Product.query.get(product_id)


def add_to_wishlist(user_id, product_id):
    """
    Add a product to user's wishlist
    Returns: WishlistItem if successful, None if already exists
    """
    with app.app_context():
        # Check if already in wishlist
        existing = WishlistItem.query.filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()

        if existing:
            print("Product already in wishlist")
            return None

        wishlist_item = WishlistItem(user_id=user_id, product_id=product_id)
        db.session.add(wishlist_item)
        db.session.commit()
        print("Product added to wishlist!")
        return wishlist_item


def remove_from_wishlist(user_id, product_id):
    """Remove a product from user's wishlist"""
    with app.app_context():
        wishlist_item = WishlistItem.query.filter_by(
            user_id=user_id,
            product_id=product_id
        ).first()

        if wishlist_item:
            db.session.delete(wishlist_item)
            db.session.commit()
            print("Product removed from wishlist!")
            return True
        else:
            print("Product not found in wishlist")
            return False


def get_user_wishlist(user_id):
    """Get all products in a user's wishlist"""
    with app.app_context():
        user = User.query.get(user_id)
        if user:
            return [item.product for item in user.wishlist_items]
        return []


def list_all_users():
    """List all users (for debugging)"""
    with app.app_context():
        users = User.query.all()
        print(f"\n=== Total Users: {len(users)} ===")
        for user in users:
            print(f"ID: {user.id} | Username: {user.username} | Email: {user.email}")
        return users


def list_all_products():
    """List all products (for debugging)"""
    with app.app_context():
        products = Product.query.all()
        print(f"\n=== Total Products: {len(products)} ===")
        for product in products:
            print(f"ID: {product.id} | {product.name} | ${product.price}")
        return products


def add_product(name, description, price, image_url, external_link=None, category=None):
    """
    Add a new product to the database
    Returns: Product object if successful, None if product already exists
    """
    with app.app_context():
        # Check if product already exists
        existing = Product.query.filter_by(name=name).first()
        if existing:
            print(f"Error: Product '{name}' already exists")
            return None

        product = Product(
            name=name,
            description=description,
            price=price,
            image_url=image_url,
            external_link=external_link,
            category=category
        )

        db.session.add(product)
        db.session.commit()
        print(f"Product '{name}' added successfully! (ID: {product.id})")
        return product


def add_products_bulk(products_list):
    """
    Add multiple products at once
    products_list: List of dictionaries with product data
    Returns: Number of products added
    """
    with app.app_context():
        added = 0
        for product_data in products_list:
            # Check if product already exists
            existing = Product.query.filter_by(name=product_data['name']).first()
            if existing:
                print(f"⊘ Skipping '{product_data['name']}' - already exists")
                continue

            product = Product(**product_data)
            db.session.add(product)
            added += 1
            print(f"✓ Added: {product_data['name']}")

        db.session.commit()
        print(f"\n{added} new products added to database!")
        return added


def update_product(product_id, **kwargs):
    """
    Update a product's fields
    Usage: update_product(1, price=699.00, description="New description")
    """
    with app.app_context():
        product = Product.query.get(product_id)
        if not product:
            print(f"Error: Product with ID {product_id} not found")
            return None

        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
                print(f"Updated {key}: {value}")

        db.session.commit()
        print(f"Product '{product.name}' updated successfully!")
        return product


def delete_product(product_id):
    """Delete a product from the database"""
    with app.app_context():
        product = Product.query.get(product_id)
        if not product:
            print(f"Error: Product with ID {product_id} not found")
            return False

        name = product.name
        db.session.delete(product)
        db.session.commit()
        print(f"Product '{name}' deleted successfully!")
        return True


# Example usage if run directly
if __name__ == '__main__':
    print("Database Utility Functions Demo\n")

    # List all products
    list_all_products()

    # Create a test user
    print("\n--- Creating Test User ---")
    test_user = create_user('testuser', 'test@example.com', 'password123')

    # List all users
    list_all_users()

    # Test authentication
    print("\n--- Testing Authentication ---")
    authenticate_user('testuser', 'password123')
    authenticate_user('testuser', 'wrongpassword')
