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

class Embycli(object):
	def __init__(self, api = None, host = None, port = None):
		self.configname = os.path.join(os.path.dirname(__file__), 'embycli.ini')
		self.config = configset(self.configname)
		self.api = api
		self.default_api = self.config.get_config('auth', 'api')		
		self.host = host
		self.port = port
		self.url = None
		self.headers = {'Content-Type': 'application/json'}
		self.session = None
		
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
		if api and host and port:
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
				if not 'invalid' in content or not 'expired' in content:
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
					if not 'invalid' in content or not 'expired' in content:
						content = json.loads(content)
						for it in content.get('Items'):
							list_api.append(it.get('AccessToken'))
					debug(list_api = list_api)
					if list_api:
						break				
			return list_api
		return []
		
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
		if not self.api:
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
		
	def setting_get_users(self):
		if not self.session:
			self.session = self.get_config()
		url = self.url + "/emby/users"
		return self.session.get(url, headers = self.headers).json()
		
	def setting_get_dlna(self):
		if not self.session:
			self.session = self.get_config()		
		url = self.url + "/emby/System/Configuration/dlna"
		return self.session.get(url, headers = self.headers).json()
		
	def format_argument(self, argument):
		arg = re.split("_", argument)
		debug(arg = arg)
		arg_1 = []
		for i in arg:
			arg_1.append(str(i).title())
		debug(arg_1 = arg_1)
		return "".join(arg_1)
		
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
		
		
	def refresh_library(self, itemid=None, name = None, replace_all_image=False, replace_all_metadata=False):
		headers = {'Content-Type': 'application/json'}
		debug(self_url = self.url)
		
		url = self.url + "/emby/Items/{0}/Refresh"
		params = {
			'Recursive':'true',
			'ImageRefreshMode':'Default',
			'MetadataRefreshMode':'Default',
			'ReplaceAllImages':str(replace_all_image).lower(),
			'ReplaceAllMetadata':str(replace_all_metadata).lower()
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
			
	def get_library(self):
		if not self.session:
			self.session = self.get_config()		
		url = self.url + "/emby/Library/VirtualFolders"
		try:
			content = self.session.get(url).json()
		except:
			#print(make_colors("Invalid API or Error connection !", 'lw', 'lr', ['blink']))
			print("\n")
			sys.exit(make_colors("Invalid API or Error connection !", 'lw', 'lr', ['blink']))
		debug(content = content)
		return content
		
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
		
	def usage(self):
		parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
		parser.add_argument('-H', '--host', help = 'Host/Ip emby server', action = 'store')
		parser.add_argument('-P', '--port', help = 'Port emby server, default: 8096', action = 'store', default = 8096)
		parser.add_argument('--api', help = 'Api key', action = 'store')
		parser.add_argument('-a', '--add', help='Add path to library', action='store')
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
				self.add_library(args.add, args.name, args.itemid)
			elif args.delete:
				self.delete_library(args.add, args.name, args.itemid)
			elif args.print_path:
				self.print_paths(args.name, args.itemid)
			elif args.refresh:
				self.refresh_library(args.itemid, args.name)
			if args.dlna_on:
				self.setting_set_dlna(True)
				pprint(self.setting_get_dlna())
			elif args.dlna_off:
				self.setting_set_dlna(False)
			
if __name__ == '__main__':
	c = Embycli()
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