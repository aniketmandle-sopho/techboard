## Procedure for Installation
Add proxy settings ( if any ) to the terminal by editing bashrc file

**Install Python and Nginx**
```
sudo apt-get update
sudo apt-get install python2.7 python-pip python-dev libpq-dev nginx
```
**Installation of MariaDB**

```
sudo apt-get install software-properties-common
sudo apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xF1656F24C74CD1D8
sudo add-apt-repository 'deb [arch=amd64,i386,ppc64el] http://nyc2.mirrors.digitalocean.com/mariadb/repo/10.2/ubuntu xenial main'
```
Replace the link in the last line with the link you get on the [Link](https://downloads.mariadb.org/mariadb/repositories/)  by  select the appropriate server and Ubuntu version. The shown example is for Ubuntu 16.04.

After this execute the following commands.

```
sudo apt update
sudo apt install mariadb-server libmariadbclient-dev
```

During installation it will ask you to set a username and password for accessing the database. Remeber it and Keep it secure. I would suggest making a random string will be better by the follwing command
```
openssl rand -base64 32
```

# Pending Below This
git clone https://github.com/aniketmandle-sopho/techboard.git

pip install --upgrade pip
pip install --user pipenv
pip install virtualenv

virtualenv techboard_env
source techboard_env/bin/activate
cd techboard
pip install -r requirements.txt

nano techboard/settings/base.py
	//Add the address where you want to host it in allowed hosts
	//configure database settings in it
	DATABASES = {
	    'default': {
	        'ENGINE': 'django.db.backends.mysql',
	        'NAME': 'Techboard',
	        'USER': 'root',
	        'PASSWORD': 'password',
	        'HOST': 'localhost',
	        'PORT': '',
	    }
	}
	//check once if static root and media root are set to these
	STATIC_ROOT = os.path.join(BASE_DIR, 'static')
	STATIC_URL = '/static/'

	MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
	MEDIA_URL = '/media/'

mysql -u root -p
	create database Techboard;

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
//firewall
sudo ufw allow 8000
python manage.py runserver 0.0.0.0:8000

gunicorn --bind 0.0.0.0:8000 techboard.wsgi

//check if server is working if yes proceed otherwise check gunicorn properly
//deact the virtualenv
deactivate

sudo nano /etc/systemd/system/gunicorn.service
 
	[Unit]
	Description=gunicorn daemon
	After=network.target

	[Service]
	User=ubuntu
	Group=www-data
	WorkingDirectory=/home/ubuntu/techboard
	ExecStart=/home/ubuntu/techboard_env/bin/gunicorn --access-logfile - --workers 1 --bind unix:/home/ubuntu/techboard/techboard.sock techboard.wsgi:application

	[Install]
	WantedBy=multi-user.target

sudo systemctl start gunicorn
sudo systemctl enable gunicorn
//check the status for working
sudo systemctl status gunicorn

//list files in the project folder
ls ~/techboard
//make sure it has techboard.sock file

//to see gunicorns log file
sudo journalctl -u gunicorn

//if you make changes to gunicorn.service file
sudo systemctl daemon-reload
sudo systemctl restart gunicorn


//NGINX
sudo nano /etc/nginx/sites-available/techboard
	server {
	    listen 80;
	    server_name 172.16.101.170;

	    location = /favicon.ico { access_log off; log_not_found off; }

	    location = /media/ {
	    	root /home/ubuntu/techboard;
	    }
	    location /static/ {
	        root /home/ubuntu/techboard;
	    }

	    location / {
	        include proxy_params;
	        proxy_pass http://unix:/home/ubuntu/techboard/techboard.sock;
	    }


	}

sudo ln -s /etc/nginx/sites-available/techboard /etc/nginx/sites-enabled/

//test nginx for syntx error using 
sudo nginx -t

sudo systemctl restart nginx

sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'

//You are all set( remember to set debug=False in dev.py and change the secret key)

// if anytime you make changes in django files make sure to restart the gunicorn service

sudo systemctl restart gunicorn

exit