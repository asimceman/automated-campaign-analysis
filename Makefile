# Show this help prompt.
help:
	@ echo 'Helpers for development inside automated-analysis service'

start:
	docker compose up -d --build backend db
	docker compose exec backend poetry run alembic upgrade head
	docker compose exec backend poetry run python app/data/seed.py
	cd frontend && npm install && npm run dev

stop:
	docker compose down