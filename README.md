# Rico's FilmLog (GDGoC study case)
FilmLog is a movie management web application built with *Python, Flask, and PostgreSQL*. It allows users to explore movies, manage personal watchlists, track watched movies, write reviews, and receive personalized recommendations powered by Google's Gemini AI.
The project demonstrates RESTful API development, JWT-based authentication, relational database management, AI integration, and cloud deployment.
## Features
### 1. User Authentication
- User registration and login.
- JWT-based authentication for protected endpoints.
- Secure password hashing and salting using Werkzeug.
- User-specified data access.
### 2. Movie Catalog
- Browse a collection of 20 preloaded movies.
- Retrieve detailed movie information by ID.
- View movie metadata, including titles, genres, directors, ratings, synopsis, and cast members.
### 3. Personal Watchlist
- Add movies to a personal watchlist.
- View all saved movies.
- Remove movies from the watchlist.
- Prevent duplicate entries for the same user and movie.
### 4. Watched Movies and Reviews
- Track movies that have been watched.
- Submit a personal rating from 1 to 5.
- Write reviews for watched movies.
- Retrieve personal reviews and watched movie history
- Prevent multiple reviews of the same movie by the same user.
### 5. AI Movie Recommendation
- Receive personalized movie recommendations based on natural-language preferences.
- Integrate Google's Gemini API for recommendation generation.
- Restrict recommendations to movies already available in the database.
- Provide an AI-generated explanation for each recommendation.
  
## Tech Stack
|Category |Technology |
| --- | --- |
|Programming Language |Python | 
|Backend Framework |Flask |
|ORM |Flask-SQLAlchemy |
|Database |SQLite/PostgreSQL |
|Database Hosting |Neon |
|Authentication |Flask-JWT-Extended |
|Password Security |Werkzeug |
|AI Integration |Google Gemini API |
|Data Validation |Pydantic |
|Frontend |HTML, CSS, JavaScript |
|Deployment |Vercel |
|API Testing & Documentation |Postman |
|Version Control |Github |

## System Architecture
FilmLog uses a client-server architecture.
The frontend communicates with the Flask backend through HTTP requests. The backend handles authentication, business logic, and database operations using SQLAlchemy.
User information, movie details, watchlists, and reviews are stored in a PostgreSQL database hosted on Neon.
For AI recommendations,  the backend sends the available movie catalog and the user's preferences to Gemini. The returned movie ID is then validated against the database before the recommendation is sent to the frontend.
#### Application Flow:
User
 |
 v
Frontend (HTML, CSS, JS)
 |
 v
Flask REST API
 |
 + - > JWT Authentication
 |
 + - > SQLAlchemy ORM
 |           |
 |           v
 |      PostgreSQL (Neon)
 + - > Gemini API
           |
           v
      AI Recommendation
Deployment: Vercel

## Database Design
FilmLog uses a relational database consistng of four main tables
### Users
Stores registered users' information
- id - Primary key
- Username - Username
- email - Unique email address
- password_hash - Salted password hash
### Movies
Stores the movie catalog.
- id - Primary key
- title - Movie title
- year - Release year
- director - Director
- genres - List of genres
- rating - Movie rating
- duration - Movie duration
- synopsis - Movie description
- poster_url - Movie poster URL
- cast - List of actors
### Watchlists
Stores movies saved by individual users.
- id - Primary key
- user_id - Foreign key referencing Users
- movie_id - Foreign key referencing Movies
Added unique constraint on user_id and movie_id to prevent duplicate watchlist entries.
### Reviews
Stored watched movies and user reviews.
- id - Primary key
- user_id - Foreign key referencing Users
- movie_id - Foreign key referencing Movies
- rating - Personal rating
- review - Written review
- created_at - Review creation timestamp
Added unique constraint on user_id and movie_id prevents duplicate reviews.
### Relationshiops
- One user can have multiple watchlist entries.
- One movie can appear in multiple users' watchlists.
- One user can write multiple reviews for different movies.
- One movie can receive multiple reviews from multiple users.
### ERD
<img width="667" height="747" alt="image" src="https://github.com/user-attachments/assets/25792855-50e9-46a9-9cd2-4073de55439a" />


