install:
	pip install -r requirements.txt

run-dev:
	fastapi dev main.py

run-production:
	fastapi main.py

migrate:
	alembic upgrade head