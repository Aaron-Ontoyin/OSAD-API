# Flask API with JWT Authentication and User Management

This project implements a Flask API with user authentication and management features using JWT tokens. It allows users to register, sign in, and store their details and images securely in a PostgreSQL database. Users can also manage their account information and view their uploaded images.

## Features

* User Registration and Sign-in
* JWT Authentication for Secure Access
* User Account Management
* Secure Image Storage in PostgreSQL
* Image Upload and Retrieval
* User Friendly API Endpoints

## Technologies

* Flask
* Flask-JWT
* Flask-SQLAlchemy
* PostgreSQL
* Python 3.x

## Getting Started

1. Install the required dependencies:
    ```bash
    pip install Flask Flask-JWT Flask-SQLAlchemy psycopg2-binary
    ```
2. Configure your database connection details in `app.py`.
3. Create a database and tables (optional).
4. Run the application:
    ```bash
    python app.py
    ```

## API Endpoints

* `/api/v1/users/register`: Register a new user.
* `/api/v1/users/login`: Login an existing user.
* `/api/v1/users/me`: Get logged-in user details.
* `/api/v1/users/update`: Update logged-in user details.
* `/api/v1/images`: Upload a new image.
* `/api/v1/images/<id>`: Get information about a specific image.
* `/api/v1/images`: Get all images uploaded by the logged-in user.

## Documentation

For detailed documentation on API endpoints, request parameters, and response formats, please refer to the API documentation file.

## Contributing

Feel free to contribute to this project by suggesting improvements, fixing bugs, or adding new features. Please make sure to follow the contribution guidelines.

## License
