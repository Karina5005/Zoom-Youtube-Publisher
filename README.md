## Setup

```
virtualenv -p python3 env
source env/bin/activate
pip3 install -r requipments/development.txt
export APP_SETTINGS="config.DevelopmentConfig"
export DATABASE_URL='sqlite:///app.db'
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
python manage.py runserver
```
