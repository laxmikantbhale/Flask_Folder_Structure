from flask import Blueprint, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, create_refresh_token
import uuid
from passlib.handlers.bcrypt import bcrypt
from sqlalchemy.exc import IntegrityError
from models.user import User
from db import db
from email_validator import validate_email, EmailNotValidError

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth_bp', __name__)
bcrypt = Bcrypt()


# 📌 User Registration Route
@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registers a new user.

    ✅ Validates input fields (name, email, password, confirm_password).
    ✅ Checks if email format is valid.
    ✅ Ensures password and confirm_password match.
    ✅ Hashes the password before storing in the database.
    ✅ Prevents duplicate registrations.

    🔹 Sample Request:
    {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "password": "StrongPassword123",
        "confirm_password": "StrongPassword123"
    }

    🔹 Response (Success - 201):
    {
        "message": "User Registered Successfully!"
    }

    🔹 Response (Error - 400/500):
    {
        "message": "Error message here"
    }
    """
    try:
        data = request.get_json()
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')

        # Ensure all fields are provided
        if not all([name, email, password, confirm_password]):
            return jsonify({"message": "All fields are required"}), 400

        # Validate email format
        try:
            validate_email(email)
        except EmailNotValidError:
            return jsonify({"message": "Invalid email format"}), 400

        # Ensure passwords match
        if password != confirm_password:
            return jsonify({"message": "Passwords do not match"}), 400

        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        # Hash password before saving to DB
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create new user instance
        new_user = User(
            uid=str(uuid.uuid4()),
            name=name,
            email=email,
            password=hashed_password
        )

        # Save user to database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User Registered Successfully!"}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "User already exists"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": str(e)}), 500


# 📌 User Login Route
@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Logs in a user and returns both an access token and a refresh token.

    ✅ Checks if user exists.
    ✅ Validates password using bcrypt.
    ✅ Generates a JWT access token & refresh token.

    🔹 Sample Request:
    {
        "email": "johndoe@example.com",
        "password": "StrongPassword123"
    }

    🔹 Response (Success - 200):
    {
        "access_token": "eyJhbGciOiJIUzI1...",
        "refresh_token": "eyJhbGciOiJIUzI1..."
    }
    """
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    # Find user by email
    user = User.query.filter_by(email=email).first()

    # Validate user and password
    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.uid)
        refresh_token = create_refresh_token(identity=user.uid)
        return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200

    return jsonify({"message": "Invalid Credentials"}), 401


# 📌 Refresh Access Token
@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Generates a new access token using a refresh token.

    ✅ Requires a valid refresh token.
    ✅ Returns a new access token.

    🔹 Sample Request:
    Headers: { "Authorization": "Bearer <refresh_token>" }

    🔹 Response (Success - 200):
    {
        "access_token": "new_access_token_here"
    }
    """
    current_user = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user)

    return jsonify({"access_token": new_access_token}), 200


# 📌 Protected Route (Requires Authentication)
@auth_bp.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    """
    Protected route that requires authentication.

    ✅ Requires a valid JWT access token.

    🔹 Sample Request:
    Headers: { "Authorization": "Bearer <access_token>" }

    🔹 Response (Success - 200):
    {
        "message": "Hello, user <uid>!"
    }
    """
    current_user = get_jwt_identity()
    name = User.query.filter_by(uid=current_user).first().name
    return jsonify({"message": f"Hello, user {name}!"}), 200


