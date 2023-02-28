import logging
import sys

import click

from formats import FORMATS, JSONFormat
from guesses import (
    guess_if_data_is_quoted,
    guess_separator_unquoted,
    split_by_quote_char,
)

logging.root.setLevel(logging.INFO)


@click.command()
@click.argument("filename", default=sys.stdin, type=click.File(mode="r"))
@click.option(
    "--format",
    type=click.Choice(["JSON", "Python"], case_sensitive=False),
    default="JSON",
)
@click.option("--skip-empty-lines/--keep-empty-lines", default=True)
@click.option("--comment-string", default="#")
def main(filename, format, skip_empty_lines, comment_string):
    # Load the class corresponding to the chosin output format
    # TODO: use a dict (but who cares?)
    output_format = None
    for possible_format in FORMATS:
        if format == possible_format.name:
            output_format = possible_format
    if output_format is None:
        raise NotImplementedError(f"{format}: unrecognized output format")

    # Read the input data
    raw_data = filename.read()
    raw_data = "\n".join(
        [
            line
            for line in raw_data.split(sep="\n")
            if not line.startswith(comment_string)
        ]
    )

    if skip_empty_lines:
        raw_data = "\n".join([line for line in raw_data.split("\n") if line != ""])
    else:
        raise NotImplementedError  # TODO

    # Meaning that data is empty or a collection of empty lines
    # TODO: performance
    if not raw_data.split():
        logging.info("Data is empty or is a collection of empty lines")
        click.echo(output_format.to_string([]))
        sys.exit(0)

    # Check if data is in a know format
    valid_formats = [format for format in FORMATS if format.is_valid(raw_data)]
    for format in valid_formats:
        logging.info(f"{format.name} can decode the data")

    # That is the very easy case, where the data can be directly
    # decoded by one of the implemented formats
    if len(valid_formats) == 1:
        logging.info(f"{format.name} is the only valid format, will decode using it")
        click.echo(output_format.to_string(valid_formats[0].load(raw_data)))
        sys.exit(0)

    # Less easy case, where the data can be directly decoded by
    # several of the implemented formats. If it is valid JSON, it will
    # be decoded as JSON, otherwise will use the first format that
    # matches.
    elif len(valid_formats) > 1:
        logging.info(
            f"{len(valid_formats)} valid formats ({[f.name for f in valid_formats]}), will decode using JSON if it is in the list, or the first one in the list otherwise."
        )
        if any([f.name == "JSON" for f in valid_formats]):
            click.echo(JSONFormat.to_string(valid_formats[0].load(raw_data)))
            sys.exit(0)
        else:
            click.echo(valid_formats[0].to_string(valid_formats[0].load(raw_data)))
            sys.exit(0)
    else:
        logging.info("Data is not in a known format, will try to guess something…")

    quoted, quote_char = guess_if_data_is_quoted(raw_data)
    if quoted:
        print(split_by_quote_char(raw_data, quote_char))
    else:
        separator = guess_separator_unquoted(raw_data)
        click.echo(output_format.to_string([x.strip() for x in raw_data.split(sep=separator)]))
    # guess_types(data)


if __name__ == "__main__":
    main()
