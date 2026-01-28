#!/usr/bin/env python3
"""
Command-line tool to make a user an admin.

Usage:
    python scripts/make_admin.py <email>
    python scripts/make_admin.py <email> --revoke
"""

import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User


def make_admin(email: str, revoke: bool = False) -> None:
    """
    Make a user an admin or revoke admin privileges.

    Args:
        email: User's email address
        revoke: If True, revoke admin privileges instead of granting them
    """
    db: Session = SessionLocal()

    try:
        # Find user by email
        user = db.query(User).filter(User.email == email).first()

        if not user:
            print(f"❌ Error: User with email '{email}' not found.")
            sys.exit(1)

        # Check if user is already an admin
        if not revoke and user.is_admin:
            print(f"ℹ️  User '{email}' is already an admin.")
            sys.exit(0)

        if revoke and not user.is_admin:
            print(f"ℹ️  User '{email}' is not an admin.")
            sys.exit(0)

        # Update admin status
        user.is_admin = not revoke
        db.commit()

        if revoke:
            print(f"✅ Successfully revoked admin privileges from '{email}'")
        else:
            print(f"✅ Successfully granted admin privileges to '{email}'")

        print(f"\nUser details:")
        print(f"  ID: {user.id}")
        print(f"  Email: {user.email}")
        print(f"  Name: {user.name or 'N/A'}")
        print(f"  Is Admin: {user.is_admin}")
        print(f"  Is Active: {user.is_active}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        db.rollback()
        sys.exit(1)

    finally:
        db.close()


def list_users() -> None:
    """List all users in the database."""
    db: Session = SessionLocal()

    try:
        users = db.query(User).order_by(User.created_at.desc()).all()

        if not users:
            print("No users found in the database.")
            sys.exit(0)

        print(f"\n{'ID':<5} {'Email':<30} {'Name':<20} {'Admin':<8} {'Active':<8}")
        print("-" * 80)

        for user in users:
            admin_status = "✓" if user.is_admin else ""
            active_status = "✓" if user.is_active else ""
            name = (user.name or "")[:20]
            email = user.email[:30]
            print(f"{user.id:<5} {email:<30} {name:<20} {admin_status:<8} {active_status:<8}")

        print(f"\nTotal users: {len(users)}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        sys.exit(1)

    finally:
        db.close()


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Make user admin:    python scripts/make_admin.py <email>")
        print("  Revoke admin:       python scripts/make_admin.py <email> --revoke")
        print("  List all users:     python scripts/make_admin.py --list")
        sys.exit(1)

    # List users command
    if sys.argv[1] == "--list":
        list_users()
        return

    # Make admin / revoke admin command
    email = sys.argv[1]
    revoke = "--revoke" in sys.argv

    make_admin(email, revoke)


if __name__ == "__main__":
    main()
