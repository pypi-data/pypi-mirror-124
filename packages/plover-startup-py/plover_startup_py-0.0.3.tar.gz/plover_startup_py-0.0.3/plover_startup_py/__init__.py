import importlib.util
from typing import Any, Optional
from pathlib import Path
import sys

import plover  # type: ignore

class Main:
	module: Any
	plugin_running: bool

	def __init__(self, engine: "plover.engine.StenoEngine") -> None:
		self.engine=engine
		self.plugin_running=False

		try:
			self.load_module()
		except:
			plover.log.error("while running plover_startup_py:__init__", exc_info=True)

		global instance
		assert instance is None
		instance=self

	def load_module(self)->None:
		"""
		Function to (re)load the module.

		Might raise an error if the module failed to load.
		"""
		if self.plugin_running:
			self.stop()
			try:
				self.load_module()
			finally:
				self.start()
			return

		spec = importlib.util.spec_from_file_location(
				name="plover_startup_py_module",
				location=Path(plover.oslayer.config.CONFIG_DIR)/"plover_startup_py_config.py")
		self.module = importlib.util.module_from_spec(spec)
		assert spec.loader is not None
		spec.loader.exec_module(self.module)  # type: ignore

	def start(self) -> None:
		"""
		Function to start the extension plugin. Called by Plover.

		Will never raise an error. Direct error log to plover.log instead.
		"""
		assert not self.plugin_running
		self.plugin_running=True
		try:
			self.module.start(self.engine)
		except:
			plover.log.error("while running plover_startup_py:start", exc_info=True)

	def stop(self) -> None:
		"""
		Function to stop the extension plugin. Called by Plover.

		Will never raise an error. Direct error log to plover.log instead.
		"""
		try:
			self.module.stop(self.engine)
		except:
			plover.log.error("while running plover_startup_py:stop", exc_info=True)
		assert self.plugin_running
		self.plugin_running=False

instance: Optional[Main]=None

def reload(engine, argument: str)->None:
	if instance is None:
		plover.log.error("The extension plugin is not running!")
		return
	instance.load_module()
