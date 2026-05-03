import json
from urllib.request import Request, urlopen

payload = json.dumps({"url": "https://example.com"}).encode("utf-8")
request = Request("http://127.0.0.1:8000/api/scan", data=payload, headers={"Content-Type": "application/json"})
with urlopen(request, timeout=10) as response:
    print(response.read().decode("utf-8"))
