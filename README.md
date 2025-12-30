# Tech Product Finder

A Flask-based e-commerce website for browsing and discovering technology products.

## Project Structure

```
Tech-Product-Website/
├── app.py                 # Flask application (routes & config)
├── techfinder.db          # SQLite database
├── backend/               # Backend core files
│   ├── __init__.py
│   ├── models.py          # Database models (User, Product, Wishlist)
│   └── db_utils.py        # Database utility functions
├── scripts/               # Admin & utility scripts
│   ├── init_db.py         # Initialize/reset database
│   └── db_admin.py        # Interactive admin panel
├── docs/                  # Documentation
│   ├── DATABASE_GUIDE.md  # Comprehensive database guide
│   └── QUICK_REFERENCE.md # Quick command reference
├── templates/             # HTML templates (Jinja2)
│   └── index.html
└── static/                # Static assets (CSS, images)
    ├── style.css
    └── icons/
```

## Quick Start

### 1. Install Dependencies
```bash
pip install flask flask-sqlalchemy
```

### 2. Initialize Database
```bash
python scripts/init_db.py
```

### 3. Run Flask Server
```bash
python app.py
```

Visit: http://127.0.0.1:5000/

## Backend Functions

### Using Database Utilities
```python
from backend.db_utils import *

# Add a product
add_product(
    name='MacBook Pro',
    description='Professional laptop',
    price=2499.00,
    image_url='icons/macbook.png',
    category='Laptops'
)

# Create a user
create_user('john', 'john@email.com', 'password123')

# View all products
list_all_products()
```

### Admin Panel
```bash
python scripts/db_admin.py
```

Features:
- View all products/users/wishlists
- Update prices
- Delete records
- Search products
- Export to CSV
- Database statistics

## Documentation

- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Common commands and examples
- **[Database Guide](docs/DATABASE_GUIDE.md)** - Comprehensive database documentation

## Database Models

- **User** - Authentication and profiles
- **Product** - Tech product catalog
- **WishlistItem** - User wishlists (many-to-many)