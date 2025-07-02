# Portfolio Admin Back-end

That's a cool application result of my studies about FastAPI framework featuring:

- **FastAPI** with `fastapi[standard]` for blazing-fast APIs
- **SQLModel** for intuitive data modeling with SQLAlchemy & Pydantic
- **PostgreSQL** with `psycopg2-binary`
- **Alembic** for robust database migrations
- **JWT authentication** via `python-jose[cryptography]`
- **Secure password hashing** using `passlib[bcrypt]`
- **Multipart/form-data support** for file uploads
- **Environment variable management** with `python-dotenv`
- **Serverless-ready** with `mangum` for AWS Lambda deployments


## Requirements

- Python 3.9+
- PostgreSQL database


## Project Architecture
```bash
 [ Internet ]
      │
      ▼
+--------------------+
|   Route 53 (DNS)   |
+--------------------+
      │
      ▼
+----------------------+
|  CloudFront CDN      |
|  (HTTPS + Caching)   |
+----------------------+
      │
      ▼
+------------------------+
|  AWS Lambda (FastAPI)  |
|  Runtime: Python       |
|  Code: "mangun"        |
|  Trigger: API Gateway  |
+------------------------+
      │
      ▼
+-----------------------+
|  Amazon RDS (Postgres)|
|  VPC Subnet, SecGroup |
+-----------------------+

```


## Project structure
```bash
.
├── alembic/                 # Alembic migrations
├── src/
│   ├── config/              # Application configurators
│   ├── scripts/             # Scripts for automations and others
│   └── v1/                  # Api Modules
├── .env.local               # Environment variables template
├── .gitignore               # Gitignore config
├── .alembic.ini             # Alembic config
├── main.py                  # FastAPI entrypoint
├── README.md                # Cool README file
└── requirements.txt         # Application requirements
```

## Installing
Create a virtual env:

```bash
python -m venv .venv
```

Activate it:
```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```
or
```bash
make install
```

Run it:

```bash
fastapi dev main.py
```
or
```bash
make run-dev
```

## Deploying

Extract all the dependencies:
```bash
pip install -t lib -r requirements.txt
```

Bundle the requirements into a zip file:
```bash
(cd lib; zip ../aws-lambda-artifacts.zip -r .)
```

Add to the bundle all the app source:
```bash
zip -ru aws-lambda-artifacts.zip /src /alembic alembic.ini main.py
```

Deploy the aws-lambda-artifacts.zip into a aws lambda function using aws-cli or aws console
