import requests
import re
import inspect
from pyquery import PyQuery as pq
import os

pwd = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(pwd, 'group_post_data.txt'), 'r') as f:
	groups_post_data = f.read()

def need_ident(f):
	def wrapper(*args, **kwargs):
		if not hasattr(args[0], 'id'):
			raise args[0].NoUserIdentified
		return f(*args, **kwargs)
	return wrapper

class User:
	def __init__(self, **kwargs):
		if 'id' in kwargs:
			self.id = int(kwargs['id'])
		if 'username' in kwargs:
			self.username = kwargs['username']
			self.get_id()

	def get_username(self):
		try:
			return self.username
		except AttributeError:
			if not hasattr(self, 'id'):
				raise self.NoUserIdentified

			r = requests.get('http://api.roblox.com/users/%s' % self.id)

			if not r.status_code == 200:
				raise self.FetchError

			data = r.json()

			self.username = data[u'Username']

			return self.username


	def get_id(self):
		if not hasattr(self, 'username'):
			raise self.NoUserIdentified

		try:
			return self.id
		except AttributeError:

			r = requests.get('http://www.roblox.com/User.aspx?UserName=%s' % self.username)

			if not r.status_code == 200:
				raise self.FetchError
			try:
				self.id = int(re.compile(r'(\d+)').search(r.url).group(1))
				return self.id
			except AttributeError:
				raise self.UserDoesntExist

	@need_ident
	def in_group(self, group):
		if inspect.isclass(group):
			pass
		elif isinstance(group, int):
			group_id = group
		else:
			raise Exception

		r = requests.get('http://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=IsInGroup&playerid=%s&groupid=%s' % (self.id, group_id))

		if not r.status_code == 200:
			raise self.FetchError

		if 'true' in r.text:
			return True
		elif 'false' in r.text:
			return False
		else:
			raise self.FetchError	

	@need_ident
	def get_group_rank(self, group):
		if inspect.isclass(group):
			pass
		elif isinstance(group, int):
			group_id = group
		else:
			raise Exception

		r = requests.get('http://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRank&playerid=%s&groupid=%s' % (self.id, group_id))

		if not r.status_code == 200:
			raise self.FetchError

		return int(re.compile(r'(\d+)').search(r.text).group(1))

	@need_ident
	def get_group_role(self, group):
		if inspect.isclass(group):
			pass
		elif isinstance(group, int):
			group_id = group
		else:
			raise Exception

		r = requests.get('http://www.roblox.com/Game/LuaWebService/HandleSocialRequest.ashx?method=GetGroupRole&playerid=%s&groupid=%s' % (self.id, group_id))

		if not r.status_code == 200:
			raise self.FetchError

		return r.text

	@need_ident
	def get_blurb(self):
		r = requests.get('http://www.roblox.com/User.aspx?ID=%s&ForcePublicView=true' % self.id)

		if not r.status_code == 200:
			raise self.FetchError

		doc = pq(r.text)
		doc(".UserBlurb").html(doc(".UserBlurb").html().replace('<br />', '\n'))
		return doc(".UserBlurb").text()

	@need_ident
	def get_avatar(self, size=200):
		r = requests.get('http://www.roblox.com/Thumbs/Avatar.ashx?x=%s&y=%s&format=png&username=%s' % (size, size, self.get_username()))

		if not r.status_code == 200:
			raise self.FetchError

		return r.url

	# @need_ident
	# def get_groups(self):
	# 	s = requests.Session()
	# 	while True:
	# 		r = s.post('http://www.roblox.com/User.aspx?ID=%s&ForcePublicView=true' % self.id, data=groups_post_data, headers={
	# 			'content-type': 'application/x-www-form-urlencoded'
	# 		})

	# 		if not r.status_code == 200:
	# 			raise self.FetchError

	# 		doc = pq(r.text)

	# 		# print el.find('div a').attrib['href']

	# 		for el in doc("#ctl00_cphRoblox_rbxUserGroupsPane_ctl00 div").items():
	# 			print el.find('a').attr.href

	# 	return ''



	# Custom Exceptions 

	class NoUserIdentified(Exception):
		pass

	class FetchError(Exception):
		pass

	class UserDoesntExist(Exception):
		pass