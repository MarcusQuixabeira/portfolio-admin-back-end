install:
	pip install -r requirements.txt

run-dev:
	fastapi dev main.py

run-production:
	fastapi main.py

migrate:
	alembic upgrade head

create-admin-user:
	python scripts/create_user_admin.py