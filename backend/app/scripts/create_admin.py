import getpass
from app.database import SessionLocal, Base, engine
from app.models.user import User, RoleEnum
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)

def create_admin():
    db = SessionLocal()
    try:
        full_name = input("Enter full name: ").strip()
        email = input("Enter email: ").strip()
        password = getpass.getpass("Enter password: ").strip()
        confirm_password = getpass.getpass("Confirm password: ").strip()

        if not full_name or not email or not password:
            print("All fields are required. Aborting.")
            return

        if password != confirm_password:
            print("Passwords do not match. Aborting.")
            return

        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"A user with email '{email}' already exists.")
            return

        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
            role=RoleEnum.admin,
            is_active=True,
        )
        db.add(user)
        db.commit()
        print(f"Admin '{full_name}' created successfully.")
    finally:
        db.close()


if __name__ == "__main__":
    create_admin()