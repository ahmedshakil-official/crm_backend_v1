
# CRM Backend

This project is a CRM (Customer Relationship Management) backend built with Django and Django REST Framework. The application is containerized using Docker, making it easy to set up and deploy across different environments.

## Prerequisites

Ensure that the following are installed:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Getting Started

### 1. Fork the Repository

Fork this repository and navigate into the project directory

### 2. Configure Environment Variables

Create a `.env` file in the project root to store environment variables. Use `.env.example` as a template:

```plaintext
# .env
DEBUG=1
SECRET_KEY=your_secret_key
DATABASE_NAME=your_db_name
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
REDIS_URL=redis://redis:6379/0
```

### 3. Build and Start Docker Containers

Build the Docker image and start the containers with Docker Compose:

```bash
docker-compose up --build
```

This command:
- Builds the Docker image using the `Dockerfile`.
- Starts services defined in `docker-compose.yml`, including PostgreSQL, Redis, and Celery.

### 4. Apply Migrations and Create a Superuser

With the containers running, apply migrations and create a Django superuser in a new terminal tab.

1. **Run Migrations**

   ```bash
   docker-compose exec web python manage.py migrate
   ```

2. **Create a Superuser**

   ```bash
   docker-compose exec web python manage.py createsuperuser
   ```

### 5. Access the Application

Once the application is running, access it via:

- **Django Admin**: [http://localhost:8000/admin](http://localhost:8000/admin)
- **API Endpoints**: [http://localhost:8000/api/](http://localhost:8000/api/)

## Code Formatting with Black

This project uses the `black` code formatter to maintain consistent code style. Please format code with `black` before committing changes.

To install and use `black`:

1. **Install Black**

   ```bash
   pip install black
   ```

2. **Format Code**

   ```bash
   black .
   ```

## Running Tests

Run tests using Docker:

```bash
docker-compose exec web python manage.py test
```

## Project Structure

```
crm_backend/
├── app/                        # Django application directory
├── requirements/               # Python dependencies
│   ├── development.txt
│   └── production.txt
├── Dockerfile                  # Dockerfile for building the app image
├── docker-compose.yml          # Docker Compose configuration
├── .env.example                # Example environment file
└── README.md                   # Project README
```

## Additional Docker Commands

- **Stop all containers:**

  ```bash
  docker-compose down
  ```

- **Rebuild and restart containers:**

  ```bash
  docker-compose up --build
  ```

- **View logs:**

  ```bash
  docker-compose logs -f
  ```

## Troubleshooting

- If database errors occur, verify that the database configuration in `.env` aligns with the PostgreSQL setup in `docker-compose.yml`.
- For migration issues, delete old migrations and re-run `makemigrations` and `migrate`.

## License

This project is licensed under the MIT License.

---

This README file provides setup and usage instructions for running the CRM backend application using Docker. Happy coding!
