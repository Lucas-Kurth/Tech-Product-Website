# Project Structure & Organization

## Clean Architecture Overview

Your project now follows a clean, scalable architecture with proper separation of concerns:

```
Tech-Product-Website/
├── app.py                      # Flask app entry point (routes & config)
├── techfinder.db               # SQLite database (git-ignored)
├── README.md                   # Project overview & quick start
│
├── backend/                    # Core backend logic
│   ├── __init__.py            # Makes backend a Python package
│   ├── models.py              # Database models (User, Product, WishlistItem)
│   └── db_utils.py            # Database utility functions
│
├── scripts/                    # Admin & maintenance scripts
│   ├── init_db.py             # Initialize/reset database
│   └── db_admin.py            # Interactive admin panel
│
├── docs/                       # Documentation
│   ├── DATABASE_GUIDE.md      # Comprehensive database guide
│   ├── QUICK_REFERENCE.md     # Quick command reference
│   └── PROJECT_STRUCTURE.md   # This file
│
├── templates/                  # HTML templates (Jinja2)
│   └── index.html             # Homepage template
│
└── static/                     # Static assets
    ├── style.css              # CSS styles
    └── icons/                 # Product images
        └── *.png
```

---

## File Purposes

### Root Level

- **app.py** - Flask application
  - Routes (`/`, `/login`)
  - Database configuration
  - Flask app initialization
  - Run this to start the server: `python app.py`

- **techfinder.db** - SQLite database
  - Auto-generated
  - Ignored by git
  - Contains all data (users, products, wishlists)

### Backend/ (Core Logic)

- **models.py** - Database models
  - User model (authentication)
  - Product model (catalog)
  - WishlistItem model (user wishlists)

- **db_utils.py** - Database functions
  - User management (create, authenticate)
  - Product operations (add, update, delete, query)
  - Wishlist management
  - All backend operations in one place

- **__init__.py** - Package marker
  - Makes `backend/` importable as a Python package
  - Allows `from backend.models import User`

### Scripts/ (Utilities)

- **init_db.py** - Database initialization
  - Creates all tables
  - Populates initial data (8 products)
  - Run: `python scripts/init_db.py`

- **db_admin.py** - Admin panel
  - Interactive CLI tool
  - View/edit products, users, wishlists
  - Database statistics
  - Export to CSV
  - Run: `python scripts/db_admin.py`

### Docs/ (Documentation)

- **DATABASE_GUIDE.md** - Full database documentation
  - Complete examples for all operations
  - Advanced queries
  - Maintenance guide

- **QUICK_REFERENCE.md** - Quick commands
  - Common tasks
  - Code snippets
  - File structure reference

- **PROJECT_STRUCTURE.md** - This file
  - Architecture overview
  - File organization
  - Best practices

### Templates/ (Frontend)

- **index.html** - Homepage template
  - Jinja2 template
  - Displays product cards
  - Navigation bar
  - Uses `url_for()` for static files

### Static/ (Assets)

- **style.css** - Stylesheet
  - Gradient backgrounds
  - Card layouts
  - Responsive design

- **icons/** - Product images
  - PNG format
  - Referenced in database

---

## Why This Structure?

### Benefits:

1. **Separation of Concerns**
   - Backend logic separate from admin tools
   - Documentation organized in one place
   - Clear boundaries between components

2. **Scalability**
   - Easy to add new models (create in `backend/models.py`)
   - Easy to add new utility functions (add to `backend/db_utils.py`)
   - Easy to add new admin scripts (add to `scripts/`)

3. **Maintainability**
   - Find files quickly
   - Clear file purposes
   - Professional structure

4. **Team Collaboration**
   - Frontend team works in `templates/` and `static/`
   - Backend team works in `backend/` and `app.py`
   - Admins use `scripts/`
   - Clear ownership

---

## Import Patterns

### From Root Directory

```python
# Import models
from backend.models import User, Product, WishlistItem

# Import utilities
from backend.db_utils import create_user, add_product

# Import Flask app
from app import app, db
```

### From Scripts

Scripts automatically add parent directory to path:

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now can import normally
from app import app, db
from backend.models import User, Product
```

---

## Common Operations

### Adding a New Feature

1. **Define Model** (if needed)
   - Edit `backend/models.py`
   - Add new class with columns

2. **Add Utility Functions**
   - Edit `backend/db_utils.py`
   - Add functions to interact with model

3. **Create Route** (if needed)
   - Edit `app.py`
   - Add new `@app.route()`

4. **Create Template** (if needed)
   - Add HTML to `templates/`
   - Add CSS to `static/style.css`

### Running the Project

```bash
# Initialize database (first time only)
python scripts/init_db.py

# Run Flask server
python app.py

# Open admin panel (separate terminal)
python scripts/db_admin.py
```

### Using Database Functions

```python
from backend.db_utils import *

# All functions available
create_user('john', 'john@email.com', 'pass123')
add_product('MacBook', 'Description...', 2499.00, 'icons/mac.png', category='Laptops')
list_all_products()
```

---

## .gitignore Coverage

Protected files:
- `*.db` - Database files
- `__pycache__/` - Python cache
- `.venv/` - Virtual environment
- `*.log` - Log files
- `.DS_Store` - Mac files
- `.idea/`, `.vscode/` - IDE files

---

## Next Steps

As you build out the project:

1. **Add API Routes** (`app.py`)
   - RESTful endpoints for frontend
   - `/api/products`, `/api/users`, etc.

2. **Add Authentication** (`backend/`)
   - Flask-Login for sessions
   - Login/logout routes

3. **Add More Models** (`backend/models.py`)
   - Reviews, Orders, Categories, etc.

4. **Add More Scripts** (`scripts/`)
   - Data migration scripts
   - Backup scripts
   - Test data generators

5. **Expand Documentation** (`docs/`)
   - API documentation
   - Deployment guide
   - Contributing guidelines

---

## Best Practices

1. **Keep backend/ clean**
   - Only core logic
   - No admin utilities
   - No test scripts

2. **Use scripts/ for one-off tasks**
   - Database management
   - Admin tools
   - Maintenance tasks

3. **Document everything in docs/**
   - Update guides when adding features
   - Keep examples current

4. **Follow import patterns**
   - Use `from backend.module import Class`
   - Don't mix relative and absolute imports

5. **Test before committing**
   - Run `python scripts/init_db.py` to verify
   - Check imports work
   - Test all modified functions