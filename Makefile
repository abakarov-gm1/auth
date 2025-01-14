up:
	docker compose up -d

down:
	docker compose down

migrate:
	docker compose down
	docker compose run --rm fast-api alembic upgrade head
	docker compose up -d

