from handler import ShellHandler
import pytest


@pytest.fixture()
def program(pytestconfig):
    return pytestconfig.getoption("program")


def test_ctrlc_interruption(program):
    handl = ShellHandler(program)
    for _ in range(5):
        handl.do_interrupt()
        assert handl.is_alive() and handl.do_wait_prompt(
        ), "Shell must ignore ctrl + c"

    handl.do_cmd_nowait("cat")
    handl.do_interrupt()
    if not handl.do_wait_prompt(1):
        assert False, "Cat command must finish after ctrl + c"

    handl.do_cmd_nowait("python")
    handl.do_interrupt()
    assert not handl.do_wait_prompt(
        1), "Python should not be killed by first ctrl+c"
    handl.do_interrupt()
    assert handl.do_wait_prompt(1), "Python should be killed by second ctrl+c"

    handl.do_cmd_nowait("cat &")
    assert handl.do_wait_prompt(1), "Cat & not running in background"
    handl.do_interrupt()
    handl.do_wait_prompt()
    cmd_result = handl.do_input("jobs | grep --color=never cat")
    assert "cat" in "".join(cmd_result.split("\r\n")[1:])
    handl.do_end()
