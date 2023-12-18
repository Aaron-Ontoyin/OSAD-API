# OSAD API

## Introduction
Here's the rewritten version:

OSAD, an acronym for Object Speech and Audio Detection, is a robust API engineered to manage object storage and execute object detection tasks. The API offers endpoints for image uploads, object detection within these images, user authentication management, text to speech and speech to text.

The object detection feature employs sophisticated machine learning algorithms, specifically `fasterrcnn_resnet50_fpn_v2` with weights, `FasterRCNN_ResNet50_FPN_V2_Weights` from the torchvision.models.detection module, to pinpoint and categorize objects in an image. This functionality finds its application in a wide array of areas, ranging from security and surveillance to image tagging and organization.

Designed with an emphasis on performance, scalability, and user-friendliness, the API boasts a comprehensive set of features while preserving a straightforward and intuitive interface.


## End Points

## Object Detection

### Endpoint: `POST /object-detection/detect-image`

This endpoint allows you to detect objects in an image.

#### Request

The request should be a `POST` request with the image file included in the form data. The image file should be associated with the key `image`.

The request should also include an `Authorization` header with a bearer token.

Example:

```bash
curl -X POST -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -F "image=@test_img.jpeg" http://localhost:5000/object-detection/detect-image
```

#### Response

The response will be a JSON object with the following keys:

- `detected_objs`: An object containing information about the detected objects. This object has the following keys:
  - `detected_as`: A list of the types of objects detected in the image.
  - `description`: A string describing the number of objects detected in the image.
- `img_url`: The URL of the uploaded image.

Example:

```json
{
  "detected_objs": {
    "detected_as": ["bird"],
    "description": "1 object(s) detected in the image"
  },
  "img_url": "http://localhost:5000/images/test_img.jpeg"
}
```

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and objects were detected in the image.
- `400`: The request was malformed. This could be due to not including an image in the request, or not including an `Authorization` header.
- `500`: There was an error processing the request on the server.

### Endpoint: `GET /object-detection/image`

This endpoint allows you to retrieve information about a previously processed image.

#### Request

The request should be a `GET` request with the `image_id` included in the JSON body. The `image_id` should be the ID of the image you want to retrieve information about.

The request should also include an `Authorization` header with a bearer token.

Example:

```bash
curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"image_id": 1}' -H "Content-Type: application/json" http://localhost:5000/object-detection/image
```

#### Response

The response will be a JSON object with the following keys:

- `detected_as`: A list of the types of objects detected in the image.
- `description`: A string describing the number of objects detected in the image.
- `user_id`: The ID of the user who uploaded the image.
- `url`: The URL of the uploaded image.

Example:

```json
{
  "detected_as": ["bird"],
  "description": "1 object(s) detected in the image",
  "user_id": 1,
  "url": "http://localhost:5000/images/test_img.jpeg"
}
```

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and information about the image was retrieved.
- `400`: The request was malformed. This could be due to not including an `image_id` in the request, or not including an `Authorization` header.
- `404`: The image with the provided `image_id` was not found.
- `500`: There was an error processing the request on the server.

### Endpoint: `GET /object-detection/images`

This endpoint allows you to retrieve information about all previously processed images by the current user.

#### Request

The request should be a `GET` request with no body.

The request should include an `Authorization` header with a bearer token.

Example:

```bash
curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:5000/object-detection/images
```

#### Response

The response will be a JSON array where each item is a JSON object with the following keys:

- `id`: The ID of the image.
- `detected_as`: A list of the types of objects detected in the image.
- `description`: A string describing the number of objects detected in the image.
- `user_id`: The ID of the user who uploaded the image.
- `url`: The URL of the uploaded image.

Example:

```json
[
  {
    "id": 1,
    "detected_as": ["bird"],
    "description": "1 object(s) detected in the image",
    "user_id": 1,
    "url": "http://localhost:5000/images/test_img.jpeg"
  },
  {
    "id": 2,
    "detected_as": ["cat"],
    "description": "1 object(s) detected in the image",
    "user_id": 1,
    "url": "http://localhost:5000/images/test_img2.jpeg"
  }
]
```

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and information about the images was retrieved.
- `400`: The request was malformed. This could be due to not including an `Authorization` header.
- `500`: There was an error processing the request on the server.

### Endpoint: `DELETE /object-detection/image`

This endpoint allows you to delete a previously processed image.

#### Request

The request should be a `DELETE` request with the `image_id` included in the JSON body. The `image_id` should be the ID of the image you want to delete.

