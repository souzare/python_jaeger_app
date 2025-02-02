# My Python Jaeger App

This project is a Flask application that integrates with Jaeger for distributed tracing and Prometheus for monitoring. It uses a SQLite database to store posts and provides metrics for monitoring application performance.

## Project Structure

```
my-python-jaeger-app
├── app
│   ├── app.py               # Main Flask application code
│   ├── requirements.txt      # Python dependencies
│   └── Dockerfile            # Dockerfile for building the application image
├── docker-compose.yml        # Docker Compose configuration for the application and Jaeger
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd my-python-jaeger-app
   ```

2. **Build and run the application with Docker Compose:**
   ```
   docker-compose up --build
   ```

3. **Access the application:**
   Open your web browser and navigate to `http://localhost:5000`.

4. **Access Jaeger UI:**
   Open your web browser and navigate to `http://localhost:16686` to view the Jaeger UI.

## Usage

- The application provides a simple interface to create and view posts.
- Jaeger will automatically collect traces from the application, which can be viewed in the Jaeger UI.

## Dependencies

The application requires the following Python packages, which are listed in `app/requirements.txt`:

- Flask
- Prometheus client libraries
- Jaeger client libraries

## License

This project is licensed under the MIT License.