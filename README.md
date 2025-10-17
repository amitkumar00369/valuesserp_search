A small Django app that accepts multiple search queries, queries ValueSERP API,
displays results in a table, and exports results as CSV. Uses Bootstrap for UI.

1. Clone the repository.
2. Create and activate a virtual environment:

## py -m venv valueserpenv

activate this environment
.\valueserpenv\Scripts\activate

## Requirements

- Python 3.11+ recommended
- install dependicies
  pip install -r requirements.txt

## Setup .env

VALUESSERP_API_KEY="EBC00868501542BC8EF2910564D26EAF"
base_url = "https://api.valueserp.com/search"

## Start Server

python manage.py runserver
