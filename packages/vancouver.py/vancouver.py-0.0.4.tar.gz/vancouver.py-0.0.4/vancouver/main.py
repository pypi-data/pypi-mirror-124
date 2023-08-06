import json

import base64
import requests

from pathlib import Path


class NotFound:
	def __init__(self, message):
		self.message = message

		print(message)

	def __str__(self):
		return f'https://0.0.0.0/'

class BadArgument:
	def __init__(self, message):
		self.message = message

		print(message)

	def __str__(self):
		return f'https://0.0.0.0/'

class UnknowError:
	def __init__(self, message):
		self.message = message

		print(message)

	def __str__(self):
		return f'https://0.0.0.0/'

def get_imgbb_token(st: str = ""):
	import vancouver

	pt = vancouver.__file__
	pt = pt.replace("__init__.py", "config.json")

	if Path(f"{pt}").is_file() != True:
		fp = open(pt, "a+")
		fp.write("{}")
		fp.close()

	with open(pt, "r") as f:
		j = json.load(f)

		if j.get("token", None) == None:
			with open(pt, "w") as ri:
				j["token"] = input(f"{st}> ")
			
				json.dump(j, ri, indent = 4)

				return str(j["token"])
		else:
			return str(j["token"])

def Init():
	get_imgbb_token()

def File(path: str = ""):
	if Path(f"{path}").is_file() != True:
		return NotFound(
			"File not found.\nCheck if the filename is correct"
		)
	else:
		with open(path, "rb") as file:
			payload = {
				"key":   get_imgbb_token(st = "IMGbb token "),
				"image": base64.b64encode(file.read()),
			}

			response = requests.post(
				"https://api.imgbb.com/1/upload", 
				payload
			)

		try:
			jv = response.json()

			if jv["success"] != True:
				return BadArgument("Bad Request. \nThis may been: Empty upload source.")
			else:
				return jv["data"]["url"]
		except:
			return UnknowError("Unknow error")