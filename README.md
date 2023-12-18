# OSAD API

OSAD stands for Object Speech and Audio Detection. It is a powerful API designed to handle object storage and perform object detection tasks. 


## Features

- User Authentication: Register, login, password reset, and more.
- Image Upload: Users can upload images for object detection within them.
- Speech to text: Users can upload audio files to convert them into text
- Text to speech: Users can post text data to convert them to speech.


## Technologies

- Flask: A Python micro web framework that provides tools and functionalities for building web applications.
- SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) system for Python, providing a full suite of well-known enterprise-level persistence patterns.
- Torch Vision: A part of the PyTorch project, providing tools and resources for Computer Vision research. `fasterrcnn_resnet50_fpn_v2` with weights, `FasterRCNN_ResNet50_FPN_V2_Weights`
- PIL (Python Imaging Library): A library for opening, manipulating, and saving many different image file formats in Python.
- Bcrypt: A robust password hashing library for enhancing user security.
- python-dotenv: A Python module that allows you to specify environment variables in traditional UNIX-like “.env” files.
- Flask-JWT-Extended: A Flask extension that provides JWT support (including token freshness and token revoking) for managing user sessions.
- SpeechRecognition: A library for performing speech recognition in Python, with support for several engines and APIs.
- pyttsx3: A text-to-speech conversion library in Python, capable of converting text into speech in multiple languages.
- SMTP (Simple Mail Transfer Protocol): A protocol for sending email messages between servers, commonly used by Python’s smtplib for email services.
- PyDub: A simple and easy-to-use Python library for audio manipulation.
- PostgreSQL: A powerful, open-source object-relational database system.
- Redis: It’s an in-memory data structure store.


## Getting Started

To get started with the OSAD API
### Clone the repository and install the dependencies

```bash
git clone https://github.com/Aaron-Ontoyin/osad-api.git
cd osad-api
pip install -r requirements.txt
```

### Environment Variables

The application uses environment variables for configuration. These are stored in a `.env` file. Here's a list of the required variables:

- SECRET_KEY=
- JWT_SECRET_KEY=
- SQLALCHEMY_DATABASE_URI
- JWT_ACCESS_TOKEN_EXPIRES
- JWT_REFRESH_TOKEN_EXPIRES
- REDIS_URL

### Configuring PostgreSQL

PostgreSQL is used as the main database for the application. You can install it locally or use a cloud service like Amazon RDS. Once installed, set the `DATABASE_URL` environment variable to the URL of your database.

### Configuring Redis

Redis is used for caching and task queueing. You can install it locally or use a cloud service like Redis Labs. Once installed, set the `REDIS_URL` environment variable to the URL of your Redis server.


## Documentation

For detailed documentation on API endpoints, request parameters, and response formats, please refer to the API documentation file [DOCUMENTATION] (DOCUMENTATION.md).

## Contributing

Feel free to contribute to this project by suggesting improvements, fixing bugs, or adding new features. Please make sure to follow the contribution guidelines.

## Contribution Guidelines

We appreciate your interest in contributing to the OSAD API project! Here are some guidelines to help you get started:

- Fork the Repository: Start by forking the main OSAD API repository to your own GitHub account.
- Clone the Repository: After forking, clone the repository to your local machine to start making changes.
```
git clone https://github.com/<your-username>/osad-api.git
cd osad-api
```
- Create a New Branch: Always create a new branch for your changes. This keeps the project history clean and makes it easier to track your contributions.
```
git checkout -b <branch-name>
```
- Make Your Changes: Make the necessary changes or additions to the code. Please ensure your code adheres to the existing style for consistency.
- Commit Your Changes: Once you’ve made your changes, commit them with a clear and descriptive commit message.
```
git commit -m "Your detailed commit message"
```
- Push to GitHub: Push your changes to the remote repository on GitHub.
```
git push origin <branch-name>
```
- Submit a Pull Request: Go to your forked repository on GitHub and click on the “New Pull Request” button. Fill in the necessary details and submit your pull request.

- Be sure to add tests.


## License
See [LICENSE](LICENSE)
