# OLX-clone-project

Това е моят Olx-clone project.Проектът реализира уебсайт чрез Flask ,SQLAlchemy and Jinja Templates.

## Инсталация

1. Създаване на виртуална среда:

    ```bash
    python -m venv .venv
    .venv/bin/activate
    ```

2. Инсталация на небходимите пакети:

    ```bash
    pip install -r requirements.txt
    ```

3. Инициализиране на базата:

    ```bash
    flask db init
    flask db migrate
    flask db upgrade
    ```

## Използване

```bash
Add-Content -Path ".env" -Value "SECRET_KEY='<yourSecretkey>'" 
# Заменете <yourSecretkey> с ключ по ваш избор
```

```bash
python -m flask --app app.py run
```
Последвайте * Running on {{http://XXX.X.X.X:XXXX}} 