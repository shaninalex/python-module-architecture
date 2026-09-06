PROJECT_ROOT := $(shell pwd)
MIGRATE_BIN ?= migrate
DB_URL ?= postgresql://buyshoes_user:buyshoes_password@localhost:5432/buyshoes?sslmode=disable


migrate_create:
	@test -n "$(NAME)" || (echo "Usage: make migrate_create NAME=<name>"; exit 1)
	$(MIGRATE_BIN) create \
		-ext sql \
		-dir $(PROJECT_ROOT)/resources/migrations \
		-format "20060102150405" \
		"$(NAME)"

migrate_up:
	$(MIGRATE_BIN) \
		-path $(PROJECT_ROOT)/resources/migrations \
		-database "$(DB_URL)" \
		-verbose up

seed:
	uv run --package seeder python -m seeder \
		--config $(PROJECT_ROOT)/database/seeder/config.yaml \
		start

seed_fixtures:
	uv run --package seeder python $(PROJECT_ROOT)/database/seeder/resources/gen_products.py
