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
		""" manages a single request class using the snow file at path 
		"""
		self.env = env
		self.path = path

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
		self.require: str = _data.get("require", version_tuple_to_str(VERSION))
		self.check_version()


	@property
	def url(self) -> str:
		return Template(self._url).safe_substitute(self.mapping())

	def __str__(self) -> str:
		return f"<{self.__class__.__name__} [{self.method.upper()}] {self.url}>"

	def __repr__(self) -> str:
		return str(self)

	def call(self, session: requests.Session, /, variables: Union[Dict[str, Any], None]=None) -> Union[requests.Response, None]:
		logger.info(f"calling {self}")
		request = requests.Request(method=self.method, url=self.url)
		body_type: Union[str, None] = self.body.get("type")
		evaluated_vars = self.mapping(variables)

		if body_type == "json" or body_type == "formdata":
			_data = self.body.get("data", {})
			self.reconstructDict(_data, evaluated_vars)

			if body_type == "json":
				request.json = _data
			else:
				request.data = _data

		elif body_type == "raw":
			request.data = Template(self.body.get("data", ""))\
				.safe_substitute(evaluated_vars)

		_headers = self.headers
		self.reconstructDict(_headers, evaluated_vars)
		request.headers = _headers

		prepped = request.prepare()

		try:
			response: requests.Response = session.send(prepped)
			message = "{self} status={status}"
			
			if response.status_code >= 500:
				logger.error(message.format(self=self, status=response.status_code))
			elif response.status_code >= 300 or response.status_code < 200:
				logger.warning(message.format(self=self, status=response.status_code))
			else:
				logger.info(message.format(self=self, status=response.status_code))

			return response
		except requests.exceptions.ConnectionError as e:
			logger.fatal(f"{e.__class__.__name__} -> {e}")

	def mapping(self, /, variables: Union[Dict[str, Any], None]=None) -> Dict[str, Any]:
		return {**self.env.data, **(variables or {})}

	def check_version(self):
		required_version = version_tuple_from_str(self.require)
		# if not (VERSION[0] == (rv0:=required_version[0])):
		# 	warnings.warn(f"{self} requires version {rv0}.x.x, got {version_tuple_to_str(VERSION)} instead.")
		for i in range(3):
			if (i!=0) and required_version[i]==None:
				continue

			if VERSION[i] != required_version[i]:
				warnings.warn(f'{self} requires version {".".join([str(_ or "x") for _ in required_version])}, got {version_tuple_to_str(VERSION)} instead.')
				break

	def reconstructDict(self, dictionary: Dict[str, Any], /, variables: Union[Dict[str, Any], None]=None):
		for key, value in dictionary.items():
			if type(value) == str:
				dictionary[key] = Template(value).safe_substitute(variables or {})
			elif type(value) == dict:
				self.reconstructDict(dictionary[key], variables)
