# InventoryAPIs

A demonstration code of Django-REST APIs for CRUD operations, JWT authentication and Redis caching. For database PostgreSQL is used.

## Table of Contents
- [Installation](#installation)
  - [Docker Setup](#docker-setup)
  - [Project Setup](#project-setup)

- [Test](#test)


## Installation

The database used in the project is PostgreSQL. It can also be used with MySQL by configuring the settings.py accordingly.

### Docker Setup

This project requires a Redis server. You can use Docker to set up and run a Redis container:

1. Install Docker on your system if you haven't already. You can download it from the official [Docker website](https://www.docker.com/get-started).

2. Open a terminal or command prompt and run the following command to start a Redis container:

   ```
   docker run -d --name redis-server -p 6390:6379 redis
   ```

   This will pull the latest Redis image from Docker Hub and start a new container named `redis-server`. The `-p 6390:6379` option maps the container's Redis port 6379 to the host's port 6390, so your application can connect to the Redis server.

3. Verify that the Redis container is running:

   ```
   docker ps
   ```

   You should see the `redis-server` container in the list.

### Project Setup

1. Clone the project repository:

   ```
   git clone https://github.com/your-username/project-name.git
   ```

2. Navigate to the project directory:

   ```
   cd project-name
   ```

3. Install the project dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up the environment variables:

   - Create a `.env` file in the project root directory.
   - Add the necessary environment variables, such as the Redis connection details.

5. Run the project:

   ```
   python app.py
   ```

   This will start the application and connect it to the Redis server running in the Docker container.

## Test

To run the test cases


   ```
   python manage.py test
   ```