The request should also include an `Authorization` header with a bearer token.

Example:

```bash
curl -X DELETE -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"image_id": 1}' -H "Content-Type: application/json" http://localhost:5000/object-detection/image
```

#### Response

If the image is successfully deleted, the server will return a response with a 204 status code and no content.

If the image with the provided `image_id` is not found, the server will return a response with a 404 status code and a JSON object with the following key:

- `msg`: A string with the value "Image not found".

Example:

```json
{
  "msg": "Image not found"
}
```

#### Status Codes

The API can return the following status codes:

- `204`: The request was successful, and the image was deleted.
- `400`: The request was malformed. This could be due to not including an `image_id` in the request, or not including an `Authorization` header.
- `404`: The image with the provided `image_id` was not found.
- `500`: There was an error processing the request on the server.


## Text Audio Processing

### Endpoint: `POST /tap/process-text`

This endpoint allows you to process text and produce its audio equivalent.

#### Request

The request should be a `POST` request with the `text` included in the JSON body. The `text` should be the text you want to convert to audio.

The request should also include an `Authorization` header with a bearer token.

Example:

```bash
curl -X POST -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"text": "Hello, world!"}' -H "Content-Type: application/json" http://localhost:5000/tap/process-text
```

#### Response

The response will be a JSON object with the following keys:

- `text`: The original text that was processed.
- `audio_url`: The URL of the audio file that was produced.

Example:

```json
{
  "text": "Hello, world!",
  "audio_url": "http://localhost:5000/audio_files/hello_world.mp3"
}
```

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and the text was processed.
- `400`: The request was malformed. This could be due to not including `text` in the request, or not including an `Authorization` header.
- `500`: There was an error processing the request on the server.

### Endpoint: `POST /tap/process-audio`

This endpoint allows you to process audio and produce its text equivalent.

#### Request

The request should be a `POST` request with the audio file included in the form data. The audio file should be associated with the key `audio`.

The request should also include an `Authorization` header with a bearer token.

Example:

```bash
curl -X POST -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -F "audio=@test_audio.mp3" http://localhost:5000/tap/process-audio
```

#### Response

The response will be a JSON object with the following keys:

- `audio_url`: The URL of the original audio file that was processed.
- `text`: The text that was produced from the audio file.

Example:

```json
{
  "audio_url": "http://localhost:5000/audio_files/test_audio.mp3",
  "text": "Hello, world!"
}
```

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and the audio was processed.
- `400`: The request was malformed. This could be due to not including an audio file in the request, or not including an `Authorization` header.
- `500`: There was an error processing the request on the server.

### Endpoint: `GET /tap/audios-texts`

This endpoint allows you to retrieve information about all previously processed audio files by the current user.

#### Request

The request should be a `GET` request with no body.

The request should include an `Authorization` header with a bearer token.

Example:

```bash
curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:5000/tap/audios-texts
```

#### Response

The response will be a JSON array where each item is a JSON object with the following keys:

- `id`: The ID of the audio file.
- `text`: The text that was produced from the audio file.
- `audio_url`: The URL of the original audio file that was processed.
- `processed_on`: The date and time when the audio file was processed.

Example:

```json
[
  {
    "id": 1,
    "text": "Hello, world!",
    "audio_url": "http://localhost:5000/audio_files/test_audio.mp3",
    "processed_on": "2022-01-01T00:00:00Z"
  },
  {
    "id": 2,
    "text": "Goodbye, world!",
    "audio_url": "http://localhost:5000/audio_files/test_audio2.mp3",
    "processed_on": "2022-01-02T00:00:00Z"
  }
]
```

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and information about the audio files was retrieved.
- `400`: The request was malformed. This could be due to not including an `Authorization` header.
- `500`: There was an error processing the request on the server.

### Endpoint: `GET /tap/audio-text`

This endpoint allows you to retrieve information about a specific previously processed audio file.

#### Request

The request should be a `GET` request with the `audio_text_id` included in the JSON body. The `audio_text_id` should be the ID of the audio file you want to retrieve information about.

The request should also include an `Authorization` header with a bearer token.

Example:

```bash
curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"audio_text_id": 1}' -H "Content-Type: application/json" http://localhost:5000/tap/audio-text
```

#### Response

The response will be a JSON object with the following keys:

- `id`: The ID of the audio file.
- `text`: The text that was produced from the audio file.
- `audio_url`: The URL of the original audio file that was processed.
- `processed_on`: The date and time when the audio file was processed.

