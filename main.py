import roblox

user = roblox.user(username="Kenetec")

print user.get_username()

print user.in_group(372)

print user.get_blurb()

print user.get_group_rank(372)
print user.get_group_role(372)

print user.get_avatar()