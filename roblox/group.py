import requests
import re
import user
from pyquery import PyQuery as pq

class Group:

	def __init__(self, id):
		self.id = id

	def get_id(self):
		return self.id

	def get_name(self):
		try:
			return self.name 
		except AttributeError:

			r = requests.get("http://www.roblox.com/Groups/group.aspx?gid=%s" % self.id)

			if not r.status_code == 200:
				raise self.FetchError

			doc = pq(r.text)
			self.name = doc(".GroupPanelContainer .right-col h2").text()
			return self.name

	def get_description(self):
		try:
			return self.description
		except AttributeError:

			r = requests.get("http://www.roblox.com/Groups/group.aspx?gid=%s" % self.id)

			if not r.status_code == 200:
				raise self.FetchError

			doc = pq(r.text)
			self.description = doc("#GroupDescP pre").text()
			return self.description

	def get_owner(self):
		try:
			return self.owner
		except AttributeError:

			r = requests.get("http://www.roblox.com/Groups/group.aspx?gid=%s" % self.id)

			if not r.status_code == 200:
				raise self.FetchError

			doc = pq(r.text)
			owner_link = doc("#ctl00_cphRoblox_OwnershipPanel a").attr("href")
			owner_id = int(re.compile(r'(\d+)').search(owner_link).group(1))
			self.owner = user.User(id=owner_id)
			return self.owner

	def get_rolesets(self):
		try:
			return self.rolesets
		except AttributeError:

			r = requests.get("http://www.roblox.com/api/groups/%s/RoleSets/" % self.id)

			self.rolesets = r.json()

			return self.rolesets

	def __unicode__(self):
		try:
			return self.get_name()
		except AttributeError:
			return "group-%s" % self.id

	def __str__(self):
		return unicode(self).encode('utf-8')

	class NoGroupIdentified(Exception):
		pass

	class FetchError(Exception):
		pass

	class GroupDoesntExist(Exception):
		pass