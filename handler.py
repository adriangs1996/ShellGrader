import pexpect


class ShellHandler:
    def __init__(self, program):
        self.prog = pexpect.spawn(program, encoding="utf-8")
        self.prog.expect(".+")  # must print a prompt
        self.__custom_prompt = self.prog.after

    def do_input(self, strng):
        self.prog.sendline(strng)
        self.prog.expect_exact(self.__custom_prompt)
        return self.prog.before

    def do_interrupt(self):
        self.prog.sendintr()

    def do_cmd_nowait(self, cmd):
        self.prog.sendline(cmd)

    def do_wait_prompt(self, timeout=-1):
        try:
            self.prog.expect_exact(self.__custom_prompt, timeout=timeout)
            return True
        except Exception:
            return False

    def do_end(self, exit_command="exit"):
        self.prog.terminate(force=True)

    def is_alive(self):
        return self.prog.isalive()