Example:

```json
{
  "id": 1,
  "text": "Hello, world!",
  "audio_url": "http://localhost:5000/audio_files/test_audio.mp3",
  "processed_on": "2022-01-01T00:00:00Z"
}
```

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and information about the audio file was retrieved.
- `400`: The request was malformed. This could be due to not including an `audio_text_id` in the request, or not including an `Authorization` header.
- `404`: The audio file with the provided `audio_text_id` was not found.
- `500`: There was an error processing the request on the server.

### Endpoint: `DELETE /tap/audio-text`

This endpoint allows you to delete a specific previously processed audio file.

#### Request

The request should be a `DELETE` request with the `audio_text_id` included in the JSON body. The `audio_text_id` should be the ID of the audio file you want to delete.

The request should also include an `Authorization` header with a bearer token.

Example:

```bash
curl -X DELETE -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"audio_text_id": 1}' -H "Content-Type: application/json" http://localhost:5000/tap/audio-text
```

#### Response

If the audio file is successfully deleted, the server will return a response with a 204 status code and no content.

If the audio file with the provided `audio_text_id` is not found, the server will return a response with a 404 status code and a JSON object with the following key:

- `msg`: A string with the value "Audio Text not found".

Example:

```json
{
  "msg": "Audio Text not found"
}
```

#### Status Codes

The API can return the following status codes:

- `204`: The request was successful, and the audio file was deleted.
- `400`: The request was malformed. This could be due to not including an `audio_text_id` in the request, or not including an `Authorization` header.
- `404`: The audio file with the provided `audio_text_id` was not found.
- `500`: There was an error processing the request on the server.


## Authentication

### Endpoint: `POST /auth/register`

This endpoint allows you to register a new user.

#### Request

The request should be a `POST` request with the `username`, `email`, and `password` included in the JSON body.

Example:

```bash
curl -X POST -d '{"username": "testuser", "email": "testuser@example.com", "password": "testpassword"}' -H "Content-Type: application/json" http://localhost:5000/auth/register
```

#### Response

If the registration is successful, the server will return a response with a 201 status code and a JSON object with the following key:

- `message`: A string with the value "User created successfully".

If the username or email already exists, the server will return a response with a 400 status code and a JSON object with the following key:

- `message`: A string with the value "Username or email already exists".

If any of the required fields (`username`, `email`, `password`) are missing, the server will return a response with a 400 status code and a JSON object with the following key:

- `message`: A string with the value "Missing fields: {fields}", where `{fields}` is a comma-separated list of the missing fields.

#### Status Codes

The API can return the following status codes:

- `201`: The request was successful, and the user was registered.
- `400`: The request was malformed. This could be due to missing fields, or a username or email that already exists.
- `500`: There was an error processing the request on the server.

### Endpoint: `POST /auth/login`

This endpoint allows you to log in an existing user.

#### Request

The request should be a `POST` request with the `username` and `password` included in the JSON body.

Example:

```bash
curl -X POST -d '{"username": "testuser", "password": "testpassword"}' -H "Content-Type: application/json" http://localhost:5000/auth/login
```

#### Response

If the login is successful, the server will return a response with a 200 status code and a JSON object with the following keys:

- `msg`: A string with the value "Login successful".
- `access_token`: The access token for the user.
- `refresh_token`: The refresh token for the user.

If the username is not found or the password is incorrect, the server will return a response with a 401 status code and a JSON object with the following key:

- `msg`: A string with the value "Invalid username" or "Invalid password" respectively.

If any of the required fields (`username`, `password`) are missing, the server will return a response with a 400 status code and a JSON object with the following key:

- `msg`: A string with the value "Missing required fields".

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and the user was logged in.
- `400`: The request was malformed. This could be due to missing fields.
- `401`: The username was not found or the password was incorrect.
- `500`: There was an error processing the request on the server.

### Endpoint: `DELETE /auth/logout`

This endpoint allows you to log out the current user by revoking their JWT access token and associated refresh tokens.

#### Request

The request should be a `POST` request with no body.

The request should include an `Authorization` header with a bearer token.

Example:

```bash
curl -X DELETE -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:5000/auth/logout
```

#### Response

If the logout is successful, the server will return a response with a 200 status code and a JSON object with the following key:

- `msg`: A string with the value "{token_type} token successfully revoked", where `{token_type}` is either "Access" or "Refresh" depending on the type of the token that was revoked.

If no current user is found, the server will return a response with a 401 status code and a JSON object with the following key:

