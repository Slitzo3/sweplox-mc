import json
import os
import re

DEBUG=False

Config: json
Errors: list = []
IgnoreDir: list = [".git"]
IgnoreFile: list = ["README.md", "config.json"]
IgnoreExtension = (".jar", ".py", ".md", ".db")
# Get config file
c = open("config.json", "rt")
c = json.load(c)
Config = c

if not DEBUG:
    for subdir, dirs, files in os.walk("./"):
        for file in files:
            # Ignore dirs we don't want to modify
            if not any(ext in subdir for ext in IgnoreDir):
                # Ignore files we don't want to modify
                if not any(ext in file for ext in IgnoreFile) and not file.endswith(IgnoreExtension):
                    # Open our file
                    with open(os.path.join(subdir, file), "rt") as a_file:
                        # Get all of the lines
                        list_of_lines = a_file.readlines()
                        count = 0

                        # Loop through each line
                        for x in range(len(list_of_lines)):
                            # Search for our secret stuff
                            result = re.search("{{ (.*) }}", list_of_lines[x])
                            d = os.path.join(subdir, file)
                            # Check if not None
                            if result:
                                r = result.group(1)
                                # If we found a matching key continue here
                                # Remove ugly brackets xd
                                list_of_lines[x] = re.sub(r"{{\s", "", list_of_lines[x])
                                list_of_lines[x] = list_of_lines[x].replace("{{", "")
                                list_of_lines[x] = re.sub(r"\s}}", "", list_of_lines[x])
                                list_of_lines[x] = list_of_lines[x].replace("}}", "")
                                r = r.split("}}" or "{{")
                                for xr in range(len(r)):
                                    r[xr] = re.sub(r"{{\s|:|!", "", r[xr])
                                    r[xr] = re.sub(r"\s}}|:|!", "", r[xr])
                                    r[xr] = r[xr].strip()
                                    if Config.get(r[xr]):
                                        # Replace the value
                                        list_of_lines[x] = list_of_lines[x].replace(r[xr], Config.get(r[xr]))
                                    else:
                                        Errors.append("Unable to locate " + r[xr] + " in " + d)
                            if x+1 == len(list_of_lines):
                                print("Modifying " + d)
                                file = open(os.path.join(subdir, file), "w")
                                file.writelines(list_of_lines)
else:
    with open("test.yml", "rt") as a_file:
        # Get all of the lines
        list_of_lines = a_file.readlines()
        count = 0

        # Loop through each line
        for x in range(len(list_of_lines)):
            # Search for our secret stuff
            result = re.search("{{ (.*) }}", list_of_lines[x])
            # Check if not None
            if result:
                r = result.group(1)
                # If we found a matching key continue here
                # Remove ugly brackets xd
                list_of_lines[x] = re.sub(r"{{\s", "", list_of_lines[x])
                list_of_lines[x] = list_of_lines[x].replace("{{", "")
                list_of_lines[x] = re.sub(r"\s}}", "", list_of_lines[x])
                list_of_lines[x] = list_of_lines[x].replace("}}", "")
                r = r.split("}}" or "{{")
                for xr in range(len(r)):
                    r[xr] = re.sub(r"{{\s|:|!", "", r[xr])
                    r[xr] = re.sub(r"\s}}|:|!", "", r[xr])
                    r[xr] = r[xr].strip()
                    if Config.get(r[xr]):
                        # Replace the value
                        list_of_lines[x] = list_of_lines[x].replace(r[xr], Config.get(r[xr]))

            if x+1 == len(list_of_lines):
                file = open("test.yml", "w")
                file.writelines(list_of_lines)

if len(Errors) > 0:
    f = open("errors.txt", "a")
    for x in Errors:
        f.write("\n" +x)
        continue
    f.close()