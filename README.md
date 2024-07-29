# Connectify

## About
Connectify is a social media application designed using a microservice architecture, providing two primary services: user management and post management.

## Setup

1. **Grant Executable Permission to the `permissions.sh` Script**
   ```bash
   connectify$ sudo chmod +x permissions.sh
   ```
   The above command grants executable permission to the `permissions.sh` script.

2. **Run the `permissions.sh` Script**
   ```bash
   connectify$ ./permissions.sh
   ```
   The above command executes the `permissions.sh` script. This script grants executable permissions to other scripts and runs the `dependencies.sh` script, which installs the necessary OS-level dependencies.
   > **Note:** The system will reboot after running this command.

3. **Install Project-Level Dependencies**
   ```bash
   connectify$ ./setup.sh
   ```
   The above command installs the project-level dependencies and completes the setup process.



### 1. Low-Level Design (LLD)

**User Service:**

- **User Model:**
  - Attributes: `id`, `username`, `email`, `password`, `followers` (many-to-many relationship with `User`), etc.
  - Methods: `create_user()`, `update_user()`, `delete_user()`, etc.

- **Views:**
  - **UserViewSet:**
    - **List Users:** Handles GET requests to list all users.
    - **Create User:** Handles POST requests to create a new user.
    - **Retrieve User:** Handles GET requests for a specific user.
    - **Update User:** Handles PUT requests to update a specific user.
    - **Delete User:** Handles DELETE requests to remove a user.
    - **Follow User:** Handles POST requests to follow a user.
    - **Unfollow User:** Handles POST requests to unfollow a user.

- **Serializers:**
  - **UserSerializer:** Serializes user data for creating, updating, and retrieving users.
  - **FollowSerializer:** Serializes follow/unfollow actions.

- **Authentication & Authorization:**
  - JWT Authentication is set up using `rest_framework_simplejwt`.
  - Custom permission classes for access control.

**Post Service:**

- **Post Model:**
  - Attributes: `id`, `author` (foreign key to `User`), `content`, `views`, `hashtags` (many-to-many relationship with `Hashtag`), etc.
  - Methods: `create_post()`, `update_post()`, `delete_post()`, etc.

- **Views:**
  - **DiscussionViewSet:**
    - **List Discussions:** Handles GET requests to list all discussions.
    - **Create Discussion:** Handles POST requests to create a new discussion.
    - **Retrieve Discussion:** Handles GET requests for a specific discussion.
    - **Update Discussion:** Handles PUT requests to update a specific discussion.
    - **Delete Discussion:** Handles DELETE requests to remove a discussion.
    - **Add View to Discussion:** Handles POST requests to add a view to a discussion.

  - **CommentViewSet:**
    - **List Comments:** Handles GET requests to list all comments.
    - **Create Comment:** Handles POST requests to create a new comment.
    - **Retrieve Comment:** Handles GET requests for a specific comment.
    - **Update Comment:** Handles PUT requests to update a specific comment.
    - **Delete Comment:** Handles DELETE requests to remove a comment.
    - **Like/Unlike Comment:** Handles POST requests to like or unlike a comment.

  - **HashtagViewSet:**
    - **Search Discussions by Hashtag:** Handles GET requests to search discussions by hashtag.

- **Serializers:**
  - **DiscussionSerializer:** Serializes discussion data for creating, updating, and retrieving discussions.
  - **CommentSerializer:** Serializes comment data for creating, updating, and retrieving comments.
  - **HashtagSerializer:** Serializes hashtag data for searching.

- **Authentication & Authorization:**
  - JWT Authentication is set up using `rest_framework_simplejwt`.

### 2. High-Level Design Document

**Detailed Description of Each Component:**

- **User Service:**
  - **Purpose:** Manages user profiles, authentication, and user relationships (following/unfollowing).
  - **Endpoints:** CRUD operations for users, following and unfollowing users.
  - **Dependencies:** `django.contrib.auth`, `rest_framework`, `rest_framework_simplejwt`.

- **Post Service:**
  - **Purpose:** Manages discussions (posts), comments, and hashtags.
  - **Endpoints:** CRUD operations for discussions and comments, searching by hashtags.
  - **Dependencies:** `django.contrib.auth`, `rest_framework`, `rest_framework_simplejwt`.

**Diagram Illustrating the System Architecture:**