- `msg`: A string with the value "No current user found".

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and the user was logged out.
- `401`: No current user was found.
- `500`: There was an error processing the request on the server.

### Endpoint: `GET /auth/user`

This endpoint allows you to retrieve information about the currently logged-in user.

#### Request

The request should be a `GET` request with no body.

The request should include an `Authorization` header with a bearer token.

Example:

```bash
curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:5000/auth/user
```

#### Response

The response will be a JSON object with the following keys:

- `username`: The username of the user.
- `email`: The email of the user.
- `firstname`: The first name of the user.
- `lastname`: The last name of the user.
- `phone`: The phone number of the user.
- `is_admin`: A boolean indicating whether the user is an admin.
- `remaining_requests`: The number of remaining requests the user can make.

Example:

```json
{
  "username": "testuser",
  "email": "testuser@example.com",
  "firstname": "Test",
  "lastname": "User",
  "phone": "1234567890",
  "is_admin": false,
  "remaining_requests": 100
}
```

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and the user information was retrieved.
- `401`: The user is not logged in.
- `500`: There was an error processing the request on the server.

### Endpoint: `PATCH /auth/user`

This endpoint allows you to update the information of the currently logged-in user.

#### Request

The request should be a `PUT` request with the fields you want to update included in the JSON body. The fields can be any of the following: `username`, `email`, `firstname`, `lastname`, `phone`.

The request should include an `Authorization` header with a bearer token.

Example:

```bash
curl -X PATCH -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"firstname": "NewFirstName", "lastname": "NewLastName"}' -H "Content-Type: application/json" http://localhost:5000/auth/user
```

#### Response

If the update is successful, the server will return a response with a 200 status code and a JSON object with the updated user information.

If the user is not found, the server will return a response with a 404 status code and a JSON object with the following key:

- `msg`: A string with the value "User not found".

If any of the fields are invalid, the server will return a response with a 400 status code and a JSON object with the following key:

- `msg`: A string with the value "Invalid fields".

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and the user information was updated.
- `400`: The request was malformed. This could be due to invalid fields.
- `404`: The user was not found.
- `500`: There was an error processing the request on the server.

### Endpoint: `DELETE /auth/user`

This endpoint allows you to delete the currently logged-in user.

#### Request

The request should be a `DELETE` request with no body.

The request should include an `Authorization` header with a bearer token.

Example:

```bash
curl -X DELETE -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:5000/auth/user
```

#### Response

If the deletion is successful, the server will return a response with a 204 status code and no content.

If the user is not found, the server will return a response with a 404 status code and a JSON object with the following key:

- `msg`: A string with the value "User not found".

#### Status Codes

The API can return the following status codes:

- `204`: The request was successful, and the user was deleted.
- `401`: The user is not logged in.
- `404`: The user was not found.
- `500`: There was an error processing the request on the server.

### Endpoint: `PATCH /auth/change-password`

This endpoint allows you to change the password of the currently logged-in user.

#### Request

The request should be a `PUT` request with the `old_password` and `new_password` included in the JSON body.

The request should include an `Authorization` header with a bearer token.

Example:

```bash
curl -X PATCH -H "Authorization: Bearer YOUR_ACCESS_TOKEN" -d '{"old_password": "oldpassword", "new_password": "newpassword"}' -H "Content-Type: application/json" http://localhost:5000/auth/change-password
```

#### Response

If the password change is successful, the server will return a response with a 200 status code and a JSON object with the following key:

- `msg`: A string with the value "Password changed successfully".

If the old password is incorrect, the server will return a response with a 401 status code and a JSON object with the following key:

- `msg`: A string with the value "Invalid old password".

If any of the required fields (`old_password`, `new_password`) are missing, the server will return a response with a 400 status code and a JSON object with the following key:

- `msg`: A string with the value "Missing required fields".

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and the password was changed.
- `400`: The request was malformed. This could be due to missing fields.
- `401`: The old password was incorrect.
- `500`: There was an error processing the request on the server.

### Endpoint: `GET /auth/password-reset-token`

This endpoint allows you to request a password reset token for a user.

#### Request

The request should be a `POST` request with the `email` included in the JSON body.

Example:

```bash
curl -X GET -d '{"email": "testuser@example.com"}' -H "Content-Type: application/json" http://localhost:5000/auth/password-reset-token
```

#### Response

If the email is found, the server will generate a password reset token, store it in Redis with an expiration time of 30 minutes, and send an email to the user with the token. The server will return a response with a 200 status code and a JSON object with the following key:

