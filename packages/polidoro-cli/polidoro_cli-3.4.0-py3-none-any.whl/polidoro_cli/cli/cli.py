import os
import re
import sys
from argparse import SUPPRESS
from string import Template
from subprocess import Popen, PIPE

from polidoro_argument import Command
from polidoro_argument.polidoro_argument_parser import DEFAULT_COMMAND


class CLI:
    """
    Class to create CLI commands
    """

    @staticmethod
    def create_file_commands(full_path):
        """
        Create commands reading from file
        """
        file = full_path.split('/')[-1]
        clazz_name = file.split('.')[0].title()
        clazz = getattr(sys.modules.get(clazz_name.lower(), None), clazz_name, None)
        if clazz is None:
            clazz = type(clazz_name, (object,), {})

        if not hasattr(clazz, 'help'):
            setattr(clazz, 'help', clazz.__qualname__ + ' CLI commands')

        local_vars = {}
        read_dict = False
        name = None
        command = ""
        with open(full_path, 'r', newline='') as file:
            for line in file.readlines():
                line = line.strip()
                if line and not line.startswith('#'):
                    # set local variables defined in .cli file with `set VAR`
                    if line.startswith('set '):
                        local_var, _, value = line[4:].partition('=')
                        if local_var == 'DEFAULT_COMMAND':
                            setattr(clazz, DEFAULT_COMMAND, value)
                            CLI._create_command(DEFAULT_COMMAND, value, clazz, help=SUPPRESS, **local_vars)
                        else:
                            local_vars[local_var] = value
                    elif line.startswith('export '):
                        env_var, _, value = line[7:].partition('=')
                        os.environ[env_var] = value
                    elif read_dict:
                        command += line
                        read_dict = CLI._create_evalueted_command(clazz, command, local_vars, name)
                    else:
                        name, _, command = line.partition('=')
                        if command.startswith('{'):
                            read_dict = CLI._create_evalueted_command(clazz, command, local_vars, name)
                        else:
                            final_command = []
                            for cmd in command.split(';'):
                                if hasattr(clazz, DEFAULT_COMMAND):
                                    cmd = f'{getattr(clazz, DEFAULT_COMMAND)} {cmd}'
                                final_command.append(cmd)
                            CLI._create_command(name, ';'.join(final_command), clazz, **local_vars)

    @staticmethod
    def _create_evalueted_command(clazz, command, local_vars, name):
        try:
            command_dict = eval(command)
            command = command_dict.pop('command')
            CLI._create_command(name, command, clazz, **command_dict, **local_vars)
            return False
        except SyntaxError:
            return True

    @staticmethod
    def _create_command(name, command, clazz, show_cmd=True, help=None,
                        messages=None,
                        **local_vars):
        run_cmd = getattr(clazz, 'get_cmd_method', CLI._get_cmd_method)(
            command,
            clazz,
            show_cmd=show_cmd,
            messages=messages,
            **local_vars)
        aliases = name.replace(' ', '').split(',')
        name = aliases.pop(0)
        # Parser full name
        setattr(run_cmd, '__qualname__', '%s.%s' % (clazz.__qualname__, name))
        # Command name
        setattr(run_cmd, '__name__', name)
        # Command class
        setattr(run_cmd, '__objclass__', clazz)
        if help is None:
            help = f'Run "{command}"'
        Command(help=help, aliases=aliases)(run_cmd)

    @staticmethod
    def _get_cmd_method(command, clazz, show_cmd=True, exit_on_fail=True, messages=None, **local_vars):
        if messages is None:
            messages = {}

        def print_if_has_message(message_key):
            if message_key in messages:
                print(messages[message_key])

        def run_cmd_method(*_remainder, docker=False):
            if docker is None:
                docker = True
            docker_class = getattr(sys.modules['docker'], 'Docker', None)
            interceptors = []
            substituted_command = Template(command).safe_substitute(**local_vars)
            interceptors_kwargs = {}
            if docker_class:
                if docker:
                    # If the argument --docker/-d in arguments, replace "$docker" (if exists) in command
                    interceptors.append(docker_class.command_interceptor)
                    substituted_command = Template(substituted_command).safe_substitute(
                        docker='docker-compose exec $service',
                    )
                    # Include environments variables to docker-compose call
                    interceptors_kwargs.update(local_vars)
                    if isinstance(docker, str):
                        interceptors_kwargs['service'] = docker
                else:
                    substituted_command = Template(substituted_command).safe_substitute(
                        docker=''
                    )

            if hasattr(clazz, 'command_interceptor'):
                interceptors.append(clazz.command_interceptor)

            for interceptor in interceptors:
                substituted_command, _remainder = interceptor(substituted_command, *_remainder, **interceptors_kwargs)

            if '$args' in substituted_command:
                substituted_command = Template(substituted_command).safe_substitute(args=' '.join(_remainder))
                _remainder = ()

            args_to_substitute = {}
            for arg in _remainder:
                arg_key = f'arg{len(args_to_substitute)}'
                if f'${arg_key}' in substituted_command:
                    args_to_substitute[arg_key] = arg
                else:
                    break
            _remainder = tuple(list(_remainder)[len(args_to_substitute):])
            substituted_command = Template(substituted_command).safe_substitute(**args_to_substitute)

            print_if_has_message('start')
            try:
                for cmd in substituted_command.split(';'):
                    cmd = cmd.replace('  ', ' ').strip()
                    compiled = compile_command(cmd, *_remainder)
                    run_command(compiled)
            except SystemExit as se:
                if se.code:
                    print_if_has_message('error')
                print_if_has_message('finish')

        def compile_command(cmd, *_remainder):
            cmd = cmd.strip()
            _for = re.search(r'(.*) for (\w+) in (.*)', cmd)
            if _for:
                for_cmd = _for.groups()[0]
                for_var = _for.groups()[1]
                for_in = _for.groups()[2]

                # Replacing for var for '%s'
                for_cmd = ' '.join(['$for_var' if c == for_var else c for c in for_cmd.split()] + list(_remainder))
                return eval('[Template(\'' + for_cmd + '\').safe_substitute(for_var=' + for_var + ') for ' +
                            for_var + ' in ' + for_in + ']')
            elif cmd.lower().startswith('run'):
                cmds = re.search('run(.*)in(.*)done', cmd).groups()
                return 'cd %s; %s; cd..' % (cmds[1], cmds[0])
            else:
                return ' '.join([cmd] + list(_remainder))

        def run_command(cmd):
            if isinstance(cmd, list):
                for c in cmd:
                    run_command(c)
            elif isinstance(cmd, str):
                if cmd.lower().startswith('cd'):
                    os.chdir(os.path.expanduser(cmd[2:].strip()))
                else:
                    CLI.execute(cmd, show_cmd=show_cmd, exit_on_fail=exit_on_fail)
            else:
                print_if_has_message('error')
                raise Exception

        # method without "docker" argument
        def run_docker_cmd_method(*_remainder):
            run_cmd_method(*_remainder)

        if clazz.__name__ == 'Docker':
            return run_docker_cmd_method
        else:
            setattr(run_cmd_method, 'arguments_aliases', {'docker': 'd'})
            return run_cmd_method

    @staticmethod
    def execute(command, exit_on_fail=True, capture_output=False, show_cmd=True):
        """
        Run a shell command

        :param command: command as string
        :param exit_on_fail: If True, exit script if command fails
        :param capture_output: Return the command output AND not print in terminal
        :param show_cmd: Show command in terminal
        :return: subprocess.CompletedProcess
        """
        if show_cmd:
            print('+ %s' % command.strip())

        if capture_output:
            std = PIPE
        else:
            std = None

        proc = Popen('exec ' + command, shell=True, text=True, stdout=std, stderr=std)
        try:
            outs, errs = proc.communicate()
        except KeyboardInterrupt:
            proc.terminate()
            print('Waiting until process terminate')
            proc.wait()
            outs, errs = proc.communicate()
            proc.returncode = 1

        if exit_on_fail and proc.returncode:
            exit(proc.returncode)
        return outs, errs


