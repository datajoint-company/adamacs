import json
import rspace_client as rc
import sys
import json
import os

# Ask admin to get you the local_conf file
local_dir = os.path.dirname(__file__)
with open(os.path.join(local_dir, 'rspace_local_conf.json')) as jsonFile:
    local_conf = json.load(jsonFile)

client = rc.Client(local_conf['server'], local_conf['apiKey'])

print(client.get_status())

client.get_document('SD37310')