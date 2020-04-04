import handler
import pytest


def run_commands(bash, hand, commands):
    for cmd in commands:
        print(cmd)
        bash_out = bash.do_input(cmd)
        sh_out = hand.do_input(cmd)
        assert bash_out == sh_out, "Command execution failed, expected %s and got %s" % (
            bash_out, sh_out)
    bash.do_end()
    hand.do_end()


@pytest.fixture()
def program(pytestconfig):
    return pytestconfig.getoption("program")


def test_multiple_pipes(program):
    commands = [
        "ls -la --color=never | sort | uniq | wc", "echo H" + "i" * 8000 + " | wc" * 200,
        'echo "." > a1.txt', "ls -la --color=never < a.txt | sort | uniq | grep a >> a1.txt",
    ]

    bash = handler.ShellHandler("bash")
    hand = handler.ShellHandler(program)

    run_commands(bash, hand, commands)
