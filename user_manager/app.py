import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

db = SQLAlchemy()


def create_app(app_config=None):
    load_dotenv()

    app = Flask(__name__)

    # Get database URI from environment variables or use default
    DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///:memory:")

    if app_config:
        app.config.update(app_config)
    else:
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

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

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()
    app.run(debug=True)
