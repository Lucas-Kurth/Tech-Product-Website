# Tech Product Finder

A Flask-based e-commerce website for browsing and discovering technology products.

## 🚀 New Team Member? Start Here!

**First time setup:** See [SETUP.md](SETUP.md) for detailed step-by-step instructions.

**Having issues?** Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common fixes.

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

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database (creates techfinder.db)
python scripts/init_db.py

# 3. Run Flask server
python app.py
```

Visit: http://127.0.0.1:5000/

**Note:** See [SETUP.md](SETUP.md) for complete setup instructions including virtual environment.

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

### Getting Started
- **[SETUP.md](SETUP.md)** - Complete setup guide for new team members
- **[TROUBLESHOOTING.md](TROUBLESHOOTING.md)** - Common issues and fixes

### Reference
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Common commands and examples
- **[Database Guide](docs/DATABASE_GUIDE.md)** - Comprehensive database documentation
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Architecture overview

## Database Models

- **User** - Authentication and profiles
- **Product** - Tech product catalog
- **WishlistItem** - User wishlists (many-to-many)

### Curl command for adding products

curl -X POST http://localhost:5001/api/products \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Product Name",
    "description": "Product description here",
    "price": 99.99,
    "image_url": "https://example.com/image.jpg",
    "external_link": "https://example.com/buy",
    "category": "Electronics"
  }'
