
# skol - Some kind of list

`skol` is command-line tool that transform data into different types of lists (JSON list, Python list, Postgres array…). It will try very hard to guess where the data should be split and how to treat escaped characters.

# Example
`curl -s "https://api-adresse.data.gouv.fr/reverse/?lat=50.622772&lon=3.043936&limit=10" | jq '.features[].properties.id' | skoll --format=postgres`
