JSON:

JSON Type    | URL
------------ | -------------

daily | http://localhost:8089/location/national/?format=json
weekly | http://localhost:8089/location/national/?format=weekly_json

pg_dump dbname > outfile
ex) pg_dump ebola > 0825_night

psql ebola < 0825_night

qs to get all entries between these dates
http://api.crisis.net/item?text=ebola&after=2014-05-01&apikey=53f3b2c526102d463f4b14e1

then: can just get the new entries since yesterday by using 'after' and can double check that we don't already have them by using the provided id
