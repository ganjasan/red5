#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

	until PGPASSWORD=$SQL_PASSWORD psql -h $SQL_HOST -p $SQL_PORT -d  $SQL_DATABASE -U $SQL_USER -c '\q'; do
	  echo "Postgres is unavailable - sleeping"
	  sleep 30
	done

    echo "PostgreSQL started"
fi

#python manage.py flush --no-input
python manage.py makemigrations
python manage.py migrate
python manage.py loaddata currency.json country.json city.json unit.json

#python manage.py createsuperuser 
#echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('admin', 'admin@myproject.com', 'adminadmin')" | python manage.py shell

exec "$@"