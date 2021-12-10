import json
from pathlib import Path
from typing import Any, Dict

class SnowEnv:
	def __init__(self, path:Path) -> None:
		""" Manages the environmental variable at path
		"""
		self.path: Path = path
		self.data: Dict[str, Any] = dict()

		with open(self.path) as file:
			self.data: Dict[str, Any] = json.load(file)
	
	def get(self, key: str, default: Any) -> Any:
		return self.data.get(key, default)

	def set(self, key: str, value: Any) -> None:
		self.data[key] = value
		self._save()

	def _save(self):
		with open(self.path, "w") as file:
			json.dump(self.data, file, indent=4)

	def remove(self, key: str):
		if key in self.data:
			del self.data[key]
			self._save()
