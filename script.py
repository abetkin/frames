
def main():
    import getopt

    opts, args = getopt.getopt(sys.argv[1:], 'hc:', ['--help', '--command='])

    if not args:
        print(_usage)
        sys.exit(2)

    commands = []
    for opt, optarg in opts:
        if opt in ['-h', '--help']:
            print(_usage)
            sys.exit()
        elif opt in ['-c', '--command']:
            commands.append(optarg)

    mainpyfile = args[0]     # Get script filename
    if not os.path.exists(mainpyfile):
        print('Error:', mainpyfile, 'does not exist')
        sys.exit(1)

    sys.argv[:] = args      # Hide "pdb.py" and pdb options from argument list

    # Replace pdb's dir with script's dir in front of module search path.
    sys.path[0] = os.path.dirname(mainpyfile)

    # Note on saving/restoring sys.argv: it's a good idea when sys.argv was
    # modified by the script being debugged. It's a bad idea when it was
    # changed by the user from the command line. There is a "restart" command
    # which allows explicit specification of command line arguments.
    pdb = Pdb()
    pdb._runscript(mainpyfile)



def _runscript(self, filename):
    # The script has to run in __main__ namespace (or imports from
    # __main__ will break).
    #
    # So we clear up the __main__ and set several special variables
    # (this gets rid of pdb's globals and cleans old variables on restarts).
    import __main__
    __main__.__dict__.clear()
    __main__.__dict__.update({"__name__"    : "__main__",
                                "__file__"    : filename,
                                "__builtins__": __builtins__,
                                })

    # When bdb sets tracing, a number of call and line events happens
    # BEFORE debugger even reaches user's code (and the exact sequence of
    # events depends on python version). So we take special measures to
    # avoid stopping before we reach the main script (see user_line and
    # user_call for details).
    self._wait_for_mainpyfile = True
    self.mainpyfile = self.canonic(filename)
    self._user_requested_quit = False
    with open(filename, "rb") as fp:
        statement = "exec(compile(%r, %r, 'exec'))" % \
                    (fp.read(), self.mainpyfile)
    self.run(statement)