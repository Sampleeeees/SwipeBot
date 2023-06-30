import asyncio
import json
import httpx
from yarl import URL
from database.database import get_refresh_token, get_token, set_tokens, logout, update_token, is_authenticated


class APIClient:
    def __init__(self, user):
        self.user = user
        self.url = URL('http://194.146.38.190/')

    async def send_refresh_token(self):
        async with httpx.AsyncClient() as client:
            response = await client.post(url=str(self.url.with_path('api/token/refresh')),
                                         data={'refresh': get_refresh_token(self.user)})
            if response.status_code == 200:
                response_data = response.json()
                update_token(response_data['access'], self.user)
                return response
            else:
                logout(self.user)
                return response

    async def send_request(self, request):
        async with httpx.AsyncClient() as client:
            response = await client.send(request=request)
            if response.status_code == 401:
                response = await self.send_refresh_token()
                response_data = response.json()
                if 'access' in response_data:
                    request.headers['Authorization'] = 'Bearer ' + response_data['access']
                    response = await client.send(request)
        return response


class Test(APIClient):

    def test(self):
        return self.send_refresh_token()


class UserAPIClient(APIClient):

    def headers(self) -> dict:
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + get_token(self.user)
        }
        return headers

    async def register_user(self, user_data: dict) -> bool:
        data = {
            'email': user_data.get('user_data'),
            'password1': user_data.get('password1'),
            'password2': user_data.get('password2'),
            'name': user_data.get('name'),
            'surname': user_data.get('username')
        }
        async with httpx.AsyncClient() as client:
            request = await client.post(url=str(self.url.with_path('api/registration/user/')), data=data)
            response = await self.send_request(request)
            if response.status_code == 201:
                return True
            else:
                return False

    async def login(self, user_data: dict) -> bool:
        data = {
            'email': user_data.get('email'),
            'password': user_data.get('password')
        }
        async with httpx.AsyncClient() as client:
            request = client.build_request(method='POST', url=str(self.url.with_path('api/token/')), data=data)
            response = await self.send_request(request)
            if response.status_code == 200:
                set_tokens(response.json(), self.user)
                return True
            else:
                return False

    async def profile(self):
        async with httpx.AsyncClient() as client:
            request = client.build_request(method='GET', url=str(self.url.with_path('api/v1/user/profile/')),
                                           headers=self.headers())
            response = await self.send_request(request)
            if response.status_code == 200:
                return response.json()
            else:
                return False

    async def profile_update(self, validated_data):
        profile_image_path = None
        if 'profile_image' in validated_data and validated_data['profile_image'] is not None:
            image = validated_data['profile_image'].split('/')
            if image[1] != 'media':
                profile_image_path = validated_data.get('profile_image') or None
        data = {
            'email': validated_data.get('email'),
            'first_name': validated_data.get('first_name'),
            'last_name': validated_data.get('last_name'),
            'phone': validated_data.get('phone'),
        }
        async with httpx.AsyncClient() as client:
            request = client.build_request(method='PATCH', url=str(self.url.with_path('api/v1/user/profile/update/')),
                                           headers=self.headers(),
                                           data=data,
                                           files={
                                           'profile_image': open(profile_image_path, 'rb')
                                           } if profile_image_path is not None else {})

            response = await self.send_request(request)
            if response.status_code == 200:
                return response.json()
            else:
                return False

    async def user_announcements(self):
        async with httpx.AsyncClient() as client:
            request = client.build_request(method='GET', url=str(self.url.with_path('api/v1/announcement/user/')),
                                           headers=self.headers())
            response = await self.send_request(request)
            if response.status_code == 200:
                return response.json()
            else:
                return False

class AnnouncementAPIClient(APIClient):

    def headers(self) -> dict:
        headers = {
            'accept': 'application/json',
            'Authorization': 'Bearer ' + get_token(self.user)
        }
        return headers

    async def get_house(self, pk):
        async with httpx.AsyncClient() as client:
            request = client.build_request(method='GET', url=str(self.url.with_path(f'api/v1/house/{pk}/')),
                                           headers=self.headers())
            response = await self.send_request(request)
            if response.status_code == 200:
                return response.json()['name']
            else:
                return False

    async def get_flat(self, pk):
        async with httpx.AsyncClient() as client:
            request = client.build_request(method='GET', url=str(self.url.with_path(f'api/v1/flat/{pk}/user/detail/')),
                                           headers=self.headers())
            response = await self.send_request(request)
            if response.status_code == 200:
                return response.json()
            else:
                return False

    async def get_section(self, pk):
        async with httpx.AsyncClient() as client:
            request = client.build_request(method='GET', url=str(self.url.with_path(f'api/v1/section/{pk}/')),
                                           headers=self.headers())
            response = await self.send_request(request)
            if response.status_code == 200:
                return response.json()
            else:
                return False

    async def get_floor(self, pk):
        async with httpx.AsyncClient() as client:
            request = client.build_request(method='GET', url=str(self.url.with_path(f'api/v1/floor/{pk}/')),
                                           headers=self.headers())
            response = await self.send_request(request)
            if response.status_code == 200:
                return response.json()
            else:
                return False

    async def get_corps(self, pk):
        async with httpx.AsyncClient() as client:
            request = client.build_request(method='GET', url=str(self.url.with_path(f'api/v1/corps/{pk}/')),
                                           headers=self.headers())
            response = await self.send_request(request)
            if response.status_code == 200:
                return response.json()
            else:
                return False

    async def list_announcement(self):
        async with httpx.AsyncClient() as client:
            request = client.build_request(method='GET', url=str(self.url.with_path("api/v1/announcement/user/")),
                                           headers=self.headers())
            print('REQUEST', request)
            response = await self.send_request(request)
            print('RESPONSELIST', response)
            if response.status_code == 200:
                return response.json()
            else:
                return False

    async def get_announcement(self, pk):
        async with httpx.AsyncClient() as client:
            request = client.build_request(method='GET', url=str(self.url.with_path(f"api/v1/announcement/{pk}/")),
                                           headers=self.headers())
            response = await self.send_request(request)
            if response.status_code == 200:
                return response.json()
            else:
                return False



if __name__ == '__main__':
    test = UserAPIClient(user='1946232317')
    async def cehck():
        test2 = await test.profile()
        print(test2)
    asyncio.run(cehck())
