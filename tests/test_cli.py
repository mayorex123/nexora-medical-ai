from typer.testing import CliRunner
from nexora.__main__ import app

runner = CliRunner()

def test_version():
    r = runner.invoke(app, ["version"])
    assert r.exit_code == 0 and "NEXORA" in r.stdout

def test_status():
    r = runner.invoke(app, ["status"])
    assert r.exit_code == 0 and "Python" in r.stdout
