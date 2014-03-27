import roblox

group = roblox.group(id=372)

print group.get_rolesets()
print group.get_name()
print group.get_description()
print group.get_owner()

user = roblox.user(username="Kenetec")

print user.get_group_rank(group)

print user.in_group(372)

print user.get_blurb()

print user.get_group_rank(372)
print user.get_group_role(372)

print user.get_avatar()