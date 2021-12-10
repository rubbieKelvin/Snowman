import os
import logging

from .snow import Snow
from .env import SnowEnv

from pathlib import Path
from requests import Session
from requests import Response

from typing import Dict
from typing import Any
from typing import Union

logging.basicConfig(
	level=logging.DEBUG,
	format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
	datefmt='%m-%d %H:%M',
	filename='snowman.log',
	filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(name)-6s: %(levelname)-6s %(message)s')
console.setFormatter(formatter)

logging.getLogger('').addHandler(console)

class Snowman:
	def __init__(self, root: Path, envfilename: str='env.json') -> None:
		self.root = root
		self.session = Session()

		self.env = SnowEnv(root/envfilename)
		self.files: Dict[str, Snow] = {
			os.path.splitext(filename)[0] : Snow(root/filename, self.env) \
			for filename in os.listdir(root) \
			if os.path.splitext(filename)[1].lower() == ".snow"
		}

	def call(self, name: str, data: Union[Dict[str, Any], None]=None) -> Union[Response, None]:
		snow: Snow = self.get(name)
		return snow.call(self.session, data)

	def get(self, name: str) -> Snow:
		return self.files[name]
