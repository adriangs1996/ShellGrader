import handler
import pytest
import pexpect
import time


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


def test_nospaces_cmds(program):
    cmds = [
        "ls -la|wc", 'echo ".">a.txt', "ls<a.txt",
        "find ~/ -print -type f|grep share>>a.txt"
    ]

    hand = handler.ShellHandler(program)
    bash = handler.ShellHandler("sh")

    run_commands(bash, hand, cmds)


def test_multiple_spaces_cmds(program):
    cmds = [
        "ls         -la |    wc", "echo           Hello     >  a.txt",
        'echo    "."     > a.txt', "ls     < a.txt    | wc     >> a.txt"
    ]
    hand = handler.ShellHandler(program)
    bash = handler.ShellHandler("sh")

    run_commands(bash, hand, cmds)


def test_background(program):
    handl = pexpect.spawn(program, encoding="utf-8")
    handl.expect(".+")
    prompt = handl.after
    # Test if correctly sended to background
    handl.sendline("sleep 3 &")
    # inmediatly receive prompt
    handl.expect_exact(prompt, timeout=1)
    handl.sendline("ps aux | grep sleep | head -n 1")
    handl.expect_exact(prompt)
    assert "sleep 3" in handl.before, "Error, program sleep 3 not sended to background"
    handl.sendline("sleep 5")
    handl.expect_exact(prompt)
    handl.sendline("ps aux | grep sleep | head -n 1")
    handl.expect_exact(prompt)
    assert "sleep 3" not in handl.before, "Error, program sleep 3 not executed in background"
    handl.terminate(force=True)


def test_jobs(program):
    handl = pexpect.spawn(program, encoding="utf-8")
    handl.expect(".+")
    prompt = handl.after
    handl.sendline("sleep 5 &")
    handl.expect_exact(prompt)
    handl.sendline("jobs")
    handl.expect_exact(prompt)
    assert "sleep 5" in handl.before, "Jobs is not working or not printing the job"
    handl.sendline("sleep 6 &")
    handl.expect_exact(prompt)
    handl.sendline("sleep 3 &")
    handl.expect_exact(prompt)
    handl.sendline("jobs")
    handl.expect_exact(prompt)
    assert "sleep 3" in handl.before and "sleep 6" in handl.before
    handl.terminate(force=True)


def test_fg(program):
    handl = pexpect.spawn(program, encoding="utf-8")
    handl.expect(".+")
    prompt = handl.after
    handl.sendline("sleep 5 &")
    handl.expect_exact(prompt)
    handl.sendline("sleep 3")
    handl.expect_exact(prompt)
    start = time.time()
    handl.sendline("fg 1")
    handl.expect_exact(prompt, timeout=3)
    elapsed = int((time.time() - start))
    assert elapsed <= 2, "Sleep not running in fg"
    handl.terminate(force=True)
