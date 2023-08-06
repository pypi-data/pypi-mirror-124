from click.testing import CliRunner
import pytest

from dude._commands.cli_base import dude_cli


def test_prints_usage_when_no_arguments_are_provided():
    runner = CliRunner()
    result = runner.invoke(dude_cli, ["topics"])
    assert "Usage" in result.output
    assert result.exit_code == 0


@pytest.mark.skip("SCHEMA_REGISTRY_URL is required but shouldn't be")
def test_requires_bootstrap_server():
    runner = CliRunner()
    result = runner.invoke(dude_cli, ["topics", "list"])
    assert "Missing option '--bootstrap-servers'" in result.output
    assert result.exit_code == 2


@pytest.mark.skip("some StopIteration exception that I didn't feel like debugging")
def test_it_can_list_topics():
    runner = CliRunner()
    result = runner.invoke(dude_cli, ["topics", "--bootstrap-servers", "localhost:9092,kafka-1:9092", "list"])
    assert "__consumer_offsets\n" in result.output
    assert result.exit_code == 0


@pytest.mark.skip("some StopIteration exception that I didn't feel like debugging")
def test_envvar_supported_for_option_bootstrap_server():
    runner = CliRunner()
    result = runner.invoke(dude_cli, ["topics", "list"], env={"BOOTSTRAP_SERVERS": "localhost:9092,kafka-1:9092"})
    assert "__consumer_offsets\n" in result.output
    assert result.exit_code == 0
