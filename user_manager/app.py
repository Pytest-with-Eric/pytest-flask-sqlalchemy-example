import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Get Postgres Environment Variables
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB = os.getenv("POSTGRES_DB")

# Get database URI from environment variable or use default
DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///./prod_db.db")
print("Using database URI:", DATABASE_URI)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"


@app.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return (
        jsonify(
            [
                {"id": user.id, "username": user.username, "email": user.email}
                for user in users
            ]
        ),
        200,
    )


@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    new_user = User(username=data["username"], email=data["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created"}), 201


def setup_database():
    with app.app_context():
        if not os.path.exists("user.db"):
            db.create_all()
            print("Database created")
        else:
            print("Database already exists")


if __name__ == "__main__":
    setup_database()
    app.run(debug=True)
