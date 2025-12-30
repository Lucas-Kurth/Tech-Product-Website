# Quick Reference Guide - Database Functions

All backend database operations are now in **`db_utils.py`**

---

## Adding Products

### Add Single Product
```python
from db_utils import add_product

add_product(
    name='MacBook Pro M3',
    description='Professional laptop with M3 chip',
    price=2499.00,
    image_url='icons/macbook.png',
    external_link='https://www.apple.com/macbook-pro/',
    category='Laptops'
)
```

### Add Multiple Products (Bulk)
```python
from db_utils import add_products_bulk

products = [
    {
        'name': 'Product 1',
        'description': 'Description here',
        'price': 99.99,
        'image_url': 'icons/product1.png',
        'external_link': 'https://example.com',
        'category': 'Category'
    },
    {
        'name': 'Product 2',
        'description': 'Another product',
        'price': 149.99,
        'image_url': 'icons/product2.png',
        'category': 'Category'
    }
]

add_products_bulk(products)
```

---

## Managing Products

### View All Products
```python
from db_utils import list_all_products
list_all_products()
```

### Get Product by ID
```python
from db_utils import get_product_by_id
product = get_product_by_id(1)
print(f"{product.name} - ${product.price}")
```

### Update Product
```python
from db_utils import update_product

# Update price
update_product(1, price=699.00)

# Update multiple fields
update_product(1, price=699.00, description="New description", category="Tablets")
```

### Delete Product
```python
from db_utils import delete_product
delete_product(9)  # Deletes product with ID 9
```

---

## User Management

### Create User
```python
from db_utils import create_user
user = create_user('john_doe', 'john@example.com', 'password123')
```

### Authenticate User
```python
from db_utils import authenticate_user
user = authenticate_user('john_doe', 'password123')
if user:
    print(f"Welcome {user.username}!")
```

### View All Users
```python
from db_utils import list_all_users
list_all_users()
```

---

## Wishlist Operations

### Add to Wishlist
```python
from db_utils import add_to_wishlist
add_to_wishlist(user_id=1, product_id=5)
```

### Remove from Wishlist
```python
from db_utils import remove_from_wishlist
remove_from_wishlist(user_id=1, product_id=5)
```

### View User's Wishlist
```python
from db_utils import get_user_wishlist
wishlist = get_user_wishlist(user_id=1)
for product in wishlist:
    print(f"{product.name} - ${product.price}")
```

---

## Admin Tools

### Interactive Admin Panel
```bash
python db_admin.py
```
Features:
- View all products/users/wishlists
- Update prices
- Delete records
- Search products
- Export to CSV
- Database statistics

### View Database Contents
```bash
python db_utils.py
```

### Initialize/Reset Database
```bash
python init_db.py
```

---

## Common Tasks

### Add a New Product and Test It
```python
from db_utils import add_product, get_product_by_id

# Add product
product = add_product(
    name='PlayStation 5',
    description='Next-gen gaming console',
    price=499.00,
    image_url='icons/ps5.png',
    category='Gaming'
)

# Verify it was added
if product:
    retrieved = get_product_by_id(product.id)
    print(f"Added: {retrieved.name}")
```

### Create User and Add Products to Their Wishlist
```python
from db_utils import create_user, add_to_wishlist, get_user_wishlist

# Create user
user = create_user('alice', 'alice@example.com', 'pass123')

if user:
    # Add products to wishlist
    add_to_wishlist(user.id, 1)  # iPad
    add_to_wishlist(user.id, 4)  # iPhone

    # View wishlist
    wishlist = get_user_wishlist(user.id)
    print(f"\n{user.username}'s Wishlist:")
    for p in wishlist:
        print(f"  - {p.name}")
```

### Update Product Price
```python
from db_utils import update_product, get_product_by_id

# Check current price
product = get_product_by_id(1)
print(f"Current price: ${product.price}")

# Update price
update_product(1, price=649.00)

# Verify
product = get_product_by_id(1)
print(f"New price: ${product.price}")
```

---

## File Structure Reference

```
Tech-Product-Website/
├── app.py                  # Flask app + DB config
├── models.py               # Database models (tables)
├── db_utils.py            # ALL database functions ⭐
├── db_admin.py            # Interactive admin panel
├── init_db.py             # Initialize database
├── techfinder.db          # SQLite database file
├── templates/
│   └── index.html
└── static/
    ├── style.css
    └── icons/
```

---

## Next Steps for Backend

1. **Create API endpoints** in `app.py` for frontend to call
2. **Add Flask-Login** for session management
3. **Create routes** for:
   - `/api/products` - Get all products
   - `/api/products/<id>` - Get single product
   - `/api/wishlist` - Manage wishlist
   - `/api/register` - User registration
   - `/api/login` - User login

---

## Tips

- All functions print status messages when you run them
- Functions return `None` if operation fails (e.g., duplicate username)
- Use `python -i` to enter interactive Python shell
- Database file is ignored by git (in `.gitignore`)
- Backup database: `cp techfinder.db techfinder_backup.db`
