# Setup Guide for New Developers

Follow these steps in order to get the project running on your machine.

---

## First Time Setup

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Tech-Product-Website
```

### Step 2: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python -m venv .venv

# Activate it
# On Mac/Linux:
source .venv/bin/activate

# On Windows:
.venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install flask flask-sqlalchemy
```

Or if there's a requirements.txt:
```bash
pip install -r requirements.txt
```

### Step 4: Initialize the Database
```bash
python scripts/init_db.py
```

**Expected Output:**
```
Database tables created successfully!
Added 8 sample products to the database!
```

This will:
- Create the `techfinder.db` file (SQLite database)
- Create all tables (users, products, wishlist_items)
- Populate with 8 initial products

### Step 5: Verify Database Setup
```bash
python -c "from backend.db_utils import list_all_products; list_all_products()"
```

**Expected Output:**
```
=== Total Products: 8 ===
ID: 1 | Apple iPad Air M3 | $599.0
ID: 2 | Lenovo ThinkPad | $1299.0
...
```

### Step 6: Run the Flask Server
```bash
python app.py
```

**Expected Output:**
```
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### Step 7: Test in Browser
Open: http://127.0.0.1:5000/

You should see the Tech Product Finder homepage with 8 products.

---

## Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'flask'"

**Problem:** Flask not installed

**Solution:**
```bash
pip install flask flask-sqlalchemy
```

### Issue 2: "ModuleNotFoundError: No module named 'backend'"

**Problem:** Running scripts from wrong directory

**Solution:** Make sure you're in the project root directory:
```bash
# Check current directory
pwd  # Should show .../Tech-Product-Website

# If not, navigate to project root
cd /path/to/Tech-Product-Website

# Then run the script
python scripts/init_db.py
```

### Issue 3: "No such file or directory: techfinder.db"

**Problem:** Database not initialized

**Solution:**
```bash
python scripts/init_db.py
```

### Issue 4: Database file exists but tables are empty

**Problem:** Database created but not populated

**Solution:** Reset the database:
```bash
# Delete old database
rm techfinder.db

# Re-initialize
python scripts/init_db.py
```

### Issue 5: "sqlite3.OperationalError: table users already exists"

**Problem:** Trying to initialize database that already exists

**Solution:** This is normal if database exists. The script will skip adding duplicate products. If you want a fresh start:
```bash
rm techfinder.db
python scripts/init_db.py
```

### Issue 6: Import errors when running scripts

**Problem:** Python path issues

**Solution:** Always run scripts from project root:
```bash
# Don't do this:
cd scripts
python init_db.py  # ❌

# Do this:
python scripts/init_db.py  # ✓
```

---

## Verifying Everything Works

Run these commands to verify setup:

```bash
# 1. Check Flask is installed
python -c "import flask; print(flask.__version__)"

# 2. Check database exists
ls -lh techfinder.db

# 3. Check products in database
python -c "from backend.db_utils import list_all_products; list_all_products()"

# 4. Run admin panel (interactive - press 0 to exit)
python scripts/db_admin.py

# 5. Start Flask server
python app.py
```

---

## Quick Setup Script

For convenience, you can run all setup steps at once:

```bash
# Create a setup script
cat > setup.sh << 'EOF'
#!/bin/bash
echo "🚀 Setting up Tech Product Finder..."

echo "📦 Creating virtual environment..."
python -m venv .venv
source .venv/bin/activate

echo "📥 Installing dependencies..."
pip install flask flask-sqlalchemy

echo "🗄️  Initializing database..."
python scripts/init_db.py

echo "✅ Setup complete!"
echo "Run 'python app.py' to start the server"
EOF

chmod +x setup.sh
./setup.sh
```

---

## File Checklist

After cloning, you should have:

```
✓ app.py
✓ README.md
✓ .gitignore
✓ backend/
  ✓ __init__.py
  ✓ models.py
  ✓ db_utils.py
✓ scripts/
  ✓ init_db.py
  ✓ db_admin.py
✓ docs/
  ✓ DATABASE_GUIDE.md
  ✓ QUICK_REFERENCE.md
  ✓ PROJECT_STRUCTURE.md
✓ templates/
  ✓ index.html
✓ static/
  ✓ style.css
  ✓ icons/ (8 PNG files)
```

**NOT included (auto-generated):**
- `techfinder.db` - Created by init_db.py
- `.venv/` - Created by you
- `__pycache__/` - Created by Python

---

## Daily Workflow

After initial setup, here's the typical workflow:

### Starting Work
```bash
# 1. Pull latest changes
git pull

# 2. Activate virtual environment
source .venv/bin/activate  # Mac/Linux
# or
.venv\Scripts\activate     # Windows

# 3. Check for new dependencies
pip install -r requirements.txt  # If added

# 4. Run migrations if database changed
# (If someone added new models)
python scripts/init_db.py

# 5. Start server
python app.py
```

### Making Changes
```bash
# Work on your feature...

# Test changes
python app.py

# If you modified models:
rm techfinder.db
python scripts/init_db.py
```

### Before Committing
```bash
# Don't commit database
git status  # Should NOT show techfinder.db

# Commit your changes
git add <files>
git commit -m "Your message"
git push
```

---

## Environment Variables (Future)

When you add sensitive config (API keys, secrets):

1. Create `.env` file (already in .gitignore):
```bash
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///techfinder.db
```

2. Install python-dotenv:
```bash
pip install python-dotenv
```

3. Load in app.py:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Need Help?

- **Documentation:** Check `/docs` folder
- **Database Issues:** Run `python scripts/db_admin.py` to inspect
- **Import Errors:** Make sure you're in project root
- **Flask Errors:** Check Python version (requires Python 3.7+)

---

## System Requirements

- **Python:** 3.7 or higher
- **Pip:** Latest version recommended
- **Git:** For version control
- **Browser:** Any modern browser

Check versions:
```bash
python --version  # Should be 3.7+
pip --version
git --version
```
