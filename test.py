
from google import genai

client = genai.Client(api_key="AIzaSyBrvpAyi2Bgh2Cig-i5QF3PSFob2IjPnqI")

for m in client.models.list():
    print(m.name)
