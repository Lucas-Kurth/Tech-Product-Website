# Database Management Guide

## Current Database Status
- **Database File**: `techfinder.db` (SQLite)
- **Tables**: Users, Products, WishlistItems
- **Current Data**: 8 products, 1 test user

---

## 1. Adding More Products

### Option A: Using Python Script
Create a new file `add_products.py`:

```python
from app import app, db
from models import Product

with app.app_context():
    # Add a new product
    new_product = Product(
        name='MacBook Pro M3',
        description='Professional laptop with M3 Pro chip and stunning display.',
        price=2499.00,
        image_url='icons/macbook.png',
        external_link='https://www.apple.com/macbook-pro/',
        category='Laptops'
    )

    db.session.add(new_product)
    db.session.commit()
    print(f"Added: {new_product.name}")
```

Then run: `python add_products.py`

### Option B: Using Interactive Python Shell

```bash
python
```

```python
from app import app, db
from models import Product

with app.app_context():
    # Create product
    product = Product(
        name='AirPods Pro 2',
        description='Active noise cancellation and spatial audio',
        price=249.00,
        image_url='icons/airpods.png',
        external_link='https://www.apple.com/airpods-pro/',
        category='Audio'
    )
    db.session.add(product)
    db.session.commit()
```

### Option C: Bulk Import from List

```python
from app import app, db
from models import Product

products_to_add = [
    {
        'name': 'MacBook Pro M3',
        'description': 'Professional laptop with M3 Pro chip',
        'price': 2499.00,
        'image_url': 'icons/macbook.png',
        'external_link': 'https://www.apple.com/macbook-pro/',
        'category': 'Laptops'
    },
    {
        'name': 'PlayStation 5',
        'description': 'Next-gen gaming console',
        'price': 499.00,
        'image_url': 'icons/ps5.png',
        'external_link': 'https://www.playstation.com/',
        'category': 'Gaming'
    }
]

with app.app_context():
    for p in products_to_add:
        product = Product(**p)
        db.session.add(product)
    db.session.commit()
    print(f"Added {len(products_to_add)} products!")
```

---

## 2. Managing Users

### Create a New User
```python
from db_utils import create_user

# Create user with username, email, password
create_user('john_doe', 'john@example.com', 'securepass123')
```

### Authenticate a User (Login)
```python
from db_utils import authenticate_user

user = authenticate_user('john_doe', 'securepass123')
if user:
    print(f"Welcome, {user.username}!")
```

### List All Users
```python
from db_utils import list_all_users

list_all_users()
```

---

## 3. Managing Wishlists

### Add Product to User's Wishlist
```python
from db_utils import add_to_wishlist

# Add product ID 1 to user ID 1's wishlist
add_to_wishlist(user_id=1, product_id=1)
```

### Remove from Wishlist
```python
from db_utils import remove_from_wishlist

remove_from_wishlist(user_id=1, product_id=1)
```

### View User's Wishlist
```python
from db_utils import get_user_wishlist

wishlist = get_user_wishlist(user_id=1)
for product in wishlist:
    print(f"{product.name} - ${product.price}")
```

---

## 4. Querying the Database

### Get All Products
```python
from app import app, db
from models import Product

with app.app_context():
    products = Product.query.all()
    for p in products:
        print(f"{p.id}: {p.name} - ${p.price}")
```

### Filter Products by Category
```python
with app.app_context():
    laptops = Product.query.filter_by(category='Laptops').all()
    for laptop in laptops:
        print(laptop.name)
```

### Filter Products by Price Range
```python
with app.app_context():
    # Products under $500
    affordable = Product.query.filter(Product.price < 500).all()

    # Products between $500 and $1000
    mid_range = Product.query.filter(
        Product.price >= 500,
        Product.price <= 1000
    ).all()
```

### Search Products by Name
```python
with app.app_context():
    # Search for products containing "iPhone"
    results = Product.query.filter(Product.name.like('%iPhone%')).all()
```

### Get Specific Product
```python
with app.app_context():
    product = Product.query.get(1)  # Get product with ID 1
    print(f"{product.name}: {product.description}")
```

---

## 5. Updating Records

### Update Product Price
```python
from app import app, db
from models import Product

with app.app_context():
    product = Product.query.get(1)
    product.price = 649.00  # Update price
    db.session.commit()
    print(f"Updated {product.name} price to ${product.price}")
```

