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

Clone the follwing repo or download it
```
git clone https://github.com/aniketmandle-sopho/techboard.git
```
Now we will install virtualenv and make one so that the python libraries we are using don't clash with other libraries. Also we will install all the requirements.
``` 
pip install --upgrade pip
pip install --user pipenv
pip install virtualenv
virtualenv techboard_env
source techboard_env/bin/activate
cd techboard
pip install -r requirements.txt
```
After this 50% of your job is done now things that are left is configuring your server. First we will edit settings.by

```
nano techboard/settings.py

//Add these lines at appropriate locations

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'Techboard',
        'USER': 'username_of_database',
        'PASSWORD': 'password_of_database',
        'HOST': 'localhost',
        'PORT': '',
    }
}

//check once if allowed_hosts, static root and media root are set to these
ALLOWED_HOSTS = ['URL_where_you_want_to_host']

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

```
Now we will make a database named Techboard
```
mysql -u username_of_database -p
create database Techboard;
```
Now as we have Setup the databse and configured django we can do a trial run on the server. First of all we will makemigrations and migrate(This will create and modify existing tables in the database.). Then we will createsuperuser to access the adminpanel. Again now set admin panel's password securely and I would suggest to keep it again a random string.
``` 
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```
Set up firewall for port 8000 as we are test run our server on that port. Run the server and link it with gunicorn
```
sudo ufw allow 8000
python manage.py runserver 0.0.0.0:8000
gunicorn --bind 0.0.0.0:8000 techboard.wsgi
```

Check if server is working properly, if yes proceed further otherwise check gunicorn again. After this deactivate the virtualenv
```
deactivate
```
Now we want that gunicron should be running all time so we will make a system service.
Working Directory 
```
sudo nano /etc/systemd/system/gunicorn.service
//Add these in the file
[Unit]
Description=gunicorn daemon
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/techboard
ExecStart=/home/ubuntu/techboard_env/bin/gunicorn --access-logfile - --workers 1 --bind unix:/home/ubuntu/techboard/techboard.sock techboard.wsgi:application -e http_proxy=http://name:pass@address -e https_proxy=https://name:pass@address

[Install]
WantedBy=multi-user.target
```
So now we have successfully made the service file telling system what to do, now we will activate the service. Enable the service and check status whether gunicorn is working ot not

```
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
sudo systemctl status gunicorn
```
If gunicorn status is shoing error make sure that there is techboard.sock file in project folder. If you want to see log file of gunicorn, use this command.
```
sudo journalctl -u gunicorn
```

Whenever you make changes to gunicorn.service file or python files make sure to reload the server by these commands
```
sudo systemctl daemon-reload
sudo systemctl restart gunicorn
```
So now as we are all set with gunicorn now we will have to configure NGINX, this will handle all the requests and pass it to our server
```
sudo nano /etc/nginx/sites-available/techboard
//Add these lines
server {
    listen 80;
    server_name server_address;

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
```
```
sudo nano /etc/nginx/nginx.conf
//Add the follwing line in http section to increase the default upload size
http{
    ...
    ...
   	client_max_body_size 20M;
   	...
   	}
```
Make a link to sites enabled in NGINX using this command and we will enable firewall for NGINX and check for syntax error's in NGINX file using -t flag.
```
sudo ln -s /etc/nginx/sites-available/techboard /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
sudo ufw delete allow 8000
sudo ufw allow 'Nginx Full'
```
Now we are ready to deploy just make sure you edit settings.py and set debug=False.

Now to access wagtail-admin goto server_address/admin and for django-admin goto server-address/django-admin.

If you find any issue feel free to contact us.