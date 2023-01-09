# url-shortener

This project was completed as a coding assessment for [MovingWorlds](movingworlds.org).

## Local Deployment Instructions

The API has been containerized using Docker, and a simple Docker Compose specification has been provided for easy deployment on a development machine. See [this link](https://docs.docker.com/get-docker/) if you need to install Docker. After checking out the repository, simply run

```
docker compose -f /path/to/url-shortener/docker-compose.dev.yml up
```

Then go to `localhost:5000/docs` in your browser to see the interactive API documentation. Note that the `GET /{shortcode}` endpoint will not work interactively due to CORS policies – instead, type `localhost:5000/{shortcode}` into your browser directly to be redirected to the appropriate page.

## Explanation of code

The API has been written using the [Flask web framework for Python](https://flask.palletsprojects.com/en/2.2.x/) as well as its extensions [APIFlask](https://apiflask.com/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/). The provided Docker image serves this API using [Gunicorn](https://gunicorn.org).

The API routes can be found in `./api/app.py`. The API input and output object definitions can be found in `./api/schemas.py`. The ORM definitions for the database schema can be found in `./database/models.py`.

## Steps towards a production deployment

Several considerations must be taken into account before a production server is created for this API.

### Workers and Threads

When run, the provided docker image defaults to serving a single worker that uses a single thread to handle incoming requests. That is, there is no application concurrency by default. Depending on server hardware and expected traffic, workers should be configured via [Gunicorn command line arguments](https://docs.gunicorn.org/en/latest/settings.html#worker-processes) when running the API container.

### HTTP Reverse Proxy

Setting up an HTTP Reverse Proxy like Nginx is essential to deploying a scalable and secure backend service. Whether the proxy manages traffic for all production servers or for each individual server depends on how load balancing will be managed as the application scales.

### Database deployment

I wrote code for this API as naively towards database deployment as possible, only requiring that PostgreSQL be used and not hardcoding any specific multistep authentication other than database URI username/password. Managing a reliable, secure, and scalable database instance is an essential step before the API can be deployed on top of it. Using an Docker-managed Postgres instance on the same hardware as the API as specified by the provided Docker compose file meets none of these requirements nor even global persistence.

### Load balancing

Intelligent load balancing is essential for ensuring that computing resources can be scaled to accomodate future changes to the volume of requests that must be handled. This can be managed by a reverse proxy like Nginx or by a cloud provider service.

### CI/CD

Continuous integration ensures that the product is robust in its behavior under future changes. Continuous delivery ensures that the product served to customers is fully up-to-date with latest development and releases. I am most well-versed in Github Actions as a CI/CD solution. Thorough unit and system testing of the application is a prerequisite of robust CI/CD solutions.

## Proposed deployment solutions

If tasked with deploying this API with the following constraints:

- as quickly as possible
- with concern for future scalability
- without concern for hosting/infrastructure costs

then I would propose that the Flask API be hosted by [Google App Engine](https://cloud.google.com/appengine) and backed by a [Google Cloud SQL](https://cloud.google.com/sql) Postgres instance.
