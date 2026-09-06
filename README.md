# Run

```bash

# 1) run postgres 

# 2) create database
PGPASSWORD=postgres psql -h localhost -p 5432 -U postgres -f ./resources/init_db.sql

# 3) run app
uv run --env-file .env --module uvicorn src.market.web:app
```