import getpass
from app.database import SessionLocal, Base, engine
from app.models.user import User, RoleEnum
from app.core.security import hash_password

Base.metadata.create_all(bind=engine)


def choose_role() -> RoleEnum:
    roles = list(RoleEnum)
    print("\nSelect a role:")
    for idx, role in enumerate(roles, start=1):
        print(f"  {idx}. {role.value}")

    while True:
        choice = input(f"Enter choice (1-{len(roles)}): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(roles):
            return roles[int(choice) - 1]
        print("Invalid choice. Try again.")


def create_user():
    db = SessionLocal()
    try:
        print("=== Create New User ===")
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

        role = choose_role()

        existing = db.query(User).filter(User.email == email).first()
        if existing:
            print(f"A user with email '{email}' already exists.")
            return

        user = User(
            full_name=full_name,
            email=email,
            hashed_password=hash_password(password),
            role=role,
            is_active=True,
        )
        db.add(user)
        db.commit()
        print(f"\nUser '{full_name}' created successfully with role '{role.value}'.")
    finally:
        db.close()


if __name__ == "__main__":
    create_user()