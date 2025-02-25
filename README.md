# OLX-clone-project

This is my OLX clone project. It uses Flask, SQLAlchemy, and Jinja Templates to build a dynamic website.

## Install

1. Create a virtual environment:

    ```bash
    python -m venv .venv
    .venv/bin/activate
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Initialize the database:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Usage

```bash
Add-Content -Path ".env" -Value "SECRET_KEY='<yourSecretkey>'" 
# Заменете <yourSecretkey> с ключ по ваш избор
```

```bash
python -m flask --app app.py run
```
Click on * Running on {{http://XXX.X.X.X:XXXX}} 
