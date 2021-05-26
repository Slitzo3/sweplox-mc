import json
import os
import re

Config: json
Errors: list = []
IgnoreDir: list = [".git"]
IgnoreFile: list = ["SAIP.py", "README.md", "config.json"]
# Get config file
c = open("config.json", "rt")
c = json.load(c)
Config = c

for subdir, dirs, files in os.walk("./"):
    for file in files:
        # Ignore dirs we don't want to modify
        if not any(ext in subdir for ext in IgnoreDir):
            # Ignore files we don't want to modify
            if not any(ext in file for ext in IgnoreFile):
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
                            if Config.get(r):
                                # Replace the value
                                list_of_lines[x] = list_of_lines[x].replace(r, Config.get(r))
                                
                                # Remove ugly brackets xd
                                list_of_lines[x] = re.sub(r"{{\s", "", list_of_lines[x])
                                list_of_lines[x] = list_of_lines[x].replace("{{", "")
                                list_of_lines[x] = re.sub(r"\s}}", "", list_of_lines[x])
                                list_of_lines[x] = list_of_lines[x].replace("}}", "")
                            else:
                                Errors.append("Unable to locate " + r + " in " + d)
                        if x+1 == len(list_of_lines):
                            print("Modifying " + d)
                            file = open(os.path.join(subdir, file), "w")
                            file.writelines(list_of_lines)

if len(Errors) > 0:
    f = open("errors.txt", "a")
    for x in Errors:
        f.write("\n" +x)
        continue
    f.close()