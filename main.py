import logging
import sys

import click

from formats import FORMATS, JSONFormat
from guesses import (
    guess_if_data_is_quoted,
    guess_separator_unquoted,
    split_by_quote_char,
)

logging.root.setLevel(logging.DEBUG)


@click.command()
@click.argument("filename", default=sys.stdin, type=click.File(mode="r"))
@click.option(
    "--format",
    type=click.Choice(["JSON", "Python"], case_sensitive=False),
    default="JSON",
)
@click.option("--skip-empty-lines/--keep-empty-lines", default=True)
@click.option("--comment-string", default="#")
@click.option("--sep", "separator", type=click.STRING, default=None)
def main(filename, format, skip_empty_lines, comment_string, separator):
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
        logging.debug("Data is empty or is a collection of empty lines")
        click.echo(output_format.to_string([]))
        sys.exit(0)

    # Check if we already have a separator
    if separator is not None:
        logging.debug(f"Using provided separator {separator}")
        click.echo(JSONFormat.to_string(raw_data.split(sep=separator)))
        sys.exit(0)

    # Check if data is in a know format
    valid_formats = [format for format in FORMATS if format.is_valid(raw_data)]

    # That is the very easy case, where the data can be directly
    # decoded by one of the implemented formats
    if len(valid_formats) == 1:
        logging.debug(f"{valid_formats[0].name} is the only valid format, will decode using it")
        click.echo(output_format.to_string(valid_formats[0].load(raw_data)))
        sys.exit(0)

    # Less easy case, where the data can be directly decoded by
    # several of the implemented formats. If it is valid JSON, it will
    # be decoded as JSON, otherwise will use the first format that
    # matches.
    elif len(valid_formats) > 1:
        logging.debug(
            f"{len(valid_formats)} valid formats ({[f.name for f in valid_formats]}), will decode using JSON if it is in the list, or the first one in the list otherwise."
        )
        if any([f.name == "JSON" for f in valid_formats]):
            click.echo(JSONFormat.to_string(valid_formats[0].load(raw_data)))
            sys.exit(0)
        else:
            click.echo(valid_formats[0].to_string(valid_formats[0].load(raw_data)))
            sys.exit(0)
    else:
        logging.debug("Data is not in a known format, will try to guess something…")

    quoted, quote_char = guess_if_data_is_quoted(raw_data)
    if quoted:
        split_by_quote_char_data = split_by_quote_char(raw_data, quote_char)
        outside_fragments = ([fragment for fragment, status in split_by_quote_char_data if status == 'OUTSIDE'])
        inside_fragments = ([fragment for fragment, status in split_by_quote_char_data if status == 'INSIDE'])        
        if len(outside_fragments) == 0:
            raise ValueError("We cannot have an empty outside_fragments there")
        elif len(outside_fragments) == 1:
            logging.debug("TODO, what does this mean?")
        else:
            if all([not fragment.isalnum() for fragment in outside_fragments]):
                # Then we consider that the data "real data" is the
                # data inside quotes and that we can discard the
                # outside fragments
                click.echo(output_format.to_string([x.strip() for x in inside_fragments]))
        
    else:
        separator = guess_separator_unquoted(raw_data)
        click.echo(output_format.to_string([x.strip() for x in raw_data.split(sep=separator)]))
    # guess_types(data)


if __name__ == "__main__":
    main()
