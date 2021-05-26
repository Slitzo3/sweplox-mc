# Sweplox Minecraft
This repository contains our plugins and configurations on each server for our Minecraft community on Sweplox.

Help is always welcomed.

# Setup for new server
1. Fork this repository
2. Create a new folder named what the server or theme is called
3. Create a `README.md` file in that directory
4. Use this format on the `README.md` file:
```md
# Sweplox Minecraft - {folder_name}

## Description
{Explain what this server/minigame/game is about}

{Optional underneath here now}
## Plugins
{A list of of all plugins needed}
```
5. Push and wait for approval and merged

# What should these folders contain?
These folders should contain plugins and configurations on each server.

# What do I do with sensitive information?
If you got information like passwords or IP's that shall not get exposed, read this.

Remove the sensitive part and insert `{{ }}` instead, and instead of the `{{ }}` give it a name.
This will be used later to automatically insert the sensitive data from our private machines.

How it works:
1. The program looks through every file.
2. If it finds `{{ }}` it will check what kind of name it contains.
3. If the name matches something in our config it will remove the `{{ }}` and the name and replace it from our config.

If the name doesn't match any of the configs it will return a error telling us what is missing and we have to add it manually,
thus to keep things straight here is basic stuff:
```txt
Database IP: {{ database_ip }}
Database Port: {{ database_port }}
Database Password: {{ database_password }}
Database User: {{ database_username }}
...
```

Example:
```yml
data:
  address: {{ database_ip }}
  database: minecraft
  username: {{ database_username }}
  password: '{{ database_password }}'
  port: {{ database_port }}
```