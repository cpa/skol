from tempfile import NamedTemporaryFile

import pytest
from click.testing import CliRunner

from src.main import main

with open("examples.txt", "r") as fd:
    tmp = fd.read().split("---")
    tmp = [fragment.splitlines() for fragment in tmp]
    # tmp = [[subfragment.strip() for subfragment in fragment if not subfragment.strip().startswith("#")] for fragment in tmp]

    test_data = []
    cur_input = []
    cur_output = []
    part = "header"

    for fragment_tmp in tmp:
        for line in fragment_tmp:
            if line == "Input:":
                part = "input_body"
                continue
            if line == "Output:":
                part = "output_body"
                continue
            if part == "input_body":
                cur_input.append(line)
            if part == "output_body":
                cur_output.append(line)
        test_data.append(("\n".join([f for f in cur_input]), [f for f in cur_output if f != ""][0]))
        cur_input = []
        cur_output = []
        part = "header"


@pytest.mark.parametrize("test_input,expected", test_data)
def test_out_format_json_no_ai(test_input, expected):
    with NamedTemporaryFile("w+") as fd:
        fd.write(test_input)
        fd.flush()
        runner = CliRunner()
        result = runner.invoke(main, [fd.name, "--format=json"])
        assert not result.exception
        assert result.stdout.strip() == expected


# Commenting out this test as it's slow and costly
# @pytest.mark.parametrize("test_input,expected", test_data)
# def test_out_format_json_with_ai(test_input, expected):
#     with NamedTemporaryFile("w+") as fd:
#         fd.write(test_input)
#         fd.flush()
#         runner = CliRunner()
#         result = runner.invoke(main, [fd.name, "--format=json", "--ai"])
#         assert not result.exception
#         assert result.stdout.strip() == expected
