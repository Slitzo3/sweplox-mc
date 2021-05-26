import json
import os
import bs4 as bs
import re

Config: json

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
                    for line in list_of_lines:
                        
                        # Search for our secret stuff
                        result = re.search("{{ (.*) }}", list_of_lines[count])

                        # Check if not None
                        if result:
                            # Go through each key etc
                            for key, value in Config.items():
                                # If we found a matching key continue here
                                if result.group(1) == key:
                                    # Replace the value
                                    list_of_lines[count] = list_of_lines[count].replace(result.group(1), Config[result.group(1)])

                                    # Remove ugly brackets xd
                                    list_of_lines[count] = list_of_lines[count].replace("{{ ", "")
                                    list_of_lines[count] = list_of_lines[count].replace("{{", "")
                                    list_of_lines[count] = list_of_lines[count].replace(" }}", "")
                                    list_of_lines[count] = list_of_lines[count].replace("}}", "")
                                else:
                                    continue
                                    # Error something here please.
                                    # @Tolfx
                            #print(result.group(1))
                            
                        count = count+1
                    
                    if count == len(list_of_lines):
                        file = open(os.path.join(subdir, file), "w")
                        file.writelines(list_of_lines)