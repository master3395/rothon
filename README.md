ROTHON - a Python wrapper for ROBLOX.com
========================================

ROTHON makes it easy to interact with the ROBLOX website with Python. It is currently a work in progress, and will eventually support many features such as logging in, sending PMs, and more.

Dependencies
------------
- requests
- pyquery

You can grab these with this command:
```
pip install requests pyquery
```

Current API
-----------

### Users

#### Creating a user object

By ID:
```
user = roblox.user(id=5377304)
```

By username:
```
user = roblox.user(username="Kenetec")
```

#### Methods
All of these methods should be wrapped in a `try...except` block, as there can be errors while fetching the values.

Get username:
```
print user.get_username()
```

Get ID:
```
print user.get_id()
```

> `get_id` and `get_username` will fetch the value if it has not already been stored in the user object.
> `get_id` will be called internally in the user constructor is instantiated with the username parameter

Is in group:
```
print user.in_group(372)
```

Get blurb
```
print user.get_blurb()
```

Get group rank (Number value)
```
print user.get_group_rank(372)
```

Get group role (String value/role name):
```
print user.get_group_role(372)
```

Get user avatar image link:
```
print user.get_avatar()
```