### Update User Information
```python
from app import app, db
from models import User

with app.app_context():
    user = User.query.get(1)
    user.email = 'newemail@example.com'
    db.session.commit()
```

---

## 6. Deleting Records

### Delete a Product
```python
from app import app, db
from models import Product

with app.app_context():
    product = Product.query.get(9)  # Get product by ID
    if product:
        db.session.delete(product)
        db.session.commit()
        print(f"Deleted {product.name}")
```

### Delete a User
```python
from app import app, db
from models import User

with app.app_context():
    user = User.query.filter_by(username='testuser').first()
    if user:
        db.session.delete(user)
        db.session.commit()
```

---

## 7. Advanced Queries

### Count Products by Category
```python
from app import app, db
from models import Product
from sqlalchemy import func

with app.app_context():
    category_counts = db.session.query(
        Product.category,
        func.count(Product.id)
    ).group_by(Product.category).all()

    for category, count in category_counts:
        print(f"{category}: {count} products")
```

### Get Most Wishlisted Products
```python
from app import app, db
from models import Product, WishlistItem
from sqlalchemy import func

with app.app_context():
    popular_products = db.session.query(
        Product.name,
        func.count(WishlistItem.id).label('wishlist_count')
    ).join(WishlistItem).group_by(Product.id).order_by(
        func.count(WishlistItem.id).desc()
    ).limit(5).all()

    for name, count in popular_products:
        print(f"{name}: {count} wishlists")
```

---

## 8. Database Maintenance

### View Database Schema
```bash
sqlite3 techfinder.db ".schema"
```

### Direct SQL Queries
```bash
sqlite3 techfinder.db "SELECT * FROM products;"
```

### Reset Database (Delete All Data)
```python
from app import app, db

with app.app_context():
    db.drop_all()  # Delete all tables
    db.create_all()  # Recreate empty tables
    print("Database reset!")
```

### Backup Database
```bash
cp techfinder.db techfinder_backup_$(date +%Y%m%d).db
```

---

## 9. Quick Testing Scripts

### Test User Registration & Wishlist Flow
```python
from db_utils import *

# Create users
user1 = create_user('alice', 'alice@example.com', 'pass123')
user2 = create_user('bob', 'bob@example.com', 'pass456')

# Add products to wishlists
if user1:
    add_to_wishlist(user1.id, 1)  # iPad
    add_to_wishlist(user1.id, 4)  # iPhone

if user2:
    add_to_wishlist(user2.id, 6)  # Gaming Laptop
    add_to_wishlist(user2.id, 8)  # Graphics Card

# Check wishlists
print("\nAlice's Wishlist:")
for p in get_user_wishlist(user1.id):
    print(f"  - {p.name}")

print("\nBob's Wishlist:")
for p in get_user_wishlist(user2.id):
    print(f"  - {p.name}")
```

---

## 10. Database Location & Info

- **File**: `/Users/jackkurth/Desktop/Tech-Product-Website/techfinder.db`
- **Type**: SQLite3
- **Size**: ~28KB (will grow with more data)
- **Excluded from Git**: Yes (via `.gitignore`)

---

## Common Commands Reference

```bash
# View all products
python -c "from db_utils import list_all_products; list_all_products()"

# View all users
python -c "from db_utils import list_all_users; list_all_users()"

# Re-initialize database (keeps existing data)
python init_db.py

# Interactive Python shell with database access
python
>>> from app import app, db
>>> from models import *
>>> with app.app_context():
...     # Your queries here
```

---

## Next Steps for Backend Development

1. **Create API Endpoints** - Build REST API routes for frontend
2. **Add Session Management** - Install Flask-Login for user sessions
3. **Form Validation** - Add Flask-WTF for secure form handling
4. **Password Reset** - Implement email-based password recovery
5. **Admin Panel** - Create admin routes to manage products
6. **Search Functionality** - Add full-text search for products
7. **Reviews/Ratings** - Create new models for product reviews

---

## Troubleshooting

### "Database is locked" error
The database file is being used by another process. Close other connections.

### Need to start fresh
```bash
rm techfinder.db
python init_db.py
```

### Import errors
Make sure Flask-SQLAlchemy is installed:
```bash
pip install flask-sqlalchemy
```
