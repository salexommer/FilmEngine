# Initial filmengine script that will be split into separate modules later
import requests
import os
import gzip

# Script variables
archive_name = 'enwiki-latest-abstract.xml.gz'
url = 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz'

# Download the required files
r = requests.get(url, allow_redirects=True)
open (os.path.join('./files/',archive_name), 'wb').write(r.content)

print(archive_name + " has been downloaded.")

# Decompress
input = gzip.GzipFile("./files/" + archive_name, 'rb')
s = input.read()
input.close()

output = open("./files/" + archive_name, 'wb')
output.write(s)
output.close()

print("The file has been decompressed")