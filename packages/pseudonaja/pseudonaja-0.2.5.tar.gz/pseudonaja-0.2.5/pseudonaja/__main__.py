import sys
import pseudonaja.c.PInterpreter as pcint
import pseudonaja.debug as debug
debug.debug_flag = False

if len(sys.argv) == 1:
    pcint.PInterpreter().repl()
else:
    for file in sys.argv[1:]:
        try:
            with open(file, "r") as prog:
                prog = prog.read()
                pcint.PInterpreter().run(prog)

        except FileNotFoundError as e:
            print(f"{e}")