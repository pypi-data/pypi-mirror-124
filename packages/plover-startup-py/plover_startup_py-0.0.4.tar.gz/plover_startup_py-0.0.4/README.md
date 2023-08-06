# plover-startup-py
Quick and dirty plugin to run something when Plover starts.

### About plugin

This plugin should only used for testing purposes. See also:

* [user202729/plover-debugging-console: A IPython debugging console for Plover.](https://github.com/user202729/plover-debugging-console)
* [user202729/plover-run-py: Command plugin for Plover to run an arbitrary Python command.](https://github.com/user202729/plover-run-py)

Disadvantages in comparison to writing an extension plugin:

* Can only be used on a single machine.

   However, it should not be hard to convert a configuration file into an extension plugin to be distributed.

Advantages over writing an extension plugin:

* For testing purposes, the user-provided code might have some bug/errors.

   While using a normal extension plugin might make Plover nonfunctional (for example if `stop()` raises
   an error, Plover quit will be interrupted), this module guarantees that Plover is never interrupted.

* Has a reload command, which is faster than restarting Plover.

* Some convenience functions to make hacks easier to achieve. (will be available later)

### Installation

The package can be installed from pip or GitHub.

### Configuration

You need to create a file named `plover_startup_py_config.py` in Plover's configuration folder
(see https://plover.readthedocs.io/en/latest/api/oslayer_config.html#plover.oslayer.config.CONFIG_DIR
for where it is exactly)

The file must define two functions `start` and `stop`, each receives the engine as the only input parameter:

```python
def start(engine):
	pass

def stop(engine):
	pass
```

They will be called when the plugin starts/stops (which is normally when Plover starts/exits)

### Usage

Go to "Plugins" tab of Plover configuration, enable the plugin named "plover_startup_py".

To view the full traceback/error messages, you may need to invoke Plover with `--log-level debug`.

There's also an additional command `{plover:plover_startup_py_reload}` for reloading the module.
