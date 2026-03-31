from models import User, Post

# Create tables
User.create_table()
Post.create_table()

# Insert user
alice = User(name="Alice", email="alice@example.com", age=30)
alice.save()

# Query
users = User.filter(age__gte=25).order_by("-name").all()
print(users)