import requests
import urllib.request

try:
	a = requests.post("https://testsandbox-post.com/", data={"info": "success"})
except:
	print("Failed1")
	pass


try:
	with urllib.request.urlopen("http://testsandbox-url.com/") as response:
		html = response.read()
except:
	print("Failed1")
	pass
