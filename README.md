# http://django-ebola.herokuapp.com/

### Backup or load pg database

pg_dump dbname > outfile
ex) pg_dump ebola > 0825_night

psql ebola < 0825_night
