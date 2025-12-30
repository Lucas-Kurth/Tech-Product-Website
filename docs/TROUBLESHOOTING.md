# Troubleshooting Guide

Quick fixes for common issues when setting up the project.

---

## Setup Order (MUST follow this order!)

```bash
1. git clone <repo>
2. cd Tech-Product-Website
3. python -m venv .venv
4. source .venv/bin/activate  (or .venv\Scripts\activate on Windows)
5. pip install -r requirements.txt
6. python scripts/init_db.py
7. python app.py
```

---

## Quick Diagnostics

Run this command to check your setup:

```bash
python -c "
import sys
print('Python version:', sys.version)
try:
    import flask
    print('✓ Flask installed:', flask.__version__)
except:
    print('✗ Flask NOT installed - run: pip install flask')

try:
    import flask_sqlalchemy
    print('✓ Flask-SQLAlchemy installed')
except:
    print('✗ Flask-SQLAlchemy NOT installed - run: pip install flask-sqlalchemy')

import os
if os.path.exists('techfinder.db'):
    print('✓ Database file exists')
else:
    print('✗ Database NOT found - run: python scripts/init_db.py')

if os.path.exists('backend/models.py'):
    print('✓ Backend files found')
else:
    print('✗ Backend files NOT found - check git clone')
"
```

---

## Error Messages & Fixes

### "ModuleNotFoundError: No module named 'flask'"

**Fix:**
```bash
pip install -r requirements.txt
```

### "ModuleNotFoundError: No module named 'backend'"

**You're in wrong directory!**

```bash
# Check where you are
pwd

# Should be in project root, not inside scripts/
cd /path/to/Tech-Product-Website

# Then run commands from root
python scripts/init_db.py
```

### "FileNotFoundError: techfinder.db"

**Database not initialized**

```bash
python scripts/init_db.py
```

### "ImportError: attempted relative import with no known parent package"

**Running script incorrectly**

```bash
# ❌ Wrong
cd scripts
python init_db.py

# ✓ Correct
python scripts/init_db.py
```

### "sqlite3.OperationalError: table already exists"

**Normal - database already initialized**

To reset:
```bash
rm techfinder.db
python scripts/init_db.py
```

### Flask server starts but page shows "Hello, Flask!"

**Old database or wrong route**

Make sure you're at http://127.0.0.1:5000/ (not /login)

### No products showing on homepage

**Database not populated**

```bash
# Check if products exist
python -c "from backend.db_utils import list_all_products; list_all_products()"

# If empty, reinitialize
rm techfinder.db
python scripts/init_db.py
```

---

## Platform-Specific Issues

### Mac/Linux

**Virtual environment activation:**
```bash
source .venv/bin/activate
```

**Permission issues:**
```bash
chmod +x scripts/init_db.py
```

### Windows

**Virtual environment activation:**
```cmd
.venv\Scripts\activate
```

**Execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## Complete Reset

If everything is broken, start fresh:

```bash
# 1. Remove virtual environment
rm -rf .venv

# 2. Remove database
rm techfinder.db

# 3. Remove Python cache
find . -type d -name __pycache__ -exec rm -rf {} +

# 4. Start setup from scratch
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/init_db.py
python app.py
```

---

## Still Having Issues?

1. **Check you're in the right directory:**
   ```bash
   ls -la
   # Should see: app.py, backend/, scripts/, templates/, static/
   ```

2. **Check Python version:**
   ```bash
   python --version
   # Should be 3.7 or higher
   ```

3. **Check virtual environment is active:**
   ```bash
   which python
   # Should show path to .venv/bin/python
   ```

4. **Check file structure:**
   ```bash
   tree -L 2 -I '__pycache__|.venv|.git'
   ```

5. **Run diagnostics:**
   ```bash
   python scripts/db_admin.py
   # Choose option 5 for database statistics
   ```

---

## Contact

If you still can't get it working, share:
1. Error message (full output)
2. Operating system
3. Python version
4. Output of diagnostics command above
