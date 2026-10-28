import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.repository import UserRepository
from app.models import User, Post

# In-memory database for quick testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()
    Base.metadata.drop_all(bind=engine)

def test_successful_transaction(db_session):
    repo = UserRepository(db_session)
    user = repo.create_user_with_posts(
        username="john_doe",
        email="john@example.com",
        posts_data=[{"title": "Test Title", "content": "Test Content"}]
    )

    assert user.id is not None
    assert len(user.posts) == 1

def test_rollback_on_failure(db_session):
    repo = UserRepository(db_session)

    # Intentional failure: pass invalid payload missing 'content' key
    with pytest.raises(KeyError):
        repo.create_user_with_posts(
            username="fail_user",
            email="fail@example.com",
            posts_data=[{"title": "No Content"}]
        )

    # Verify user was NOT saved (rolled back completely)
    assert db_session.query(User).filter_by(username="fail_user").first() is None