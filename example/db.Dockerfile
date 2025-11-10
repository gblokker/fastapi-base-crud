# Postgres Database Image for Testing with Alembic migrations
FROM postgres:16-alpine

# Install Python and pip for running Alembic
RUN apk add --no-cache python3 py3-pip

# Set environment variables for testing
ENV POSTGRES_DB=test_db
ENV POSTGRES_USER=test_user
ENV POSTGRES_PASSWORD=test_password

# Create directory for migrations
WORKDIR /migrations

# Copy alembic files and models
COPY alembic.ini .
COPY alembic ./alembic
COPY models.py .
COPY db.py .

# Install required Python packages
RUN pip3 install --no-cache-dir sqlalchemy alembic psycopg2-binary --break-system-packages

# Create entrypoint script that starts postgres and runs migrations
RUN echo '#!/bin/sh' > /docker-entrypoint-migrations.sh && \
    echo 'set -e' >> /docker-entrypoint-migrations.sh && \
    echo '' >> /docker-entrypoint-migrations.sh && \
    echo '# Start PostgreSQL in background' >> /docker-entrypoint-migrations.sh && \
    echo 'docker-entrypoint.sh postgres &' >> /docker-entrypoint-migrations.sh && \
    echo 'PG_PID=$!' >> /docker-entrypoint-migrations.sh && \
    echo '' >> /docker-entrypoint-migrations.sh && \
    echo '# Wait for PostgreSQL to be ready' >> /docker-entrypoint-migrations.sh && \
    echo 'echo "Waiting for PostgreSQL to start..."' >> /docker-entrypoint-migrations.sh && \
    echo 'until pg_isready -U $POSTGRES_USER -d $POSTGRES_DB; do' >> /docker-entrypoint-migrations.sh && \
    echo '  sleep 1' >> /docker-entrypoint-migrations.sh && \
    echo 'done' >> /docker-entrypoint-migrations.sh && \
    echo 'echo "PostgreSQL is ready!"' >> /docker-entrypoint-migrations.sh && \
    echo '' >> /docker-entrypoint-migrations.sh && \
    echo '# Run Alembic migrations' >> /docker-entrypoint-migrations.sh && \
    echo 'cd /migrations' >> /docker-entrypoint-migrations.sh && \
    echo 'echo "Running Alembic migrations..."' >> /docker-entrypoint-migrations.sh && \
    echo 'alembic upgrade head' >> /docker-entrypoint-migrations.sh && \
    echo 'echo "Migrations complete!"' >> /docker-entrypoint-migrations.sh && \
    echo '' >> /docker-entrypoint-migrations.sh && \
    echo '# Keep PostgreSQL running in foreground' >> /docker-entrypoint-migrations.sh && \
    echo 'wait $PG_PID' >> /docker-entrypoint-migrations.sh && \
    chmod +x /docker-entrypoint-migrations.sh

# Expose the default PostgreSQL port
EXPOSE 5432

# Add healthcheck
HEALTHCHECK --interval=10s --timeout=5s --retries=5 \
    CMD pg_isready -U test_user -d test_db

# Initialize with custom configuration optimized for testing
RUN echo "shared_buffers = 128MB" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "fsync = off" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "synchronous_commit = off" >> /usr/local/share/postgresql/postgresql.conf.sample && \
    echo "full_page_writes = off" >> /usr/local/share/postgresql/postgresql.conf.sample

# Use custom entrypoint that runs migrations
ENTRYPOINT ["/docker-entrypoint-migrations.sh"]
