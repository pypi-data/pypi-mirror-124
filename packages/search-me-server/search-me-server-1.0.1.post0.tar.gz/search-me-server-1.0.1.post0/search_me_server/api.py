# -*- coding: utf-8 -*-
import asyncio
import enum
import functools
import io
import json
import logging
import os
import sys
from dataclasses import dataclass, asdict, field
from logging.handlers import RotatingFileHandler
from typing import Any, Awaitable, Callable, Dict

import aiofiles
from aiohttp.web import (
	HTTPException, Application, Request, Response, StreamResponse,
	json_response, run_app, get, post
	)
from desert import metadata, schema
from marshmallow import fields, validate, ValidationError
from search_me import Google, Searx, Rambler


__app_name__ = "SEARCH-ME-SERVER"
__encoding__ = "UTF-8"
__base_dir__ = os.getcwd()


server_logger = logging.getLogger(__app_name__)
server_stream = logging.StreamHandler()
server_stream.setFormatter(
	logging.Formatter(
		"%(asctime)s	|	%(levelname)s	|	%(name)s	|	%(message)s"
		)
	)
server_logger.addHandler(server_stream)
server_logger.addHandler(logging.NullHandler())


@dataclass
class Data(fields.Field):

	def to_dict(self):
		return asdict(self)


@dataclass
class SettingsServer(Data):
	host: str = field(metadata=metadata(
		fields.Str(required=False)
		), default="127.0.0.1")
	port: int = field(metadata=metadata(fields.Int(
		required=False,
		validate=validate.Range(min=5000, error="Server port must be >= 5000")
		)), default=8080)
	api: str = field(metadata=metadata(fields.Str(required=False)), default="/")
	log_format: str = field(metadata=metadata(
		fields.Str(required=False)
		), default="%t	|	%s	|	%a	|	%Tf")

	def __post_init__(self):
		if not (self.api.startswith("/") or self.api.endswith("/")):
			server_logger.error(f"E01	|	{Errors.get_msg_by_code('E01')}")
			sys.exit()


@dataclass
class SettingsLog(Data):
	file: str = field(metadata=metadata(
		fields.Str(required=False)
		), default="main.log")
	size: int = field(metadata=metadata(
		fields.Int(
			required=False,
			validate=validate.Range(min=10, error="Log file size must be >= 10 bytes")
			)
			), default=100000000)
	format: str = field(metadata=metadata(
		fields.Str(required=False)
		), default="%(asctime)s	|	%(levelname)s	|	%(message)s")
	buffer: int = field(metadata=metadata(
		fields.Int(required=False)
		), default=io.DEFAULT_BUFFER_SIZE * 2)


@dataclass
class Settings(Data):
	log: bool = field(metadata=metadata(
		fields.Boolean(required=False)
		), default=True)
	log_options: Dict = field(metadata=metadata(
		fields.Dict(required=False)
		), default_factory=SettingsLog)
	server: Dict = field(metadata=metadata(
		fields.Dict(required=False)
		), default_factory=SettingsServer)
	engine: Any = field(default_factory=Google)

	def __post_init__(self):
		if not(
			isinstance(self.engine, Google) or
			isinstance(self.engine, Searx) or
			isinstance(self.engine, Rambler)
			):
			server_logger.error(f"E02	|	{Errors.get_msg_by_code('E02')}")
			sys.exit()


class Errors(enum.Enum):
	E01 = "Api must by like .../api/v1/..."
	E02 = "Chosen object is not engine from package search-me"
	E03 = enum.auto()

	@classmethod
	@functools.lru_cache(maxsize=4)
	def get_msg_by_code(cls, error_code):
		for code, _ in cls.__members__.items():
			if code == error_code:
				return getattr(cls, code).value


class Utils:

	@staticmethod
	def catch_log(func: Callable[[Request], Awaitable[Response]]):

		async def wrapper(*args, **kwargs) -> Response:
			_, request = args
			msg = f"{request.remote}	|	{request.rel_url}"
			logger = request.app.logger if hasattr(
				request.app,
				"logger"
				) else server_logger
			try:
				f = await func(*args, **kwargs)
			except asyncio.CancelledError:
				raise
			except (HTTPException, Exception) as e:
				logger.error(f"{msg}	|	{str(e)}")
				return json_response({"status": "error"}, status=500)
			else:
				logger.debug(f"{msg}	|	OK")
				return f
		return wrapper


class SearchMeServer:

	def __init__(self, **kwargs) -> None:
		settings_schema = schema(Settings)
		if kwargs:
			try:
				self.settings = settings_schema.load(kwargs)
				self.settings.log_options = SettingsLog(**self.settings.log_options)
				self.settings.server = SettingsServer(**self.settings.server)
			except ValidationError as e:
				server_logger.error(f"E03	|	{str(e)}")
				sys.exit()
		else:
			self.settings = Settings()
		self.init_app()

	def __str__(self) -> str:
		return f"{__app_name__}()"

	def __repr__(self) -> str:
		return f"{__app_name__}({self.settings})"

	def init_app(self) -> None:
		self.app = Application()
		self.app["E"] = self.settings.engine
		self.init_routes()
		if self.settings.log:
			self.init_logger()

	def init_routes(self) -> None:
		self.app.add_routes([
			get(
				f'{self.settings.server.api}logs',
				self.display_logs
				),
			post(
				f'{self.settings.server.api}',
				self.accept_request
				)
			])

	def init_logger(self) -> None:
		logger = RotatingFileHandler(
			self.settings.log_options.file,
			maxBytes=self.settings.log_options.size
			)
		logger.setLevel(logging.DEBUG)
		logger.setFormatter(
			logging.Formatter(self.settings.log_options.format)
			)
		self.app.logger.setLevel(logging.DEBUG)
		self.app.logger.addHandler(logger)

	def run(self):
		run_app(
			self.app,
			host=self.settings.server.host,
			port=self.settings.server.port,
			access_log_format=self.settings.server.log_format
			)

	@staticmethod
	@functools.lru_cache(maxsize=64)
	def encode_msg(msg):
		return msg.encode(__encoding__)

	def get_stream_resp(self, mime="application/json"):
		resp = StreamResponse()
		resp.content_type = mime
		return resp

	@Utils.catch_log
	async def display_logs(self, request) -> StreamResponse:
		stream = self.get_stream_resp(mime="text/plain")
		await stream.prepare(request)
		async with aiofiles.open(self.settings.log_options.file) as f:
			while True:
				logs = await f.read(self.settings.log_options.buffer)
				await stream.write(self.encode_msg(msg=logs))
				if not logs:
					break
		return stream

	@Utils.catch_log
	async def accept_request(self, request) -> StreamResponse:
		engine, query = request.app["E"], request.rel_url.query['q']
		await engine.search(query)
		stream = self.get_stream_resp()
		await stream.prepare(request)
		async for result in engine.results:
			await stream.write(
				self.encode_msg(msg=json.dumps(result.to_dict()))
				)
		return stream


__all__ = ["SearchMeServer"]
