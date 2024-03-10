from sentinel.commands.common import get_command, get_commands_from_module


def test_get_commands_from_module():
    commands = get_commands_from_module("sentinel.commands")
    assert list(commands.keys()) == [
        "abi_signature",
        "fetch",
        "launch",
    ], "Incorrect list of sentinel commands"


def test_get_command():
    assert get_command([]) == "", "Incorrect command for empty argument list"
    assert (
        get_command(["sentinel", "launch", "--profile", "test.yaml"]) == "launch"
    ), "Incorrect launch command detected"
    assert (
        get_command(["--profile", "test.yaml"]) == "test.yaml"
    ), "Wrong command detected for incorrect command arguments"
