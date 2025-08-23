import requests
import dotenv
import os
dotenv.load_dotenv()
print(os.getenv("TOKEN1"))
url = "https://proxy.webshare.io/api/v2/profile/"
url2 = "https://proxy.webshare.io/api/v2/proxy/list/?page=4&page_size=10"




response = requests.get(url2, headers={"Authorization": f"Bearer {os.getenv('TOKEN1')}"})
print(response.json())