"""
Database Administration Tool
Quick commands to view, update, and manage database
Usage: python scripts/db_admin.py
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from backend.models import User, Product, WishlistItem
from datetime import datetime


def display_menu():
    """Display admin menu"""
    print("\n" + "="*50)
    print("DATABASE ADMIN PANEL")
    print("="*50)
    print("\n[VIEW]")
    print("1. View all products")
    print("2. View all users")
    print("3. View all wishlists")
    print("4. View product by ID")
    print("5. View database statistics")
    print("\n[MANAGE]")
    print("6. Update product price")
    print("7. Delete product")
    print("8. Delete user")
    print("9. Search products by name")
    print("\n[UTILITIES]")
    print("10. Export products to CSV")
    print("0. Exit")
    print("="*50)


def view_all_products():
    """Display all products"""
    with app.app_context():
        products = Product.query.order_by(Product.category, Product.name).all()
        print(f"\n=== ALL PRODUCTS ({len(products)}) ===\n")

        current_category = None
        for p in products:
            if p.category != current_category:
                current_category = p.category
                print(f"\n--- {current_category or 'Uncategorized'} ---")

            print(f"  [{p.id}] {p.name}")
            print(f"      ${p.price:.2f} | {p.description[:60]}...")


def view_all_users():
    """Display all users"""
    with app.app_context():
        users = User.query.all()
        print(f"\n=== ALL USERS ({len(users)}) ===\n")

        for u in users:
            wishlist_count = len(u.wishlist_items)
            print(f"  [{u.id}] {u.username}")
            print(f"      Email: {u.email}")
            print(f"      Wishlist: {wishlist_count} items")
            print(f"      Joined: {u.created_at.strftime('%Y-%m-%d')}")
            print()


def view_all_wishlists():
    """Display all wishlist relationships"""
    with app.app_context():
        users = User.query.all()
        print(f"\n=== ALL WISHLISTS ===\n")

        for user in users:
            if user.wishlist_items:
                print(f"{user.username}'s Wishlist ({len(user.wishlist_items)} items):")
                for item in user.wishlist_items:
                    print(f"  • {item.product.name} - ${item.product.price}")
                print()


def view_product_by_id():
    """View detailed product information"""
    product_id = int(input("\nEnter Product ID: "))

    with app.app_context():
        product = Product.query.get(product_id)

        if not product:
            print(f"✗ Product with ID {product_id} not found")
            return

        print(f"\n=== PRODUCT DETAILS ===")
        print(f"ID: {product.id}")
        print(f"Name: {product.name}")
        print(f"Description: {product.description}")
        print(f"Price: ${product.price:.2f}")
        print(f"Category: {product.category}")
        print(f"Image: {product.image_url}")
        print(f"External Link: {product.external_link}")
        print(f"Created: {product.created_at.strftime('%Y-%m-%d %H:%M')}")

        wishlist_count = len(product.wishlist_items)
        print(f"\nWishlisted by: {wishlist_count} users")


def view_statistics():
    """Display database statistics"""
    with app.app_context():
        user_count = User.query.count()
        product_count = Product.query.count()
        wishlist_count = WishlistItem.query.count()

        print(f"\n=== DATABASE STATISTICS ===")
        print(f"Total Users: {user_count}")
        print(f"Total Products: {product_count}")
        print(f"Total Wishlist Items: {wishlist_count}")

        # Category breakdown
        from sqlalchemy import func
        categories = db.session.query(
            Product.category,
            func.count(Product.id)
        ).group_by(Product.category).all()

        print(f"\nProducts by Category:")
        for category, count in categories:
            print(f"  • {category or 'Uncategorized'}: {count}")

        # Price statistics
        avg_price = db.session.query(func.avg(Product.price)).scalar()
        min_price = db.session.query(func.min(Product.price)).scalar()
        max_price = db.session.query(func.max(Product.price)).scalar()

        print(f"\nPrice Statistics:")
        print(f"  • Average: ${avg_price:.2f}")
        print(f"  • Minimum: ${min_price:.2f}")
        print(f"  • Maximum: ${max_price:.2f}")


def update_product_price():
    """Update a product's price"""
    product_id = int(input("\nEnter Product ID: "))
    new_price = float(input("Enter new price: $"))

    with app.app_context():
        product = Product.query.get(product_id)

        if not product:
            print(f"✗ Product with ID {product_id} not found")
            return

        old_price = product.price
        product.price = new_price
        db.session.commit()

        print(f"✓ Updated {product.name}")
        print(f"  Old price: ${old_price:.2f}")
        print(f"  New price: ${new_price:.2f}")


def delete_product():
    """Delete a product from database"""
    product_id = int(input("\nEnter Product ID to delete: "))

    with app.app_context():
        product = Product.query.get(product_id)

        if not product:
            print(f"✗ Product with ID {product_id} not found")
            return

        confirm = input(f"Delete '{product.name}'? (yes/no): ").lower()

        if confirm == 'yes':
            name = product.name
            db.session.delete(product)
            db.session.commit()
            print(f"✓ Deleted: {name}")
        else:
            print("Deletion cancelled")


def delete_user():
    """Delete a user from database"""
    user_id = int(input("\nEnter User ID to delete: "))

    with app.app_context():
        user = User.query.get(user_id)

        if not user:
            print(f"✗ User with ID {user_id} not found")
            return

        confirm = input(f"Delete user '{user.username}'? (yes/no): ").lower()

        if confirm == 'yes':
            username = user.username
            db.session.delete(user)
            db.session.commit()
            print(f"✓ Deleted user: {username}")
        else:
            print("Deletion cancelled")


def search_products():
    """Search products by name"""
    query = input("\nSearch for: ")

    with app.app_context():
        results = Product.query.filter(
            Product.name.like(f'%{query}%')
        ).all()

        print(f"\n=== SEARCH RESULTS ({len(results)}) ===\n")

        if results:
            for p in results:
                print(f"  [{p.id}] {p.name} - ${p.price:.2f}")
        else:
            print("No products found")


def export_to_csv():
    """Export products to CSV file"""
    import csv

    filename = f"products_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

    with app.app_context():
        products = Product.query.all()

        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['id', 'name', 'description', 'price', 'category', 'image_url', 'external_link']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for p in products:
                writer.writerow({
                    'id': p.id,
                    'name': p.name,
                    'description': p.description,
                    'price': p.price,
                    'category': p.category,
                    'image_url': p.image_url,
                    'external_link': p.external_link
                })

        print(f"\n✓ Exported {len(products)} products to: {filename}")


def main():
    """Main admin loop"""
    while True:
        display_menu()
        choice = input("\nEnter choice: ").strip()

        if choice == '0':
            print("\nExiting admin panel...")
            break
        elif choice == '1':
            view_all_products()
        elif choice == '2':
            view_all_users()
        elif choice == '3':
            view_all_wishlists()
        elif choice == '4':
            view_product_by_id()
        elif choice == '5':
            view_statistics()
        elif choice == '6':
            update_product_price()
        elif choice == '7':
            delete_product()
        elif choice == '8':
            delete_user()
        elif choice == '9':
            search_products()
        elif choice == '10':
            export_to_csv()
        else:
            print("Invalid choice")

        input("\nPress Enter to continue...")


if __name__ == '__main__':
    main()