```plaintext
                +------------------+
                |   Client/UI       |
                +--------+---------+
                         |
                         v
                +--------+---------+
                |    API Gateway    |
                +--------+---------+
                         |
              +----------+----------+
              |                     |
              v                     v
   +----------+---------+   +--------+---------+
   |   User Service     |   |   Post Service   |
   |                    |   |                  |
   |  /api/users/       |   |  /api/posts/     |
   |  /api/users/login/ |   |  /api/comments/  |
   |  /api/users/signup/|   |  /api/posts/hashtags/ |
   |  /api/users/follow/|   +--------+---------+
   |  /api/users/unfollow/ |
   +----------+---------+           |
              |                      |
              v                      v
   +----------+---------+    +--------+---------+
   |    User Model      |    |   Post Model     |
   |                    |    |                  |
   |  - id: PK          |    |  - id: PK        |
   |  - username        |    |  - author: FK(User)|
   |  - email           |    |  - content       |
   |  - password        |    |  - views         |
   |  - followers: M2M  |    |  - hashtags: M2M |
   +----------+---------+    +--------+---------+
              |                      |
              v                      v
   +----------+---------+    +--------+---------+
   |  User Database     |    |   Post Database  |
   |                    |    |                  |
   |  +--------------+  |    |  +--------------+|
   |  |    Users     |  |    |  |    Posts     ||
   |  +--------------+  |    |  +--------------+|
   +--------------------+    +------------------+
              |                      |
              v                      v
   +----------+---------+    +--------+---------+
   |  Authentication    |    |  Authorization   |
   |      Service       |    |      Service     |
   |     (JWT)          |    |                  |
   +--------------------+    +------------------+
```

### Description of Components

1. **Client/UI:**
   - **Role:** Provides the user interface for interacting with the system, including user management and post-related actions.

2. **API Gateway:**
   - **Role:** Routes requests from the client to the appropriate service (User Service or Post Service).

3. **User Service:**
   - **Endpoints:**
     - `POST /api/users/` - Create a new user.
     - `PUT /api/users/{id}/` - Update user details.
     - `DELETE /api/users/{id}/` - Delete a user.
     - `GET /api/users/` - List all users.
     - `GET /api/users/?search={name}` - Search users by name.
     - `POST /api/users/login/` - Authenticate user and provide JWT.
     - `POST /api/users/signup/` - Register a new user.
     - `POST /api/users/{id}/follow/` - Follow a user.
     - `POST /api/users/{id}/unfollow/` - Unfollow a user.
   - **Model:**
     - `User Model` - Represents user attributes and relationships.
   - **Database:**
     - `User Database` - Stores user data.

4. **Post Service:**
   - **Endpoints:**
     - `POST /api/posts/` - Create a new discussion post.
     - `PUT /api/posts/{id}/` - Update a post.
     - `DELETE /api/posts/{id}/` - Delete a post.
     - `GET /api/posts/` - List all posts.
     - `GET /api/posts/search/?query={text}` - Search posts by text.
     - `GET /api/posts/hashtags/?query={hashtag}` - Search posts by hashtag.
     - `POST /api/posts/{id}/add_view/` - Add a view to a post.
     - `POST /api/comments/` - Create a comment on a post.
     - `PUT /api/comments/{id}/` - Update a comment.
     - `DELETE /api/comments/{id}/` - Delete a comment.
     - `GET /api/comments/` - List all comments.
     - `POST /api/comments/{id}/like/` - Like or unlike a comment.
   - **Model:**
     - `Post Model` - Represents post attributes and relationships.
   - **Database:**
     - `Post Database` - Stores post and comment data.

5. **Authentication Service (JWT):**
   - **Role:** Issues and validates JSON Web Tokens (JWT) for user authentication.

6. **Authorization Service:**
   - **Role:** Ensures users have the appropriate permissions for specific actions, though this is typically part of the authentication service in simple setups.

### 3. Database Schema

**User Table:**

- **Users**
  - `id`: Integer, Primary Key
  - `username`: String, Unique
  - `email`: String, Unique
  - `password`: String
  - `followers`: Many-to-Many relationship with `User` (self-referencing)

**Post Table:**

- **Posts**
  - `id`: Integer, Primary Key
  - `author`: Foreign Key to `User`
  - `content`: Text
  - `views`: Integer
  - `hashtags`: Many-to-Many relationship with `Hashtags`

- **Comments**
  - `id`: Integer, Primary Key
  - `post`: Foreign Key to `Post`
  - `author`: Foreign Key to `User`
  - `content`: Text
  - `likes`: Integer

