import logging
from collections import Counter

QUOTE_CHARS = "'\""


def split_by_quote_char(data, quote_char):
    # Note that this trick can return a char that is larger than the
    # larger unicode char (but "in real life" that does not happen)
    replacer = chr(ord(max(data + quote_char)) + 1)

    data = data.replace("\\" + quote_char, replacer)

    result = []
    accumulator = []
    inside_quote = False
    for c in data:
        if c == quote_char:
            if inside_quote:
                result.append(("".join(accumulator), "INSIDE"))
            else:
                result.append(("".join(accumulator), "OUTSIDE"))
            accumulator = []
            inside_quote = not inside_quote
        else:
            accumulator.append(c)
    if inside_quote:
        result.append(("".join(accumulator), "INSIDE"))
    else:
        result.append(("".join(accumulator), "OUTSIDE"))

    result = [
        (fragment.replace(replacer, "\\" + quote_char), status)
        for fragment, status in result
    ]

    return result


def guess_if_data_is_quoted(data):
    candidates = []
    for quote_char in QUOTE_CHARS:
        quote_char_count = data.count(quote_char)
        escaped_quote_char_count = data.count("\\" + quote_char)

        if quote_char_count == 0:
            logging.debug(f"Quote char {quote_char} not found in data")
            continue

        logging.debug(
            f"Quote char {quote_char} found {quote_char_count} times{', of which ' + str(escaped_quote_char_count) + ' are escaped' if escaped_quote_char_count > 0 else ''}."
        )

        candidates.append(
            (quote_char, quote_char_count - escaped_quote_char_count, quote_char_count)
        )

    if not candidates or all([c == 0 for (_, c, _) in candidates]):
        logging.debug(f"No quote character found in input data")
        return False, None
    else:
        candidates.sort(key=lambda d: -d[1])  # Sort on counts
        logging.debug(f"Using {candidates[0][0]} as quote character")
        # split_data = split_by_quote_char(data, quote_char=candidates[0][0])
        return True, candidates[0][0]


def guess_separator_unquoted(data):
    # We try to split on newlines and check if non-empty lines often
    # ends with a specific non-alphanumeric substring. If we can't
    # find a suitable separator this way, we check if the non-empty
    # lines often starts with a specific non-alphanumeric
    # substring. If it still fails, we try to use \n a the separator.

    split_data = data.split(sep="\n")

    tmp_suffix = []
    for line in split_data:
        non_alnum_suffix = []
        for c in line[::-1]:
            if c.isalnum():
                if non_alnum_suffix != []:
                    tmp_suffix.append("".join(non_alnum_suffix))
                    non_alnum_suffix = []
                break
            else:
                non_alnum_suffix.append(c)
    non_alnum_suffix_counter = Counter(tmp_suffix)

    if non_alnum_suffix_counter:  # Meaning the counter is not empty
        (
            possible_separator,
            possible_separator_count,
        ) = non_alnum_suffix_counter.most_common(1)[0]
        logging.debug(
            f"Most common non-alnum prefix is {possible_separator} ({possible_separator_count} occurence(s), {int(float(possible_separator_count) / len(split_data) * 100)}% of lines)."
        )
        if float(possible_separator_count) / len(split_data) > 0.8:
            logging.debug(
                f"{possible_separator} is a suffix of more than 80% of all lines, will use as separator"
            )
            return possible_separator
        else:
            logging.debug(
                f"{possible_separator} is a suffix of less than 80% of all lines, will not use as separator. Trying prefixes."
            )

    tmp_prefix = []
    for line in split_data:
        non_alnum_prefix = []
        for c in line:
            if c.isalnum():
                if non_alnum_prefix != []:
                    tmp_prefix.append("".join(non_alnum_prefix))
                    non_alnum_prefix = []
                break
            else:
                non_alnum_prefix.append(c)
    non_alnum_prefix_counter = Counter(tmp_prefix)

    if non_alnum_prefix_counter:  # Meaning the counter is not empty
        (
            possible_separator,
            possible_separator_count,
        ) = non_alnum_prefix_counter.most_common(1)[0]
        logging.debug(
            f"Most common non-alnum prefix is {possible_separator} ({possible_separator_count} occurence(s), {int(float(possible_separator_count) / len(split_data) * 100)}% of lines)."
        )
        if float(possible_separator_count) / len(split_data) > 0.8:
            logging.debug(
                f"{possible_separator} is a suffix of more than 80% of all lines, will use as separator"
            )
            return possible_separator
        else:
            logging.debug(
                f"{possible_separator} is a suffix of less than 80% of all lines, will not use as separator. Trying \\n."
            )

    logging.debug(
        "Could not find a common suffix or prefix appearing on most lines, defaulting to \\n"
    )
    return "\n"

    # split_data = data.split()  # TODO: splits on any whitespace character
    # # print(data, split_data)

    # if len(split_data) == 1:
    #     logging.debug("Data is one line long")
    #     data = split_data[0]
    #     non_alnum = [c for c in data if not c.isalnum()]
    #     print(non_alnum)

    # else:
    #     # In this case len > 1 because the case where len == 0 has
    #     # been caught before in the code. Right?
    #     logging.debug("Data is more than one line long")

    #     possible_separators = []
    #     for line in split_data:
    #         break
