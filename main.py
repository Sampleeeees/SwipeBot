import time
import asyncio
import httpx
import requests
import json

url = 'http://194.146.38.190/'

auth = httpx.DigestAuth('admin@admin.com', 'swipe123')

async def main():
    async with httpx.AsyncClient() as client:
        response = await client.post(url+"api/auth/login/", data={'email': 'admin@admin.com', 'password': 'swipe123'})
        print(response.status_code)
        print(response.json()['access'])

asyncio.run(main())


