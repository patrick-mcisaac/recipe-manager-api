rm ./db.sqlite3
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata users
python3 manage.py loaddata ingredients
python3 manage.py loaddata recipe