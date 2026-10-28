from app.database import engine, Base, SessionLocal
from app.repository import UserRepository

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    repo = UserRepository(db)

    print("Seeding database...")
    repo.create_user_with_posts(
        username="alex_dev",
        email="alex@example.com",
        posts_data=[
            {"title": "First Post", "content": "Hello World!"},
            {"title": "SQLAlchemy Tips", "content": "Always manage session scope cleanly."}
        ]
    )
    print("Seeding complete!")
    db.close()

if __name__ == "__main__":
    seed_database()