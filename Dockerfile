# Stage: frontend dependencies and builds
FROM node:22-alpine AS frontend-deps
WORKDIR /app

COPY package*.json ./
RUN npm install --include=dev

COPY tailwind.config.ts ./tailwind.config.ts
COPY static_src ./static_src

FROM frontend-deps AS frontend-build
RUN npm run build

FROM frontend-deps AS frontend-dev
CMD ["npm", "run", "dev"]

# Stage: python base env
FROM python:3.12-slim AS python-base

ARG APP_USER=app
ARG APP_GROUP=app
ARG APP_UID=1000
ARG APP_GID=1000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    APP_USER=${APP_USER} \
    APP_GROUP=${APP_GROUP} \
    APP_UID=${APP_UID} \
    APP_GID=${APP_GID}

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential bash gosu libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd --gid ${APP_GID} ${APP_GROUP} \
    && useradd --uid ${APP_UID} --gid ${APP_GID} --create-home --home-dir /home/${APP_USER} --shell /bin/bash ${APP_USER}

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Install entrypoint and ensure permissions
RUN install -m 0755 entrypoint.sh /usr/local/bin/entrypoint.sh

# Bring in the prebuilt Tailwind assets
COPY --from=frontend-build /app/static ./static

FROM python-base AS python-collectstatic
RUN python manage.py collectstatic --noinput

FROM python-collectstatic AS python-runtime
EXPOSE 8000

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
