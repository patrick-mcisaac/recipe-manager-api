rm ./db.sqlite3
rm -rf ./recipe/migrations
python3 manage.py migrate
python3 manage.py makemigrations recipe
python3 manage.py migrate recipe
python3 manage.py loaddata users
python3 manage.py loaddata tokens
python3 manage.py loaddata ingredients
python3 manage.py loaddata recipe