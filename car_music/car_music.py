import urllib
from smb.SMBHandler import SMBHandler
opener = urllib.request.build_opener(SMBHandler)
fh = opener.open('smb://192.168.1.1')
data = fh.read()
print(data)
fh.close()