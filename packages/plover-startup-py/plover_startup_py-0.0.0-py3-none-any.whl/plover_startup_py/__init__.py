import importlib.util
from typing import Any, TYPE_CHECKING
from pathlib import Path

import plover  # type: ignore

class Main:
	module: Any

	def __init__(self, engine: "plover.engine.StenoEngine") -> None:
		self.engine=engine
		spec = importlib.util.spec_from_file_location(
				name="plover_startup_py_module",
				location=Path(plover.oslayer.config.CONFIG_DIR)/"plover_startup_py_config.py")
		self.module = importlib.util.module_from_spec(spec)
		assert spec.loader is not None
		spec.loader.exec_module(self.module)

	def start(self) -> None:
		self.module.start(self.engine)

	def stop(self) -> None:
		self.module.stop(self.engine)
