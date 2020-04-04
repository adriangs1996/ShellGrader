import handler
import pytest


def run_commands(bash, hand, commands):
    for cmd in commands:
        bash_out = bash.do_input(cmd)
        sh_out = hand.do_input(cmd)
        assert bash_out == sh_out, "Command execution failed, expected %s and got %s" % (
            bash_out, sh_out)
    bash.do_end()
    hand.do_end()


@pytest.fixture()
def program(pytestconfig):
    return pytestconfig.getoption("program")


def test_history(program):
    handl = handler.ShellHandler(program)

    # Run 10 commands to fill the history
    cmds = [
        "ls -la --color=never", "echo HelloWorld",
        'find ~/ -type f -print | grep --color=never "Permission Denied" > out.txt',
        "rm out.txt", "echo againHello", "ps aux", "ls -la --color=never | wc",
        "echo HelloAgain", "ls -la | cat"
    ]

    for cmd in cmds:
        handl.do_input(cmd)

    history = handl.do_input("history")
    assert "[10]: history" in history, "'history' command must be part of the history"
    cmd_result = handl.do_input("again 2")
    assert cmd_result == "HelloWorld", "Bad again implementation"
    cmd_result = handl.do_input("again 5 | sort > again.txt")
    out = handl.do_input("ps aux | sort")
    out2 = handl.do_input("cat again.txt")
    assert out == out2
    handl.do_input("rm again.txt")
    cmd_result = handl.do_input("echo 'again 3 This must print'")
    assert cmd_result == "again 3 This must print", "Quotes must escape again command"
    handl.do_end()