- `msg`: A string with the value "Password reset token sent to {email}", where `{email}` is the user's email.

If the email is not found, the server will return a response with a 404 status code and a JSON object with the following key:

- `msg`: A string with the value "User not found with email {email}", where `{email}` is the user's email.

If the `email` field is missing, the server will return a response with a 400 status code and a JSON object with the following key:

- `msg`: A string with the value "Missing required field: email".

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and the password reset token was sent.
- `400`: The request was malformed. This could be due to the missing `email` field.
- `404`: The user was not found.
- `500`: There was an error processing the request on the server.

### Endpoint: `PATCH /auth/reset-password`

This endpoint allows you to reset a user's password using a password reset token.

#### Request

The request should be a `POST` request with the `token` and `password` included in the JSON body.

Example:

```bash
curl -X PATCH -d '{"token": "your-reset-token", "password": "newpassword"}' -H "Content-Type: application/json" http://localhost:5000/auth/reset-password
```

#### Response

If the password reset is successful, the server will return a response with a 200 status code and a JSON object with the following key:

- `msg`: A string with the value "Password reset successful".

If the token is invalid or expired, the server will return a response with a 400 status code and a JSON object with the following key:

- `msg`: A string with the value "Invalid or expired token".

If any of the required fields (`token`, `password`) are missing, the server will return a response with a 400 status code and a JSON object with the following key:

- `msg`: A string with the value "Missing required fields".

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and the password was reset.
- `400`: The request was malformed. This could be due to missing fields or an invalid or expired token.
- `500`: There was an error processing the request on the server.

### Endpoint: `GET /auth/refresh-token`

This endpoint allows you to refresh the access token of the currently logged-in user.

#### Request

The request should be a `POST` request with no body.

The request should include an `Authorization` header with a bearer token.

Example:

```bash
curl -X GET -H "Authorization: Bearer YOUR_REFRESH_TOKEN" http://localhost:5000/auth/refresh-token
```

#### Response

If the refresh is successful, the server will return a response with a 200 status code and a JSON object with the following key:

- `access_token`: The new access token.

Example:

```json
{
  "access_token": "new_access_token"
}
```

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and the access token was refreshed.
- `401`: The user is not logged in or the refresh token is invalid.
- `500`: There was an error processing the request on the server.

### Endpoint: `GET /auth/users`

This endpoint allows you to retrieve information about all users if the requester is an admin.

#### Request

The request should be a `GET` request with no body.

The request should include an `Authorization` header with a bearer token.

Example:

```bash
curl -X GET -H "Authorization: Bearer YOUR_ACCESS_TOKEN" http://localhost:5000/auth/users
```

#### Response

The response will be a JSON object with the following keys:

- `users`: An array of user objects. Each user object contains the following keys:
  - `username`: The username of the user.
  - `email`: The email of the user.

Example:

```json
{
  "users": [
    {
      "username": "testuser1",
      "email": "testuser1@example.com"
    },
    {
      "username": "testuser2",
      "email": "testuser2@example.com"
    }
  ]
}
```

#### Status Codes

The API can return the following status codes:

- `200`: The request was successful, and the user information was retrieved.
- `401`: The user is not logged in or is not an admin.
- `500`: There was an error processing the request on the server.


## Common Errors and Troubleshooting

This section provides information on common errors you might encounter while using the OSAD API, along with potential solutions.

- `401 Unauthorized`: This usually means that your access token is missing or invalid. Make sure you're including the `Authorization` header with a valid token in your requests.
- `404 Not Found`: This means the endpoint you're trying to reach doesn't exist. Check the endpoint URL to make sure it's correct.
- `500 Internal Server Error`: This means something went wrong on our end. If the problem persists, please contact our support team.

## Best Practices

Here are some best practices to follow when using the OSAD API:

- Always include the `Authorization` header with your access token in your requests.
- Handle errors gracefully in your application. Check the status code and message in the API response to understand what went wrong.
- Use the appropriate HTTP methods for each endpoint. For example, use `GET` to retrieve data and `POST` to send data.

## Conclusion

That's it! You're now ready to start using the OSAD API. If you have any questions or run into any issues, see me at the contact section below. Happy coding!

## Contact Information

If you have any questions, issues, or feedback regarding the OSAD API, feel free to reach out:

- Email: aarononto909@gmail.com, aarononto@virtual-world.tech
- GitHub: https://github.com/Aaron-Ontoyin
- LinkedIn: https://linkedin.com/in/aarononto
