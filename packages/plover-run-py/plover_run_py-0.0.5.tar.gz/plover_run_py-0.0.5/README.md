# plover-run-py
Command plugin for Plover to run an arbitrary Python command.

**Warning**: While this plugin can do everything what a command plugin can, this should
only be used for personal usage. If the usage is sufficiently general, it's recommended to make
a Plover command plugin instead.

It's also possible to execute a command from the command-line, using
[the `plover_send_command` script](https://plover.readthedocs.io/en/latest/cli_reference.html#sending-commands).
Unfortunately, this method takes about 1.5s per call due to Plover's overhead.

If `python -m plover.scripts.send_command` is used, the time is reduced to 0.3s per call,
mostly because of `pkg_resources` import.

### See also

* [`plover-run-shell` plugin](https://github.com/user202729/plover_run_shell) for running a shell command.
* [`plover-debugging-console` plugin](https://github.com/user202729/plover-debugging-console) for
running Python commands in Plover in a shell (more convenient for debugging and showing results).
* [`plover-retro-stringop` plugin](https://github.com/buffet/plover_retro_stringop) for
running Python commands to transform/modify the previous text using arbitrary Python expression.

## Usage

In order to use this plugin in [Plover](https://github.com/openstenoproject/plover) you need to
create a dictionary entry of the form:

``` json
{
    "example_stroke": "{PLOVER:PY:command}"
}
```

Variables `engine` and `plover` are provided.

Remember to escape the characters in `\{}` according to Plover's dictionary format.

Alternatively, if the definition has the form `"{PLOVER:PY_F:path}"`, the content of the file
at the given path will be run as Python code.

**Note**: If the command takes a long time to finish, Plover might freeze.

## Example

Refer to the API reference ([1](https://plover.readthedocs.io/en/latest/api_reference.html),
[2](https://plover2.readthedocs.io/en/latest/api_reference.html)) (unofficial, community-maintained)
for more details.

* Sleep between key presses: `{#a}{plover:py:import time; time.sleep(1)}{#b}`
* Toggle a plugin and show a warning notification on the status:
(broken into multiple lines for readability)
See also [user202729/plover-delay: Plover command plugin to sleep for some time.](https://github.com/user202729/plover-delay) for a dedicated plugin.

   ```
   {plover:py:
   engine["enabled_extensions"]^=\{'ibus'\};
   plover.log.warning('ibus enabled=' + str('ibus' in engine["enabled_extensions"]))
   }
   ```
