# Tester for 3 points requirements

import handler
import pytest
import pexpect


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


def test_command_execution(program):
    commands = [
        "ls -la --color=never",
        'echo "Hello from my Shell"',
        'echo "This Is a very Long String' + "A" * 1000 + '"',
        'echo "This string contains chars and other things .912345&*<>again()?/_-+     ~#@%"',
    ]
    bash = handler.ShellHandler("bash")
    hand = handler.ShellHandler(program)

    run_commands(bash, hand, commands)


def test_command_redirection_simple_pipe(program):
    commands = [
        "ls -la --color=never | wc",
        "ls -la --color=never | wc > a.txt",
        "cat a.txt",
        'echo "Hello Im Writing to the end of a file" >> a.txt',
        "cat a.txt",
        "wc < a.txt",
        'echo "." > a.txt',
        "ls --color=never < a.txt | wc > b.txt",
        "ls --color=never > a.txt | wc",
    ]
    bash = handler.ShellHandler("bash")
    hand = handler.ShellHandler(program)

    run_commands(bash, hand, commands)


def test_cd_command(program):
    hand = pexpect.spawn(program, encoding="utf-8")
    hand.expect(".*")
    prompt = hand.after
    hand.sendline("mkdir testdir")
    hand.expect_exact(prompt)
    hand.sendline("cd testdir")
    hand.expect(".+")
    prompt2 = hand.after
    assert prompt != prompt2, "Bad implementation of cd"
    hand.sendline("cd ..")
    hand.expect_exact(prompt)
    hand.sendline("cd ~")
    hand.expect(".+")
    home = hand.after
    assert prompt != home, "Bad implementation of cd"
    hand.terminate(force=True)


def test_comments(program):
    commands = [
        "#This line should get ignored",
        "# This line should also get ignored",
        "### This is ignored too",
    ]
    bash = handler.ShellHandler("bash")
    hand = handler.ShellHandler(program)

    run_commands(bash, hand, commands)


def test_garbage_command(program):
    hand = handler.ShellHandler(program)
    bash = handler.ShellHandler("bash")

    cmds = [
        '"ls --color=never"',  # this is a valid command
        '"echo" "ThisShouldWorkToo"'
    ]
    run_commands(bash, hand, cmds)
    hand = handler.ShellHandler(program)
    # this has to fail
    out = hand.do_input("garbage command ls -la --color=never -print | grep | tail")
    assert "not found" in out, "Garbage is not a valid command"
    hand.do_end()


def test_redirectors_with_no_first_argument(program):
    handl = pexpect.spawn(program, encoding="utf-8")
    handl.expect(".+")
    prompt = handl.after
    handl.sendline("> new.txt")
    handl.expect_exact(prompt)
    handl.sendline("ls -la")
    handl.expect_exact(prompt)
    assert "new.txt" in handl.before, "This has to work: > a.txt"
    handl.sendline("rm new.txt")
    handl.expect_exact(prompt)
    handl.sendline(">> new.txt")
    handl.expect_exact(prompt)
    handl.sendline("ls -la")
    handl.expect_exact(prompt)
    assert "new.txt" in handl.before, "This has to work: >> a.txt"
    handl.sendline("rm new.txt")
    handl.expect_exact(prompt)
    handl.terminate(force=True)
