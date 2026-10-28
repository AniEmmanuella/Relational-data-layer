from typing import List, Optional
from sqlalchemy.orm import Session
from app.models import User, Post

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_user_with_posts(self, username: str, email: str, posts_data: List[dict]) -> User:
        """
        Executes an atomic transaction: Creates a user and associated posts together.
        Rolls back automatically if an error occurs.
        """
        try:
            user = User(username=username, email=email)
            self.db.add(user)
            self.db.flush()  # Populates user.id without committing

            for p in posts_data:
                post = Post(title=p["title"], content=p["content"], user_id=user.id)
                self.db.add(post)

            self.db.commit()
            self.db.refresh(user)
            return user
        except Exception as e:
            self.db.rollback()
            raise e

    def get_user_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()