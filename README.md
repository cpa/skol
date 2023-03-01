
# skol - Some kind of list
`skol` is a command-line tool that transform data into different types of lists (currently: JSON list, Python list, Postgres array). It will try very hard to guess where the data should be split and how to treat escaped characters.

# Example
Check `examples.txt` for a sample of the kind of transformation that `skol` can do.
`curl -s "https://api-adresse.data.gouv.fr/reverse/?lat=50.622772&lon=3.043936&limit=10" | jq '.features[].properties.id' | skol --format=postgres`
`curl -s "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?format=JSON&lang=EN&time=2019" | jq '.dimension.geo.category.index' | jq keys | skol --format=postgres`

# Build
Run `python -m build` in virtualenv

# Install
Download a wheel release and `pip install skol-use-the-correct-filename.whl` it in your virtualenv of choice.
