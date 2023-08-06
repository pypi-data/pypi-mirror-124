from click.testing import CliRunner

from dude._commands.cli_base import dude_cli
from .utils import IsolatedFixtureFolder


class TestVirtualEnvironmentManager:
    def setup_method(self):
        self.runner = CliRunner()

    def test_creation_of_virtual_environment(self):
        with IsolatedFixtureFolder(self.runner, "requirements-only"):
            result = self.runner.invoke(dude_cli, ["app", "unit_test"])
            assert "no tests ran" in result.output

            # Running it again in an already synced environment
            result = self.runner.invoke(dude_cli, ["app", "unit_test"])
            assert "Everything up-to-date" in result.output
            assert "no tests ran" in result.output
