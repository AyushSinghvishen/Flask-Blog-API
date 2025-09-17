# Flask Blog API

A RESTful Blog API built with Flask, enabling users to register, log in, and manage posts and comments securely. The project uses JWT authentication, SQLAlchemy for database management, and supports full CRUD operations for posts and comments. Additionally, it can be containerized with Docker for easy deployment.

---

## Features

- **User Management**: Register and log in with secure password hashing.  
- **JWT Authentication**: Protect routes and manage user sessions.  
- **Posts**: Create, read, update, and delete blog posts.  
- **Comments**: Add and view comments for posts.  
- **Relationships**: Users, posts, and comments are linked via SQLAlchemy relationships.  
- **Error Handling**: Returns proper responses for missing fields, unauthorized access, and not found resources.  
- **Docker Support**: Containerized with Docker for easy deployment across environments.  

---

## API Endpoints

- `POST /V1/register` → Register a new user  
- `POST /V1/login` → Log in and get JWT token  
- `POST /V1/posts` → Create a new post (JWT required)  
- `GET /V1/posts` → Get all posts  
- `GET /V1/post/<post_id>` → Get a single post  
- `PATCH /V1/post/<post_id>` → Update a post (JWT required, owner only)  
- `DELETE /V1/post/<post_id>` → Delete a post (JWT required, owner only)  
- `POST /V1/post/<post_id>/comment` → Add a comment (JWT required)  
- `GET /V1/post/<post_id>/comment` → Get all comments for a post  

---

## Technologies Used

- Python 3.x  
- Flask  
- SQLAlchemy  
- Flask-JWT-Extended  
- Flask-Migrate  
- SQLite (development database)  
- Docker for containerized deployment  

