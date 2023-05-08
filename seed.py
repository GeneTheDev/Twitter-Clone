"""Seed database with sample data from CSV Files."""
from sqlalchemy.exc import IntegrityError
from csv import DictReader
from app import db, app
from models import User, Message, Follows


def remove_duplicate_users(user_rows):
    unique_users = {}
    for row in user_rows:
        username = row['username']
        if username not in unique_users:
            unique_users[username] = row
    return list(unique_users.values())


with app.app_context():

    with open('./generator/users.csv') as users:
        unique_users = remove_duplicate_users(DictReader(users))
        db.session.bulk_insert_mappings(User, DictReader(users), unique_users)

    with open('./generator/messages.csv') as messages:
        messages_data = list(DictReader(messages))
        unique_user_ids = set(
            int(message_data["user_id"]) for message_data in messages_data)

        for user_id in unique_user_ids:
            user = db.session.query(User).get(user_id)
            if user is None:
                new_user = User(
                    id=user_id, username=f"User {user_id}", email=f"user{user_id}@example.com", password=f"password{user_id}")

                db.session.add(new_user)

        db.session.commit()

        db.session.bulk_insert_mappings(Message, DictReader(messages))

    with open("./generator/follows.csv") as follows:
        reader = DictReader(follows)
        for row in reader:
            try:
                follow = Follows(
                    user_being_followed_id=row['user_being_followed_id'], user_following_id=row['user_following_id'])
                db.session.add(follow)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
                print(
                    f"Skipping follow: {row['user_being_followed_id']} -> {row['user_following_id']} due to foreign key constraint violation")

    db.session.commit()