## REST API Endpoints
FilmLog has 10 API endpoints.
#### Authentication
|**Methods**|**Endpoint**|**Description**|**Authentication**|
|---|---|---|---|
|POST|/api/auth/register|Register a new user|No|
|POST|/api/auth/login|Authenticate a user and generate a JWT|No|
#### Movies
|**Methods**|**Endpoint**|**Description**|**Authentication**|
|---|---|---|---|
|GET|/api/movies|Retrieve all movies|No|
|GET|/api/movies/{id}|Retrieve movie details|No|
#### Watchlist
|**Methods**|**Endpoint**|**Description**|**Authentication**|
|---|---|---|---|
|GET|/api/watchlist|Retrieve personal watchlist|Yes|
|POST|/api/watchlist|Add movie to watchlist|Yes|
|DELETE|/api/watchlist/{movie_id}|Remove movie from watchlist|Yes|
#### Watched & Reviews
|**Methods**|**Endpoint**|**Description**|**Authentication**|
|---|---|---|---|
|GET|/api/watched|Retrieve watched movies and reviews|Yes|
|POST|/api/watched|Add a watched movie and review|Yes|
#### Gemini AI Recommendation
|**Methods**|**Endpoint**|**Description**|**Authentication**|
|---|---|---|---|
|POST|/api/movies/recommend|Generate personalized movie recommendation|No|
### API Documentation
Detailed API documentation including request bodies, authentication requirements, example responses, and HTTP status codes, is available in Postman.

## Authentication and Security
FilmLog uses JWT (JSON Web Tokens) to authenticate users and protect personal data.
After logging in, users receive an access token which must be included in requests to protected endpoints.
#### Example Authorization Header:
`Authorization: Bearer YOUR_ACCESS_TOKEN`
Passwords are hashed and salted using Werkzeug before being stored. Original password is not stored.
User-specified endpoints retrieve the authenticated user's identity from the JWT, which prevent users from selecting another user's watchlist or reviews through a supplied user ID.
Database foreign key and unique constraints help maintain users' data integrity.

## Gemini AI Recommendation Workflow
1. The user submits a natural-language description of their movie preferences.
2. The flask backend retrieves the available movie catalog from PostgreSQL.
3. The movie catalog and user preferences are sent to Gemini.
4. Gemini generates a structured response containing a movie ID and reasoning.
5. The backend validates whether the recommended movie exists in the database.
6. If the recommended movie exists in the database, the movie details and recommendation reasoning are returned to the user.
#### Example Request:
{
  "prompt": "I want a cartoonish movie with robot in it."
}
The AI is instructed to recommend only one movie from FilmLog's existing catalog. Backend validation is used as an additional check against unsupported movie IDs.

## Installation and Setup
### Prerequisites
- Python
- Git
- A PostgreSQL database, such as Neon
- A Google Gemini API key
#### 1. Clone this Repository
`git clone github.com/herminono/filmlog-GDGoC`
`cd github.com/herminono/filmlog-GDGoC`
#### 2. Create a Virtual Environment
`python -m venv .venv`
Activate it on Windows:
`.venv\Scripts\activate`
#### 3. Install Dependencies
`pip install -r requirements.txt`
#### 4. Configure Environment Variables
Create a .env file in the project root directory.
`DATABASE_URL=YOUR_POSTGRESQL_CONNECTION_STRING`
`JWT_SECRET_KEY=YOUR_SECRET_KEY`
`GEMINI_API_KEY=YOUR_GEMINI_API_KEY`
Replace the placeholders with your own credentials.
#### 5. Initialize the Database
Run the database initialization script:
`python init__db.py`
Seed the movie catalog:
`python seed.py`
#### 6. Run the Application
`python main.py`
Open the URL in the terminal to access the application.

## Deployment
FilmLog is deployed on *Vercel*, with PostgreSQL on *Neon*.
Environment variables are configured through the Vercel project settings.
The application communicates with the Neon database using SQLAlchemy and the PostgreSQL driver.
Live Demo: https://filmlog-gdgoc.vercel.app

## API Testing
The REST API was tested using Postman.
Testing scenarios include:
- Successful and unsuccessful user registration and login.
- Movie retrieval
- Authorized and unauthorized watchlist access.
- Adding and removing watchlist entries.
- Duplicated watchlist prevention.
- Rating and review input validation.
- Duplicate review prevention.
- AI recommendation requests and input validation.
API responses use HTTP status codes to indicate successful operations and error conditions.

## Possible Improvements
- Updating and deleting submitted reviews.
- Monitoring and application performance.
- Larger movie catalog using TMDB API.

## Project Information
**Project Name**: Rico's FilmLog (GDGoC study case)
**Project Type**: REST API and Movie Management Web Application
**Purpose**: Backend Development Study Case Assignment
**Repository**: https://github.com/herminono/filmlog-GDGoC
**Live Deployment**: https://filmlog-gdgoc.vercel.app
**API Documentation**: https://documenter.getpostman.com/view/59293580/2sBYHYuJEE
