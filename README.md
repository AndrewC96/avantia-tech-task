# avantia-tech-task
Submission for Avantia tech task - Andrew Cottis

# Nobel Prize Search Application

A Flask-based web application that allows users to search through Nobel Prize laureates using fuzzy search capabilities.

## Prerequisites

- Docker
- Docker Compose

## Setup Instructions

1. Clone the repository:

2. Create a `.env` file in the root directory with the following content:

bash
MONGO_ROOT_USER=admin
MONGO_ROOT_PASSWORD=your_root_password
MONGO_USER=nobel_user
MONGO_PASSWORD=your_password


3. Build and start the containers:

docker-compose up --build