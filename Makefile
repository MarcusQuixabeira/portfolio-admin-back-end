install:
	pip install -r requirements.txt

run-dev:
	fastapi dev main.py

run-production:
	fastapi dev main.py

migrate:
	alembic upgrade head

create-admin-user:
	python -m scripts/create_user_admin