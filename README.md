# Library Django API

This is a Django-based API for managing a library system. The API allows users to manage books, authors, and favorites. Users can also search for books, view book details, add books to their favorites, and receive recommendations based on their favorite books.

## Features
- **Book Management**: Add, view, and update books in the library.
- **Author Management**: Associate books with authors.
- **Favorite Books**: Users can add/remove books to/from their favorites list.
- **Recommendations**: Based on the user's favorite books, the system recommends similar books.
- **Search**: Users can search for books by title or author.
- **User Authentication**: Built-in user authentication for secure access.

## Requirements
- Python 3.8 or higher
- Django 3.2.23
- Django Rest Framework
- PostgreSQL (or any database of your choice)
- Virtual Environment (for isolation)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Mohamed-Ahmed-12/Library-django-API.git

2. Navigate to the project directory:

cd Library-django-API

3. Create a virtual environment and activate it:

For Windows:

python -m venv env
env\Scripts\activate

For Mac/Linux:

python3 -m venv env
source env/bin/activate

4. Install the required dependencies:

pip install -r requirements.txt

5. Set up the database:

python manage.py migrate

6. Create a superuser (optional, for admin access):

python manage.py createsuperuser

7. Run the development server:

python manage.py runserver

8. Access the API:

The API will be accessible at http://127.0.0.1:8000/. You can start interacting with it via Postman or any HTTP client.
API Endpoints

    GET /books/: Get all books.
    GET /books/{id}/: Get details of a specific book by ID.
    GET /favorites/: Get the user's favorite books and recommendations.
    POST /favorites/{id}/: Add a book to the user's favorites.
    DELETE /favorites/{id}/: Remove a book from the user's favorites.
    GET /search/: Search for books by title or author.

Testing

To test the API, you can use Postman or any other API testing tool. You’ll need to include authentication headers (JWT token) for the routes that require authentication.
Example of Authorization (JWT):

    Login and get token: POST /api/token/
        Provide username and password.
        You will receive an access token and a refresh token.
    Use the access token to authorize API requests.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    Django
    Django Rest Framework
    Postman (for testing API)
