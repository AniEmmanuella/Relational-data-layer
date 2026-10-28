# Relational Data Layer

A small relational schema and Python data layer built with SQLAlchemy and SQLite. It has a one-to-many relationship (one user has many posts), a seed script, and tests that check transaction commit and rollback behavior.

## Demo

Demo recording: https://drive.google.com/file/d/14EtMm10VYZvz5Ln-6T7G269G3zC_Nd5o/view?usp=sharing

## Project structure

    app/
      database.py     engine and session setup
      models.py       User and Post models with relationships
      repository.py   data access functions
      seed.py         populates the database with sample data
    tests/
      test_transactions.py   commit and rollback tests
    requirements.txt

## Setup

    python -m venv .venv
    .\.venv\Scripts\python -m pip install -r requirements.txt

## Run

Seed the database:

    .\.venv\Scripts\python -m app.seed

Run the tests:

    .\.venv\Scripts\python -m pytest -v

## Schema

- users: id, username (unique), email (unique)
- posts: id, title, content, user_id (foreign key to users.id)
- Deleting a user also deletes their posts (cascade).
