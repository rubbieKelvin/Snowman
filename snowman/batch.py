import logging
import requests

from typing import Any
from typing import List
from typing import Dict
from typing import Callable

logger = logging.getLogger("snowman.batch")

class SnowBatch:
	def __init__(self, name: str|None, variables: Dict[str, Any]|None=None) -> None:
		"""manages batch tests"""
		self.name = name
		self.variables = variables
		self.session: requests.Session = requests.Session()
		self.cells: List[Callable[[requests.Session, Dict[str, Any]|None], bool]] = []

	def step(self, func: Callable[[requests.Session, Dict[str, Any]|None], bool]):
		def inner():
			self.cells.append(func)
		return inner()

	def run(self):
		for cell in self.cells:
			if not cell(self.session, self.variables):
				logger.error(f'batch cell {self.name}:{cell.__name__} returned false')
				break
		else:
			logger.info(f'all cells on "{self.name}" ran succesfully.')
