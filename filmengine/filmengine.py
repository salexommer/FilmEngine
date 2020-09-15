# Initial filmengine script that will be split into separate modules later
import requests
import os
import gzip

# Script variables
file_name = 'sample.xml'
url = 'https://www.w3schools.com/xml/note.xml'

# Download the required files
r = requests.get(url, allow_redirects=True)
open (os.path.join('./files/',file_name), 'wb').write(r.content)
print(file_name + " has been downloaded.")

# Decompress
gzip.decompress(os.path.join('./files/',file_name))