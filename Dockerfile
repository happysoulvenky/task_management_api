FROM python:3.13-slim


WORKDIR /app


RUN  apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt .
# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


EXPOSE 5000

CMD ["python", "run.py"]




























# ---- Base Stage ----
# Use a slim Python image for a smaller footprint


# Set environment variables to prevent writing .pyc files and to run in unbuffered mode
# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# # ---- Builder Stage ----
# # This stage installs the dependencies
# 

# WORKDIR /app

# # Install build dependencies if any (e.g., for packages that compile from source)
# # RUN apt-get update && apt-get install -y --no-install-recommends gcc

# # Install python dependencies into a wheelhouse

# RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# # ---- Final Stage ----
# # This is the final image that will be run
# FROM base as final

# WORKDIR /app

# # Copy installed dependencies from the builder stage
# COPY --from=builder /app/wheels /wheels
# RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*

# # Copy the project source code
# COPY . .

# # Expose the port your application runs on
# EXPOSE 8000

# # Command to run the app.
# # You MUST update this command to start your application.
# # For a Gunicorn/Django app, it might look like this:
# # CMD ["gunicorn", "--bind", "0.0.0.0:8000", "task_management_api.wsgi:application"]
# CMD ["echo", "Please specify the command to run your application in the Dockerfile"]