@Command(help='Create suggested aliases')
def create_aliases():
    aliases = dict(
        dk='docker',
        dj='django',
        ex='elixir',
        rb='ruby',
        g='git',
        npm='npm',
        pyt='pytest'
    )
    for bash_line in CLI.execute('bash -ixlc :', capture_output=True, show_cmd=False)[1].split('\n'):
        if 'alias' in bash_line and '=' in bash_line:
            alias = re.sub('.*alias (.*)', '\\1', bash_line)
            if alias[0] == '\'' == alias[-1]:
                alias = alias[1:-1]
            alias, _, cmd = alias.partition('=')
            if alias in aliases:
                cli_alias = f'cli {aliases[alias]}'
                if cmd != cli_alias:
                    print(f'Cant create alias "{alias}={cli_alias}", alias {alias} already exists "{alias}={cmd}"')
                aliases.pop(alias)

    for alias, cmd in aliases.items():
        bash_alias = f'{alias}=\'cli {cmd}\''
        print(f'Creating alias {bash_alias}')
        alias_file = os.path.expanduser('~/.bashrc')
        if os.path.exists(os.path.expanduser('~/.bash_aliases')):
            alias_file = os.path.expanduser('~/.bash_aliases')

        with open(alias_file, 'a+') as file_object:
            file_object.seek(0)
            data = file_object.read()
            if data[-1] != '\n':
                file_object.write('\n')
            file_object.write(f'alias {bash_alias}\n')

    if aliases:
        print('Run "source ~/.bashrc" to load the aliases')

