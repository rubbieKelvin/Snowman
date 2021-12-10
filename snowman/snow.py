import json
from pathlib import Path
from string import Template

from typing import Dict
from typing import Any
from typing import Union

from .env import SnowEnv
from .__sm import VERSION
from .__sm import APPNAME
from .__sm import version_tuple_to_str
from .__sm import version_tuple_from_str

import requests
import warnings
import logging

logger = logging.getLogger(f"snowman.snow")

class Snow:
	def __init__(self, path: Path, env: SnowEnv) -> None:
		self.path = path
		self.env = env

		with open(path) as file:
			_data: Dict[str, Any] = json.load(file)

		# call
		_call: Dict[str, Any] = _data.get("call", {})
		self._url: str = _call.get("url", "").strip()

		if not self._url:
			raise TypeError("url should not be empty")

		self.method: str = _call.get("method", "get")
		self.body: Dict[str, Any] = _call.get("body", {})
		self.params: Dict[str, str] = _call.get("params", {})
		self.cookies: Dict[str, str] = _call.get("cookies", {})
		self.headers: Dict[str, str] = {
			'user-agent': f'{APPNAME}/{version_tuple_to_str(VERSION)}',
			**_call.get("headers", {})
		}

		# config
		_config: Dict[str, Any] = _data.get("config", {})
		self.allow_redirects: bool = _config.get("allow_redirects", True)
		self.timeout: int = _config.get("timeout", 300)

		# require
		self.require: str = _data.get("require", str(VERSION[0]))
		self.check_version()


	@property
	def url(self) -> str:
		return Template(self._url).safe_substitute(self.mapping())

	def __str__(self) -> str:
		return f"<{self.__class__.__name__} [{self.method.upper()}] {self.url}>"

	def __repr__(self) -> str:
		return str(self)

	def call(self, data: Union[Dict[str, Any], None]=None):
		logger.info(f"calling {self}")
		requests.request(method=self.method, url=self.url)

	def mapping(self, data: Union[Dict[str, Any], None]=None) -> Dict[str, Any]:
		return {**self.env.data, **(data or {})}

	def check_version(self):
		required_version = version_tuple_from_str(self.require)
		if not (VERSION[0] == (rv0:=required_version[0])):
			warnings.warn(f"{self} requires version {rv0}.x.x, got {version_tuple_to_str(VERSION)} instead.")