- **Hashtags**
  - `id`: Integer, Primary Key
  - `text`: String

**Relationships:**

- **User to Post:** One-to-Many (one user can create many posts).
- **Post to Comment:** One-to-Many (one post can have many comments).
- **Post to Hashtags:** Many-to-Many (one post can have many hashtags and vice versa).

### 4. API Documentation

**User Service Endpoints:**

- **Create User:**
  - **Endpoint:** `POST /api/users/`
  - **Request:** `{"username": "string", "email": "string", "password": "string"}`
  - **Response:** `{"id": "integer", "username": "string", "email": "string"}`

- **Update User:**
  - **Endpoint:** `PUT /api/users/{id}/`
  - **Request:** `{"username": "string", "email": "string", "password": "string"}`
  - **Response:** `{"id": "integer", "username": "string", "email": "string"}`

- **Delete User:**
  - **Endpoint:** `DELETE /api/users/{id}/`
  - **Response:** `204 No Content`

- **List Users:**
  - **Endpoint:** `GET /api/users/`
  - **Response:** `[{"id": "integer", "username": "string", "email": "string"}, ...]`

- **Search User by Name:**
  - **Endpoint:** `GET /api/users/?search={name}`
  - **Response:** `[{"id": "integer", "username": "string", "email": "string"}, ...]`

- **User Login:**
  - **Endpoint:** `POST /api/users/login/`
  - **Request:** `{"username": "string", "password": "string"}`
  - **Response:** `{"access": "string", "refresh": "string"}`

- **User Signup:**
  - **Endpoint:** `POST /api/users/signup/`
  - **Request:** `{"username": "string", "email": "string", "password": "string"}`
  - **Response:** `{"id": "integer", "username": "string", "email": "string"}`

- **Follow User:**
  - **Endpoint:** `POST /api/users/{id}/follow/`
  - **Response:** `200 OK` or `400 Bad Request`

- **Unfollow User:**
  - **Endpoint:** `POST /api/users/{id}/unfollow/`
  - **Response:** `200 OK` or `400 Bad Request`

**Post Service Endpoints:**

- **Create Discussion:**
  - **Endpoint:** `POST /api/posts/`
  - **Request:** `{"author": "integer", "content": "string", "hashtags": ["string"]}`
  - **Response:** `{"id": "integer", "author": "integer", "content": "string", "hashtags": ["string"]}`

- **Update Discussion:**
  - **Endpoint:** `PUT /api/posts/{id}/`
  - **Request:** `{"content": "string", "hashtags": ["string"]}`
  - **Response:** `{"id": "integer", "author": "integer", "content": "string", "hashtags": ["string"]}`

- **Delete Discussion:**
  - **Endpoint:** `DELETE /api/posts/{id}/`
  - **Response:** `204 No Content`

- **List Discussions:**
  - **Endpoint:** `GET /api/posts/`
  - **Response:** `[{"id": "integer", "author": "integer", "content": "string", "hashtags": ["string"]}, ...]`

- **Search Discussions by Text:**
  - **Endpoint:** `GET /api/posts/search/?query={text}`
  - **Response:** `[{"id": "integer", "author": "integer", "content": "string", "hashtags": ["string"]}, ...]`

- **Search Discussions by Hashtag:**
  - **Endpoint:** `GET /api/posts/hashtags/?query={hashtag}`
  - **Response:** `[{"id": "integer", "author": "integer", "content": "string", "hashtags": ["string"]}, ...]`

- **Add View to Discussion:**
  - **Endpoint:** `POST /api/posts/{id}/add_view/`
  - **Response:** `200 OK`

- **Create Comment:**
  - **Endpoint:** `POST /api/comments/`
  - **Request:** `{"post": "integer", "author": "integer", "content": "string"}`
  - **Response:** `{"id": "integer", "post": "integer", "author": "integer", "content": "string"}`

- **Update Comment:**
  - **Endpoint:** `PUT /api/comments/{id}/`
  - **Request:** `{"content": "string"}`
  - **Response:** `{"id": "integer", "post": "integer", "author": "integer", "content": "string"}`

- **Delete Comment:**
  - **Endpoint:** `DELETE /api/comments/{id}/`
  - **Response:** `204 No Content`

- **Like/Unlike Comment:**
  - **Endpoint:** `POST /api/comments/{id}/like/`
  - **Response:** `200 OK`
