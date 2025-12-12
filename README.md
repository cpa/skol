
# skol - Some kind of list
`skol` is a command-line tool that transform data into different types of lists (currently: JSON list, Python list, Postgres array). It will try very hard to guess where the data should be split and how to treat escaped characters.

# Example
Check `examples.txt` for a sample of the kind of transformation that `skol` can do.
`curl -s "https://ec.europa.eu/eurostat/api/dissemination/statistics/1.0/data/nama_10_gdp?format=JSON&lang=EN&time=2019" | jq '.dimension.geo.category.index' | jq keys | skol --format=postgres`
`curl -s "https://api-adresse.data.gouv.fr/reverse/?lat=50.622772&lon=3.043936&limit=10" | jq '.features[].properties.id' | skol --format=postgres` (compare the output with `--ai` enabled)

# Build and install
Use the `uv` CLI for packaging and build tasks. Install `uv>=0.4` (see https://docs.astral.sh/uv/) and run `uv build`.

You can then install the generated wheel with:
```bash
uv tool install dist/skol-*-py3-none-any.whl
```

Alternatively, you can install directly from the source directory:
```bash
uv tool install .
```

Or for development installs:
```bash
uv pip install -e .
```

Once installed, you can run the CLI without activating a virtual environment:
```bash
uvx skol --help
```
