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

exec "$@"