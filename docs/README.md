# How to setup this backend (on Linux)

##0. Clone this repo and cd into it.

##1. At first install postgresql. For Arch that would be:
`yay -Sy postgresql`

for Ubuntu maybe try this:  
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```
but idk which version that would install. For newest Postgres 12 i found a [tutorial](https://itsfoss.com/install-postgresql-ubuntu/).

##2. Create database
```sudo -u postgres psql -f docs/database-setup.sql```

##3. Install dependencies
```sudo pip3 install -r requirements.txt```

##4. Perform migrations
```
python manage.py makemigrations
python manage.py migrate
```

##5. Load fixture with default groups and user accounts
```
python manage.py loaddata docs/default_users.json
```

Default accounts are:  
admin:admin  
student:Y7J.M34Ms9mVW.-  

##6. Run the server
`python manage.py runserver`

# How-to FAQ
1. Create superuser  
`python manage.py createsuperuser`

2. Create normal user  
go to http://localhost:8000/admin/ and add user using form. Don't forget to add group permissions.
