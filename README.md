## Запуск в Docker
```
sudo docker run -p 5000:5000 -it --name Ubuntu1804 ubuntu:18.04 /bin/bash
```

```
apt update &&
apt install -y git && 
git clone https://github.com/Kira5005-code/Zoom-Youtube-Publisher.git
cd Zoom-Youtube-Publisher &&
apt-get install -y --no-install-recommends python3.5 python3-pip && rm -rf /var/lib/apt/lists/* &&
pip3 install virtualenv &&
virtualenv -p python3 env &&
source env/bin/activate &&
pip3 install -U pip setuptools &&
pip3 install -r requipments/development.txt &&
pip3 install flask_script &&
export APP_SETTINGS="config.DevelopmentConfig" &&
export DATABASE_URL='sqlite:///app.db' &&
python3 manage.py db init &&
python3 manage.py db migrate &&
python3 manage.py db upgrade &&
python3 manage.py runserver --host 0.0.0.0
```
