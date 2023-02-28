from click.testing import CliRunner
from main import main

def test_list1():
    runner = CliRunner()
    result = runner.invoke(main, input='test')
    assert result.exit_code == 0
    assert result.output == 'Hello Peter!\n'
