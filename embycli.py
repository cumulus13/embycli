#!c:/SDK/Anaconda2/python.exe
from __future__ import print_function
import os, sys
import requests
#from bs4 import BeautifulSoup as bs
from pydebugger.debug import debug
from make_colors import make_colors
import re
import ast
#from idm import IDMan
#from pywget import wget
import traceback
import argparse
import textwrap
import cmdw
if sys.version_info.major == 3:
	raw_input = input
	import urllib.parse as urllib
else:
	import urllib
from pause import pause
from configset import configset
from pprint import pprint
import json
import inspect
import signal


class Embycli(object):

	configname = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'embycli.ini')
	config = configset(configname)
	default_api = config.get_config('auth', 'api')
	api = default_api
	host = config.get_config('host', 'ip') or '127.0.0.1'
	port = config.get_config('host', 'port') or 8096
	url = None
	headers = {'Content-Type': 'application/json'}
	session = None
	user = None

	def __init__(self, api = None, host = None, port = None):
		super(Embycli, self)
		self.api = api or self.api
		self.host = host or self.host
		self.port = port or self.port

	@classmethod
	def get_api(self, host = None, port = None, api = None):
		if not api:
			api = self.api
		if not api:
			api = self.config.get_config('auth', 'api')
		if not api:
			api = self.config.get_config('auth', 'default')
		if not api:
			api = raw_input(make_colors("Input Token API: ", 'lw', 'lr', ['blink']))
		if not api:
			sys.exit(make_colors("Invalid Token API !", 'lw', 'lr', ['blink']))
		else:
			api = api.split(",")

		if not host:
			host = self.host
		if not host:
			host = self.config.get_config('host', 'ip')
		if not host:
			host = raw_input(make_colors("Host IP/Domain address: ", 'lw', 'lr', ['blink']))
		if not host:
			sys.exit(make_colors("Invalid IP/Domain Host address !", 'lw', 'lr', ['blink']))

		if not port:
			port = self.port
		if not port:
			port = self.config.get_config('host', 'port', '8096')
		if not port:
			port = raw_input(make_colors("Host Port: ", 'lw', 'lr', ['blink']))
		if port:
			try:
				port = int(port)
			except:
				sys.exit(make_colors("Invalid Port !", 'lw', 'lr', ['blink']))
		if api and isinstance(api, list) and host and port:
			for ap in api:
				session = requests.Session()
				headers = {'X-Emby-Token':str(ap)}
				session.headers.update(headers)
				self.url = 'http://' + str(host) + ":" + str(port)

				url = self.url + "/emby/Auth/Keys"
				params = {
					'SortBy': 'IsFolder,SortName',
					'SortOrder': 'Ascending',
					'Fields': 'BasicSyncInfo,ProductionYear,Status,EndDate',
					'ImageTypeLimit': '1',
					'EnableImageTypes': 'Primary,Backdrop,Thumb',
					'StartIndex': '0',
				}
				a = session.get(url, params = params)
				code = a.status_code
				debug(code = code)
				content = a.content
				debug(content = content)
				debug(url = a.url)
				list_api = []
				if not 'invalid' in content.decode() or not 'expired' in content:
					content = json.loads(content)
					for it in content.get('Items'):
						list_api.append(it.get('AccessToken'))
				debug(list_api = list_api)
				if list_api:
					break
			if not list_api:
				for ap in api:
					session = requests.Session()
					headers = {'Token':str(ap)}
					session.headers.update(headers)
					self.url = 'http://' + str(host) + ":" + str(port)
					url = self.url + "/Auth/Keys"
					a = session.get(url)
					code = a.status_code
					debug(code = code)
					content = a.content
					debug(content = content)
					debug(url = a.url)
					list_api = []
					if not 'invalid' in content.decode() or not 'expired' in content.decode():
						content = json.loads(content)
						for it in content.get('Items'):
							list_api.append(it.get('AccessToken'))
					debug(list_api = list_api)
					if list_api:
						break
			return list_api
		return []

	@classmethod
	def get_config(self, host = None, port = None, api = None, write_api = False):
		session = None
		if not api:
			api = self.api
		if not api:
			api = self.config.get_config('auth', 'api')
		if not api:
			api = self.get_api(host, port, api)
		if not api:
			api = raw_input(make_colors("Input Token API: ", 'lw', 'lr', ['blink']))
		if not api:
			sys.exit(make_colors("Invalid Token API !", 'lw', 'lr', ['blink']))
		else:
			if write_api:
				self.config.write_config('auth', 'api', api)

		if not host:
			host = self.host
		if not host:
			host = self.config.get_config('host', 'ip')
		if not host:
			host = raw_input(make_colors("Host IP/Domain address: ", 'lw', 'lr', ['blink']))
		if not host:
			sys.exit(make_colors("Invalid IP/Domain Host address !", 'lw', 'lr', ['blink']))
		else:
			if write_api:
				self.config.write_config('host', 'ip', host)

		if not port:
			port = self.port
		if not port:
			port = self.config.get_config('host', 'port', '8096')
		if not port:
			port = raw_input(make_colors("Host Port: ", 'lw', 'lr', ['blink']))
		if not port:
			print(make_colors("No Port given !, use default port: 8096", 'b', 'ly', ['blink']))
			port = '8096'
		if write_api:
			self.config.write_config('host', 'port', port)

		if port:
			try:
				port = int(port)
			except:
				sys.exit(make_colors("Invalid Port !", 'lw', 'lr', ['blink']))
		debug(self_api = self.api)
		debug(api = api)
		debug(self_host = self.host)
		debug(host = host)
		debug(port = port)
		if host and port:
			self.url = 'http://' + str(host) + ":" + str(port)
		if api and host and port:
			if isinstance(api, list):
				session = requests.Session()
				headers = {'X-Emby-Token':str(api[0]).strip()}
				session.headers.update(headers)
			else:
				session = requests.Session()
				headers = {'X-Emby-Token':str(api)}
				session.headers.update(headers)
		else:
			api = self.get_api(host, port, api)
			if api:
				session = requests.Session()
				headers = {'X-Emby-Token':str(api[0])}
				session.headers.update(headers)
		return session

	@classmethod
	def setting_get_users(self):
		if not self.session:
			self.session = self.get_config()
		url = self.url + "/emby/users"
		return self.session.get(url, headers = self.headers).json()

    @classmethod	
	def get_user(self):
		self.session = self.session or self.get_config()
		debug(self_session = self.session)
		users_url = f"{self.url}/emby/Users"
		params = {
			'api_key': self.api
		}
		response = self.session.get(users_url, params=params)
		data = response.json()
		debug(data=data)
		if list(filter(lambda k: 'debug' in k.lower(), os.environ)): jprint(data)
		
		USER_ID_DATA = []
		# Display user IDs
		for user in data:
			print(f"Username: {user['Name']}, User ID: {user['Id']}")
			USER_ID_DATA.append([user['Id'], user['Name']])
		
		if len(USER_ID_DATA) > 1:
			n = 1
			for u in USER_ID_DATA:
				print(
					make_colors(str(n).zfill(2), 'lc') + ". " +
					make_colors(u[1], 'b', 'y') + " " +
					make_colors(u[0], 'lw', 'bl')
				)
		
			n += 1
		
			q = input(make_colors("Select user:", 'lw', 'r') + " ")
			if q and q.isdigit() and int(q) <= len(USER_ID_DATA):
				self.user_id = USER_ID_DATA[int(q) - 1][0]
				return USER_ID_DATA[int(q) - 1][0]
		else:
			self.user_id = USER_ID_DATA[0][0]
			return USER_ID_DATA[0][0]
		
		return ''
		


	@classmethod
	def setting_get_dlna(self):
		if not self.session:
			self.session = self.get_config()
		url = self.url + "/emby/System/Configuration/dlna"
		return self.session.get(url, headers = self.headers).json()
	
	@classmethod		
	def format_argument(self, argument):
		arg = re.split("_", argument)
		debug(arg = arg)
		arg_1 = []
		for i in arg:
			arg_1.append(str(i).title())
		debug(arg_1 = arg_1)
		return "".join(arg_1)
	
	@classmethod		
	def setting_set_dlna(self, enable_server=True, enable_play_to=True, enable_debug_log=True, blast_alive_messages=True, client_discovery_interval_seconds=60, alive_message_interval_seconds=1800, default_user_id=None):
		if not default_user_id:
			default_user_id = self.setting_get_users()[0].get('Id')
		if enable_server == False or enable_server == 0:
			enable_server = "false"
		else:
			enable_server =  "true"
		if enable_play_to== False or enable_play_to== 0:
			enable_play_to= "false"
		else:
			enable_play_to=  "true"
		if enable_debug_log == False or enable_debug_log == 0:
			enable_debug_log = "false"
		else:
			enable_debug_log =  "true"
		if blast_alive_messages == False or blast_alive_messages == 0:
			blast_alive_messages = "false"
		else:
			blast_alive_messages =  "true"
		if client_discovery_interval_seconds == False or client_discovery_interval_seconds == 0:
			client_discovery_interval_seconds = "false"
		else:
			client_discovery_interval_seconds =  "true"
		if alive_message_interval_seconds == False or alive_message_interval_seconds == 0:
			alive_message_interval_seconds = "false"
		else:
			alive_message_interval_seconds =  "true"

		data = {
			'EnableServer':enable_server,
			'EnablePlayTo':enable_play_to,
			'EnableDebugLog':enable_debug_log,
			'BlastAliveMessages':blast_alive_messages,
			'ClientDiscoveryIntervalSeconds':client_discovery_interval_seconds,
			'AliveMessageIntervalSeconds':alive_message_interval_seconds,
			'DefaultUserId':default_user_id
		}
		data = json.dumps(data)
		debug(data = data)
		url = self.url + "/emby/System/Configuration/dlna"
		debug(url = url)
		if not self.session:
			self.session = self.get_config()
		a = self.session.post(url, data = data, headers = self.headers)
		debug(a_url = a.url)
		content = a.content
		debug(content = content)

	@classmethod
	def pack_library(self, library):
		list_name = []
		all_list_name = []
		all_list_itemid = []

		for i in library:
			if i.get('LibraryOptions').get('Name'):
				list_name.append(
						{
							'name': i.get('LibraryOptions').get('Name'),
							'itemid': i.get('ItemId'),
							'path': i.get('LibraryOptions').get('PathInfos')
						})
				all_list_name.append(i.get('LibraryOptions').get('Name').lower())
				all_list_itemid.append(i.get('ItemId'))
			else:
				list_name.append(
						{
							'name': i.get('Name'),
							'itemid': i.get('ItemId'),
							'path': i.get('Locations')
						})
				all_list_name.append(i.get('Name').lower())
				all_list_itemid.append(i.get('ItemId'))

		return list_name, all_list_name, all_list_itemid

	@classmethod
	def refresh_library(self, itemid=None, name = None, replace_all_image=False, replace_all_metadata=False):
		headers = {'Content-Type': 'application/json'}
		debug(self_url = self.url)
		#http://127.0.0.1:8096/emby/Items/17753/Refresh?Recursive=true&ImageRefreshMode=Default&MetadataRefreshMode=Default&ReplaceAllImages=false&ReplaceAllMetadata=false&X-Emby-Client=Emby
		url = self.url + "/emby/Items/{0}/Refresh"
		params = {
			'Recursive':'true',
			'ImageRefreshMode':'Default',
			'MetadataRefreshMode':'Default',
			'ReplaceAllImages':str(replace_all_image).lower(),
			'ReplaceAllMetadata':str(replace_all_metadata).lower(),
			'X-Emby-Client':'Emby'
		}
		debug(params = params)
		library = self.get_library()
		debug(library = library)

		n = 1
		list_name, all_list_name, all_list_itemid = self.pack_library(library)
		debug(list_name = list_name)
		if name and name.lower() in all_list_name and not itemid:
			itemid = all_list_itemid[all_list_name.index(name.lower())]
			debug(itemid = itemid)
		else:
			if not itemid or not itemid in all_list_itemid:
				for i in list_name:
					print(str(n) + ". " + make_colors(i.get('name'), 'lw', 'lr') + " " + make_colors('in', 'ly') + " [" + make_colors(i.get('itemid'), 'lw', 'bl') + "]")
					n+=1
				qr = raw_input(make_colors("Select number of library to refresh it:", 'lw' ,'lr') + " ")
				if qr and int(qr) <= len(list_name):
					itemid = list_name[int(qr) - 1].get('itemid')
				debug(itemid = itemid)
				if not itemid:
					print(make_colors("Invald itemid !", 'lw', 'lr', ['blink']))
					return False
		url = url.format(itemid)
		debug(url = url)
		debug(name = name)
		debug(itemid = itemid)
		if not self.session:
			self.session = self.get_config()
		print(make_colors(name, 'lw', 'bl') + " [" + make_colors(itemid, 'lg') + "] " + make_colors(' is refresing in schedule ...', 'lc'))
		a = self.session.post(url, json = params, headers = headers)
		debug(a_url = a.url)
		content = a.content
		debug(content = content)
		code = a.status_code
		debug(code = code)
		return code

	@classmethod
	def print_paths(self, name=None, itemid=None, list_name = []):
		debug(itemid = itemid)
		#all_list_name = []
		#all_list_itemid = []
		library = self.get_library()
		#if not list_name:
			#for i in library:
				#list_name.append(
					#{
						#'name': i.get('LibraryOptions').get('Name'),
						#'itemid': i.get('ItemId'),
						#'path': i.get('LibraryOptions').get('PathInfos')
					#})
				#all_list_name.append(i.get('LibraryOptions').get('Name').lower())
				#all_list_itemid.append(i.get('ItemId'))
		list_name, all_list_name, all_list_itemid = self.pack_library(library)
		if not name and not itemid:
			n = 1
			for i in list_name:
				#debug(i = i)
				np = 1
				print(make_colors(str(n) + ".", 'lc') + " " + make_colors(str(i.get('name')), 'b', 'ly'))
				print(" " * 5 + make_colors("Id", 'lw', 'bl') + ":    " + make_colors(i.get('itemid'), 'lg'))
				list_path = []
				for p in i.get('path'):
					try:
						list_path.append(p.get('Path'))
					except:
						list_path = i.get('path')
						break
				print(" " * 5 + make_colors("Paths", 'lw', 'bl') + ": (" + str(np) + ")." + " " + make_colors(list_path[0], 'lm'))
				np = 2
				if len(list_path) > 1:
					for p in list_path[1:]:
						print(" " * 12 + "(" + str(np) + ")." + " " + make_colors(p, 'lm'))
						np+=1
				n+=1
		else:
			debug(name = name)
			debug(all_list_name = all_list_name)
			list_name_return = []
			if name and name.lower() in all_list_name:
				for i in list_name:
					if name.lower() in i.get('name').lower():
						list_name_return.append(i)
						break
			elif itemid and itemid in all_list_itemid:
				for i in list_name:
					if i.get('itemid') == itemid:
						list_name_return.append(i)
						break
			else:
				return self.print_paths()
			debug(list_name_return = list_name_return)
			if list_name_return:
				return self.print_paths(list_name = list_name_return)
		return list_name

	@classmethod
	def get_library(self):
		if not self.session:
			self.session = self.get_config()
		url = self.url + "/emby/Library/VirtualFolders"
		try:
			content = self.session.get(url)
			debug(self_session_headers = self.session.headers)
			debug(content = content.content)
			debug(content_status_code = content.status_code)
			if content.status_code == 200 and not 'invalid' in content.content.decode('utf-8') or not 'expired' in content.content.decode('utf-8'):
				content = content.json()
			else:
				print(make_colors(content.content.decode('utf-8'), 'lw', 'r'))
				os.kill(os.getpid(), signal.SIGTERM)
		except:
			if os.getenv('TRACEBACK') == '1':
				print(make_colors(traceback.format_exc(), 'lw', 'bl'))
			#print(make_colors("Invalid API or Error connection !", 'lw', 'lr', ['blink']))
			print("\n")
			sys.exit(make_colors("Invalid API or Error connection ! [1]", 'lw', 'lr', ['blink']))
		debug(content = content)
		return content

	@classmethod
	def get_items(self, limit=10000000, fields="PrimaryImageAspectRatio,BasicSyncInfo,ProductionYear,Status,EndDate,CanDelete", image_type_limit=1, enable_image_types="Primary,Backdrop,Thumb", parent_id="3b10751f11093c6a4fe61529d4bea115", latest = True, sortby = "DateCreated,SortName", sortorder="Descending", includeitemtypes="Series", recursive=True, startindex=0):
		if not self.session:
			self.session = self.get_config()

		if latest:
			url = "/emby/Items/Latest"
		else:
			url = "/emby/Items"
		debug(url = url, debug = True)

		params = {
			'Limit':limit,
			'Fields': fields,
			'ImageTypeLimit': image_type_limit,
			'EnableImageTypes': enable_image_types,
			'ParentId': parent_id,
			'X-Emby-Client': "Emby"
		}
		if not latest:
			params.update({
				"SortBy": sortby,
				"SortOrder":sortorder,
				"IncludeItemType": includeitemtypes,
				"Recursive": str(recursive).lower(),
				"StartIndex": startindex,
			})
			if not limit or limit == 0:
				params.pop("Limit")
		debug(params=params)
		content = self.get(url, params)
		debug(content = content)
		# pprint(content)
		return content

	@classmethod
	def get_user_id(self):
		if not self.session:
			self.session = self.get_config()
		params = {'X-Emby-Client':'Emby'}
		debug(params=params)
		url = self.url + "/Users"
		try:
			response = self.session.get(url, params = params)
			debug(content = response.content)
			print(response.content)
			content = response.json()
		except:
			print("\n")
			print(make_colors("ERRORS:", 'lw', 'lr', ['blink']))
			print(make_colors(traceback.format_exc(), 'lw','bl'))
			return False

		debug(content = content)
		# pprint(content)
		if isinstance(content, list):
			for i in content:
				if i.get('Name') == self.config.get_config('user', 'name'):
					self.user = i.get('Id')
					break
		return self.user

	@classmethod
	def get(self, url = "/emby/Users", params = {}):
		if not self.session:
			self.session = self.get_config()

		if not self.user:
			self.user = self.get_user_id()
		if self.user and url == "/emby/Users":
			url = url + "/" + self.user
		else:
			if self.user:
				url = re.sub("/emby/", "", url)
				url = "/emby/Users/" + self.user + "/" + url
				url = re.sub("//", "/", url)
		
		if not self.host + ":" + str(self.port) in url:
			url = self.url + url

		debug(url = url, debug = True)
		params.update({'X-Emby-Client':'Emby'})
		debug(params=params, debug = True)
		# pause()
		try:
			response = self.session.get(url, params = params)
			debug(response_url = response.url, debug = True)
			debug(content = response.content)
			print(response.content)
			content = response.json()
		except:
			print("\n")
			print(make_colors("ERRORS:", 'lw', 'lr', ['blink']))
			print(make_colors(traceback.format_exc(), 'lw','bl'))
			return False

		debug(content = content)
		# pprint(content)
		debug(url = url, debug = True)
		return content

	@classmethod
	def delete_library(self, path, name=None, itemid=None):
		if not name and not itemid:
			library = self.get_library()
			list_name = []
			#all_list_name = []
			#all_list_itemid = []
			#n = 1
			#for i in library:
				#list_name.append(
					#{
						#'name': i.get('LibraryOptions').get('Name'),
						#'itemid': i.get('ItemId'),
						#'path': i.get('LibraryOptions').get('PathInfos')
					#})
				#all_list_name.append(i.get('LibraryOptions').get('Name'))
				#all_list_itemid.append(i.get('ItemId'))
			list_name, all_list_name, all_list_itemid = self.pack_library(library)
			debug(list_name = list_name)
			path_is_exists = True
			list_path_exists = []
			for i in list_name:
				for x in i.get('path'):
					debug(x_get_Path = x.get('Path'))
					debug(path = path)
					if x.get('Path') == path:
						path_is_exists = True
						list_path_exists.append([i, i.get('path').index(x)])
			debug(list_path_exists = list_path_exists)
			if not path_is_exists:
				print(make_colors("Path Not Exists on Library !:", 'lw', 'lr', ['blink']))
				return False

			if len(list_path_exists) > 1:
				ns = 1
				for i in list_path_exists:
					print(str(ns) + ". " + make_colors(i[0].get('Name'), 'lw', 'lr') + " " + make_colors('in', 'ly') + " " + make_colors(i[0].get('path')[i[1]], 'lw', 'bl'))
					ns+=1
				qr = raw_input(make_colors("Select number of library delete to:", 'lw' ,'lr') + " ")
				if qr and int(qr) <= len(list_path_exists):
					itemid = list_path_exists[int(qr) - 1][0].get('itemid')
					name = list_path_exists[int(qr) - 1][0].get('name')
			else:
				itemid = list_path_exists[0][0].get('itemid')
				name = list_path_exists[0][0].get('name')
		debug(name = name)
		debug(itemid = itemid)
		headers = {'Content-Type': 'application/json'}
		url = self.url + "/emby/Library/VirtualFolders/Paths"
		params = {
			'refreshLibrary':'true',
			'path':path,
			'name':name,
			'Id':itemid
		}
		debug(params = params)
		if not self.session:
			self.session = self.get_config()
		a = self.session.delete(url, params = params, headers = headers)
		debug(a_url = a.url)
		content = a.content
		debug(content = content)
		return a.status_code

	@classmethod
	def create_library(self, name, dtype, path = []):
		headers = {'Content-Type': 'application/json'}
		# url = self.url + "/emby/Library/AddVirtualFolder?collectionType={}&refreshLibrary=true&name={}&X-Emby-Client=Emby Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=a4b67032-4dc0-4080-aaea-e4f0bbd74c93&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=80e519ca490243ef8e88d1ca5f711988".format(dtype, name)
		# url = self.url + "/emby/Library/VirtualFolder?collectionType={}&refreshLibrary=true&name={}&X-Emby-Client=Emby Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=a4b67032-4dc0-4080-aaea-e4f0bbd74c93&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=80e519ca490243ef8e88d1ca5f711988".format(dtype, name)
		#http://127.0.0.1:8096/emby/Library/VirtualFolders?collectionType=games&refreshLibrary=true&name=Games&X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=a4b67032-4dc0-4080-aaea-e4f0bbd74c93&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=80e519ca490243ef8e88d1ca5f711988
		#http://127.0.0.1:8096/emby/Library/VirtualFolders?collectionType=games&refreshLibrary=true&name=Games&X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=a4b67032-4dc0-4080-aaea-e4f0bbd74c93&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=80e519ca490243ef8e88d1ca5f711988
		url = self.url + "/emby/Library/VirtualFolders?collectionType={}&refreshLibrary=true&name={}&X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=a4b67032-4dc0-4080-aaea-e4f0bbd74c93&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=80e519ca490243ef8e88d1ca5f711988".format(dtype, name)
		#url = self.url + "/emby/Library/VirtualFolder?collectionType={}&refreshLibrary=true&name={}".format(dtype, name)
		debug(url = url, debug = True)
		PathInfos = []
		if path:
			for i in path:
				add = {}
				add = {"Path": i}
				PathInfos.append(add)

		data = {
			"LibraryOptions":{
				"EnableArchiveMediaFiles":"false",
				"EnablePhotos":"true",
				"EnableRealtimeMonitor":"true",
				"ExtractChapterImagesDuringLibraryScan":"false",
				"EnableChapterImageExtraction":"false",
				"SaveLocalThumbnailSets":"false",
				"ThumbnailImagesIntervalSeconds":"10",
				"DownloadImagesInAdvance":"false",
				"EnableInternetProviders":"true",
				"ImportMissingEpisodes":"false",
				"SaveLocalMetadata":"false",
				"EnableAutomaticSeriesGrouping":"true",
				"PreferredMetadataLanguage":"",
				"PreferredImageLanguage":"",
				"MetadataCountryCode":"",
				"SeasonZeroDisplayName":"Specials",
				"AutomaticRefreshIntervalDays":"30",
				"EnableEmbeddedTitles":"false",
				"SkipSubtitlesIfEmbeddedSubtitlesPresent":"false",
				"SkipSubtitlesIfAudioTrackMatches":"false",
				"SaveSubtitlesWithMedia":"true",
				"RequirePerfectSubtitleMatch":"false",
				"EnableAudioResume":"false",
				"MinResumePct":"5",
				"MaxResumePct":"90",
				"MinResumeDurationSeconds":"180",
				"MusicFolderStructure":"null",
				"MetadataSavers":["Nfo"],
				"TypeOptions":
					[{
						"Type":"Movie",
						"MetadataFetchers":[
							"TheMovieDb",
							"The Open Movie Database",
							"Douban"
						],
						"MetadataFetcherOrder":[
							"TheMovieDb",
							"The Open Movie Database",
							"Douban"
						],
						"ImageFetchers":[
							"TheMovieDb",
							"FanArt",
							"Douban",
							"The Open Movie Database",
							"Screen Grabber"
						],
						"ImageFetcherOrder":[
							"TheMovieDb",
							"FanArt",
							"Douban",
							"The Open Movie Database",
							"Screen Grabber"
						]
					}],
				"LocalMetadataReaderOrder":[
					"Nfo",
					"Emby Xml"
				],
				"SubtitleDownloadLanguages":["id"],
				"DisabledSubtitleFetchers":[],
				"SubtitleFetcherOrder":[
					"Open Subtitles","Addic7ed","NapiSub","SubDB","Podnapisi"],
				"PathInfos":PathInfos,
				"ContentType":"movies"
			}
		}

		if not self.session:
			self.session = self.get_config()

		try:
			# content = self.session.post(url, data = data).json()
			pprint(data)
			debug(url = url)
			content = requests.post(url, data = data, headers = headers).content
		except:
			#print(make_colors("Invalid API or Error connection !", 'lw', 'lr', ['blink']))
			print("\n")
			sys.exit(make_colors("Invalid API or Error connection ! [2]", 'lw', 'lr', ['blink']))
		debug(content = content)
		return content

	@classmethod
	def add_library(self, path, name = None, itemid = None):
		headers = {'Content-Type': 'application/json'}
		url = self.url + "/emby/Library/VirtualFolders/Paths?refreshLibrary=true"
		library = self.get_library()
		#list_name = []
		#all_list_name = []
		#all_list_itemid = []
		n = 1
		#for i in library:
			#list_name.append(
				#{
					#'name': i.get('LibraryOptions').get('Name').lower(),
					#'itemid': i.get('ItemId'),
					#'path': i.get('LibraryOptions').get('PathInfos')
				#})
			#all_list_name.append(i.get('LibraryOptions').get('Name'))
			#all_list_itemid.append(i.get('ItemId'))
		list_name, all_list_name, all_list_itemid = self.pack_library(library)
		if not name and not itemid:
			for i in list_name:
				print(make_colors(str(n) + ".", 'lc') + " " + make_colors(str(i.get('name')), 'lw', 'bl') + "[" + make_colors(str(i.get('itemid')), 'lg') + "]")
				n+=1
			number_selected = raw_input(make_colors("Select number of name of library add to: ", 'lw' ,'bl'))
			if number_selected:
				itemid = list_name[int(number_selected) - 1].get('itemid')
				name = list_name[int(number_selected) - 1].get('name')
		elif name and not itemid:
			for i in list_name:
				if i.get('name') == name.lower():
					itemid = i.get('itemid')
					break
		elif itemid and not name:
			for i in list_name:
				if i.get('itemid') == itemid:
					name = i.get('name')
					break
		if not name in all_list_name and not itemid in all_list_itemid:
			print(make_colors("Add library error !", 'lw', 'lr'))
			return False, False
		debug(name = name, debug=True)
		debug(itemid = itemid)
		data_post = {
			"Name":name,
			"PathInfo":{"Path":path},
			"Id":str(itemid),
		}

		data_post = json.dumps(data_post)
		#params = {'path':path}
		#params1 = {'api_key':self.api}
		debug(data_post = data_post)

		path_exists = False
		for i in list_name:
			for x in i.get('path'):
				if x.get('Path') == path:
					print(make_colors("Path has been add on Library:", 'lw', 'lr') + " " + make_colors(i.get('name'), 'b', 'ly') + " [" + make_colors(i.get('itemid'), 'lg') + "]")
					path_exists = True
					break
			if path_exists:
				break
		if path_exists:
			qp = raw_input(make_colors("Do you still want to add \"{0}\" to \"{1}\" library [y/enter]: ".format(make_colors(path, 'lr', 'ly'), make_colors(name, 'lc')), 'lw', 'lr'))
			if not qp == 'y':
				return False, False
		debug(url = url)
		if not self.session:
			self.session = self.get_config()
		a = self.session.post(url, data = data_post, headers = headers)
		debug(a_content = a.content)
		debug(a_url = a.url)
		return_code = a.status_code
		debug(return_code = return_code)
		self.refresh_library(itemid, name)
		self.print_paths()
		return name, itemid

	@classmethod
	def example_url(self):
		#url get folder
		url1 = "http://127.0.0.1:8096/emby/Users/01934680e84a418da88fd48736965014/Items?SortBy=IsFolder,SortName&SortOrder=Ascending&Recursive=false&Fields=BasicSyncInfo,CanDelete,PrimaryImageAspectRatio&ImageTypeLimit=1&EnableImageTypes=Primary,Backdrop,Thumb&StartIndex=0&Limit=50&ParentId=3b10751f11093c6a4fe61529d4bea115&X-Emby-Client=Emby"
		#refresh item
		url2 = "http://127.0.0.1:8096/emby/Items/17753/Refresh?Recursive=true&ImageRefreshMode=Default&MetadataRefreshMode=Default&ReplaceAllImages=false&ReplaceAllMetadata=false&X-Emby-Client=Emby"
		#get item on folder
		url3 = "http://127.0.0.1:8096/emby/Users/01934680e84a418da88fd48736965014/Items?SortBy=DateCreated,SortName&SortOrder=Descending&Fields=BasicSyncInfo,CanDelete,PrimaryImageAspectRatio,ProductionYear,Status,EndDate&ImageTypeLimit=1&EnableImageTypes=Primary,Backdrop,Thumb&StartIndex=0&Limit=50&ParentId=17753&X-Emby-Client=Emby"
		#refresh item on folder
		url4 = "http://127.0.0.1:8096/emby/Items/231627/Refresh?Recursive=true&ImageRefreshMode=Default&MetadataRefreshMode=Default&ReplaceAllImages=false&ReplaceAllMetadata=false&X-Emby-Client=Emby"
		#get season list
		url5 = "http://127.0.0.1:8096/emby/Shows/231627/Seasons?UserId=01934680e84a418da88fd48736965014&Fields=PrimaryImageAspectRatio%2CBasicSyncInfo%2CCanDelete%2CProductionYear&EnableTotalRecordCount=false&X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=69df499a-715a-477d-b244-664c59d9846b&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=d169a855d1df4eafa5a5f035b781c75f"
		url6 = "http://127.0.0.1:8096/emby/Users/01934680e84a418da88fd48736965014/Items/231629?X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=69df499a-715a-477d-b244-664c59d9846b&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=d169a855d1df4eafa5a5f035b781c75f"
		#get list of season
		url7 = "http://127.0.0.1:8096/emby/Shows/231627/Episodes?SeasonId=231629&ImageTypeLimit=1&UserId=01934680e84a418da88fd48736965014&Fields=Overview%2CPrimaryImageAspectRatio&X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=69df499a-715a-477d-b244-664c59d9846b&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=d169a855d1df4eafa5a5f035b781c75f"
		#get list of season on front
		url8 = "http://127.0.0.1:8096/emby/Shows/NextUp?SeriesId=231627&Fields=PrimaryImageAspectRatio%2CCanDelete&ImageTypeLimit=1&EnableTotalRecordCount=false&Limit=12&UserId=01934680e84a418da88fd48736965014&X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=69df499a-715a-477d-b244-664c59d9846b&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=d169a855d1df4eafa5a5f035b781c75f"
		#set un-played (DELETE)
		url9 = "http://127.0.0.1:8096/emby/Users/01934680e84a418da88fd48736965014/PlayedItems/232962?X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=69df499a-715a-477d-b244-664c59d9846b&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=d169a855d1df4eafa5a5f035b781c75f"
		#set played (POST)
		url10 = "http://127.0.0.1:8096/emby/Users/01934680e84a418da88fd48736965014/PlayedItems/232962?X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=69df499a-715a-477d-b244-664c59d9846b&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=d169a855d1df4eafa5a5f035b781c75f"
		#delete info
		url11 = "http://127.0.0.1:8096/emby/Items/232962/DeleteInfo?X-Emby-Client=Emby%20Web&X-Emby-Device-Name=Chrome&X-Emby-Device-Id=69df499a-715a-477d-b244-664c59d9846b&X-Emby-Client-Version=4.5.4.0&X-Emby-Token=d169a855d1df4eafa5a5f035b781c75f"

	@classmethod
	def print_nav(self, t = None):
		if t == 1:
			pass
		else:
			note = make_colors("select number:", "lw", 'bl') + " "
		q = raw_input(note)
		if q:
			q = str(q).strip()
			if q == 'x' or q == 'exit' or q == 'q' or q == 'quit':
				sys.exit(make_colors("system exit ... !", 'b', 'y'))
		return q

    @classmethod
	def get_devices(self):	
		devices_url = f"{self.url}/emby/Sessions"
		params = {
			'api_key': self.api
		}
		
		response = self.session.get(devices_url, params=params)
		data = response.json()
		debug(data=data)

		if list(filter(lambda k: 'debug' in k.lower(), os.environ)): jprint(data)
		
		DEVICE_ID_DATA = []
		#DEVICE_ID = ''
		#DEVICE_NAME_SELECTED = ''
		
		# Display device IDs
		for session in data:
			device_id = session.get('DeviceId')
			device_name = session.get('DeviceName')
			if device_id and device_name:
				print(f"Device Name: {device_name}, Device ID: {device_id}")
				DEVICE_ID_DATA.append([device_id, device_name])
		
		if len(DEVICE_ID_DATA) > 1:
			n = 1
			for d in DEVICE_ID_DATA:
				print(
					make_colors(str(n).zfill(2), 'lc') + ". " +
					make_colors(d[1], 'b', 'y') + " " +
					make_colors(d[0], 'lw', 'bl')
				)
				n += 1
		
			q = input(make_colors("Select Device:", 'lw', 'r') + " ")
			if q and q.isdigit() and int(q) <= len(DEVICE_ID_DATA):
				#DEVICE_ID = DEVICE_ID_DATA[int(q) - 1][0]
				#DEVICE_NAME_SELECTED = DEVICE_ID_DATA[int(q) - 1][1]
				self.device_id = DEVICE_ID_DATA[int(q) - 1][0]
				self.device_name = DEVICE_ID_DATA[int(q) - 1][1]
				return DEVICE_ID_DATA[int(q) - 1]
		else:
			#DEVICE_ID = DEVICE_ID_DATA[0][0]
			#DEVICE_NAME_SELECTED = DEVICE_ID_DATA[0][1]
			self.device_id = DEVICE_ID_DATA[0][0]
			self.device_name = DEVICE_ID_DATA[0][1]
			return DEVICE_ID_DATA[0]
		
		return []
		
	def search (self, text):
		
		user_id = self.user_id or self.get_user()
		device_id = self.device_id or self.get_devices()
		
		debug(device_id = device_id)
		debug(self_device_name = self.device_name)

		url = f"{self.url}/emby/Users/{user_id}/Items"
		
		debug(search_url = url)
		
		params = {
			'Fields': 'BasicSyncInfo,CanDelete,PrimaryImageAspectRatio,ProductionYear,Status,EndDate',
			'StartIndex': '0',
			'SortBy': 'SortName',
			'SortOrder': 'Ascending',
			'EnableImageTypes': 'Primary,Backdrop,Thumb',
			'ImageTypeLimit': '1',
			'Recursive': 'true',
			'SearchTerm': text,
			'GroupProgramsBySeries': 'true',
			'Limit': '50',
			'X-Emby-Client': 'Emby Web',
			'X-Emby-Device-Name': device_id[1],
			'X-Emby-Device-Id': device_id[0],
			'X-Emby-Client-Version': '4.8.8.0',
			'X-Emby-Token': self.api,
			'X-Emby-Language': 'en-us'
		}
		
		debug(params = params)
		
		response = self.session.get(url, params=params)
		data = response.json()
		debug(data=data)
		if list(filter(lambda k: 'debug' in k.lower(), os.environ)): jprint(data)
		
		result_albums = []
		result_artists = []
		result_tracks = []
		
		result_albums_sort = []
		result_artists_sort = []
		result_tracks_sort = []
		
		for item in data['Items']:
			if item['Type'] == 'MusicAlbum':
				artist_name = item['AlbumArtist']
				album_name = item['Name']
				result_albums_sort.append([artist_name, album_name, item['Id']])
				result_albums.append(item)
			
			elif item['Type'] == 'MusicArtist':
				artist_name = item['Name']
				result_artists_sort.append([artist_name, item['Id']])
				result_artists.append(item)
			
			elif item['Type'] == 'Audio':
				artist_name = item['AlbumArtist']
				album_name = item['Album']
				song_name = item['Name']
				result_tracks_sort.append([artist_name, album_name, song_name, item['Id']])
				result_tracks.append(item)
			
		
		# Display results
		n = 1
		if result_albums_sort:
			print(make_colors("ALBUMS:", 'b', 'y'))
			for album in result_albums_sort:
				print(
					make_colors(str(n).zfill(2), 'lc') + ". " + \
					make_colors(album[0], 'ly') + " - " + \
					make_colors(album[1], 'lw', 'm')
				)
				n += 1
		
		if result_artists_sort:
			print(make_colors("ARTISTS:", 'b', 'lg'))
			for artist in result_artists_sort:
				print(
					make_colors(str(n).zfill(2), 'lm') + ". " + \
					make_colors(artist[0], 'lc')
				)
				n += 1
		
		if result_tracks_sort:
			print(make_colors("TRACKS:", 'b', 'ly'))
			for track in result_tracks_sort:
				print(
						make_colors(str(n).zfill(2), 'lc') + ". " + \
						make_colors(track[2], 'lg') + " - " + \
						make_colors(track[0], 'ly') + " - " + \
						make_colors(track[1], 'lb')
					)
				n += 1
		
		note = make_colors("for 'album' after selected then show list of tracks/songs or you can select n1,n2,n3,nx or n1-nx or n1.n2.n3.nx to direct play album", 'lc') + ", " + \
			make_colors("for 'artist' after selected then show list of albums", 'lg') + ", " + \
			make_colors("for 'track' can select with n1,n2,n3,nx or n1-nx or n1.n2.n3.nx", 'y') + ", "
		print("\n" + note)
		q = input(make_colors('Select number:', 'lw', 'r') + " ")
		
		
		

	@classmethod
	def format_number(self, number, length = 10):
		number = str(number).strip()
		if not str(number).isdigit():
			return number
		zeros = len(str(length)) - len(number)
		r = ("0" * zeros) + str(number)
		if len(r) == 1:
			return "0" + r
		return r

	@classmethod
	def navigator(self, parent_id = None, latest = True):
		if parent_id:
			data = self.get_items(parent_id = parent_id, latest = latest)
		else:
			data = self.get("/emby/Items")

		# pprint(data)
		n = 1
		for i in data['Items']:
			print(
				make_colors(self.format_number(n, data['TotalRecordCount']) + ".", 'lc') + " " +\
				make_colors(i.get("Name"), 'b', 'ly')
			)
			n+=1
		q = self.print_nav()
		if q:
			id = data['Items'][int(q) - 1].get('Id')
			debug(id = id)
			if id:
				return self.navigator(id, False)



	@classmethod
	def usage(self):
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('-H', '--host', help = 'Host/Ip emby server', action = 'store')
		parser.add_argument('-P', '--port', help = 'Port emby server, default: 8096', action = 'store', default = 8096)
		parser.add_argument('--api', help = 'Api key', action = 'store')
		parser.add_argument('-c', '--create', help='Create Library then Add path to library with type library defined', action='store')
		parser.add_argument('-t', '--type', help='Type of create Library', action='store')
		parser.add_argument('-p', '--path', help='Path of create Library can be multiply same as "-a" or "--add"', action='store', nargs="*")
		parser.add_argument('-a', '--add', help='Add path to library can be multiply same as "-p" or "--path"', action='store', nargs="*")
		parser.add_argument('-n', '--name', help='Name of library add to', action='store')
		parser.add_argument('-i', '--itemid', help='Item id of library either name add to', action='store')
		parser.add_argument('-l', '--print-path', help='Print all of path of library',action='store_true')
		parser.add_argument('-d', '--delete', help='Delete library', action='store')
		parser.add_argument('-r', '--refresh', help='Refresh library', action='store_true')
		parser.add_argument('-x', '--write-config', help='All input option will write in config file', action='store_true')
		parser.add_argument('--dlna-on', help='Turn On DLNA Server', action='store_true')
		parser.add_argument('--dlna-off', help='Turn Off DLNA Server', action='store_true')
		if len(sys.argv) == 1:
			parser.print_help()
		else:
			args = parser.parse_args()
			if args.host:
				self.host = args.host
				#self.config.write_config('host', 'ip', self.host)
			if args.port:
				self.port = args.port
				#self.config.write_config('host', 'port', self.port)
			if args.host and args.port:
				self.session = self.get_config(args.host, args.port)
			if  args.api:
				self.api = args.api
				self.session = self.get_config(args.host, args.port, args.api)
			self.session = self.get_config(args.host, args.port, args.api, args.write_config)
			if args.add:
				for i in args.add:
					self.add_library(i, args.name, args.itemid)
			elif args.delete:
				if args.add:
					for i in args.add:
						self.delete_library(i, args.name, args.itemid)
				elif args.path:
					for i in args.path:
						self.delete_library(i, args.name, args.itemid)
			elif args.print_path:
				self.print_paths(args.name, args.itemid)
			elif args.refresh:
				self.refresh_library(args.itemid, args.name)
			elif (args.create and args.type and args.path) or (args.create and args.type and args.add):
				if args.path:
					path = args.path
				elif args.add:
					path = args.add
				self.create_library(args.create, args.type, path)

			if args.dlna_on:
				self.setting_set_dlna(True)
				pprint(self.setting_get_dlna())
			elif args.dlna_off:
				self.setting_set_dlna(False)


def usage():
	return Embycli.usage()

if __name__ == '__main__':
	c = Embycli()
	# c.navigator()
	# c.get_items(latest=False)
	# c.get("/emby/Items")
	c.usage()
	#c.get_api('192.168.43.2')
	#c.get_api('127.0.0.1')
	#pprint(c.get_library())
	#c.add_library(sys.argv[1])
	#c.delete_library(sys.argv[1])
	#c.setting_set_dlna(True)
	#c.refresh_library("661ef9ddfac11820318025aa6d38d39d")
	#c.print_paths(name="video games")
	#c.print_paths(itemid="661ef9ddfac11820318025aa6d38d39d")
