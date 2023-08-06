import asyncio
from json import loads

import httpx
import requests

from .errors import (
    LoginRequired,
    InvalidLogin,
    InvalidToken,
    TokenExpired
)


class SeedrAPI:
    def __init__(self, email=None, password=None, token=None):
        if email and password:
            data = {'grant_type': 'password', 'client_id': 'seedr_chrome', 'type': 'login', 'username': email,
                    'password': password}
            req = requests.post('https://www.seedr.cc/oauth_test/token.php', data=data)
            if 'access_token' in req.text:
                self.token = req.json()['access_token']
            else:
                raise InvalidLogin('Invalid username and password combination.')
        elif token:
            req = requests.get(f'https://www.seedr.cc/api/folder?access_token={token}')
            if 'space_max' in req.text:
                self.token = token
            else:
                raise InvalidToken('The access token provided is invalid.')
        else:
            raise LoginRequired('Account login required.')

    async def get_drive_async(self):
        token = self.token
        url = f'https://www.seedr.cc/api/folder?access_token={token}'
        async with httpx.AsyncClient() as client:
            req = await client.get(url)
            if 'invalid_token' in req.text:
                raise TokenExpired('Access token expired. Need to make new API Instance.')
            else:
                return loads(req.text)

    def get_drive(self):
        res = asyncio.run(self.get_drive_async())
        return res

    async def get_folder_async(self, id):
        token = self.token
        url = f'https://www.seedr.cc/api/folder/{id}?access_token={token}'
        async with httpx.AsyncClient() as client:
            req = await client.get(url)
            if 'access_denied' in req.text:
                raise Exception('Folder id invalid.')
            elif 'invalid_token' in req.text:
                raise TokenExpired('Access token expired. Need to make new API Instance.')
            else:
                return loads(req.text)

    def get_folder(self, id):
        res = asyncio.run(self.get_folder_async(id))
        return res

    async def get_file_async(self, id):
        token = self.token
        data = {'access_token': token, 'func': 'fetch_file', 'folder_file_id': id}
        async with httpx.AsyncClient() as client:
            req = await client.post('https://www.seedr.cc/oauth_test/resource.php', data=data)
            if 'access_denied' in req.text:
                raise Exception('File id invalid.')
            elif 'invalid_token' in req.text:
                raise TokenExpired('Access token expired. Need to make new API Instance.')
            else:
                return loads(req.text)

    def get_file(self, id):
        res = asyncio.run(self.get_file_async(id))
        return res

    async def add_torrent_async(self, magnet):
        token = self.token
        data = {'access_token': token, 'func': 'add_torrent', 'torrent_magnet': magnet}
        async with httpx.AsyncClient() as client:
            req = await client.post('https://www.seedr.cc/oauth_test/resource.php', data=data)
            if 'invalid_token' in req.text:
                raise TokenExpired('Access token expired. Need to make new API Instance.')
            else:
                return loads(req.text)

    def add_torrent(self, magnet):
        res = asyncio.run(self.add_torrent_async(magnet))
        return res

    async def delete_folder_async(self, id):
        token = self.token
        data = {'access_token': token, 'func': 'delete', 'delete_arr': [{'type': 'folder', 'id': id}]}
        async with httpx.AsyncClient() as client:
            req = await client.post('https://www.seedr.cc/oauth_test/resource.php', data=data)
            if 'invalid_token' in req.text:
                raise TokenExpired('Access token expired. Need to make new API Instance.')
            else:
                return loads(req.text)

    def delete_folder(self, id):
        res = asyncio.run(self.delete_folder_async(id))
        return res

    async def delete_file_async(self, id):
        token = self.token
        data = {'access_token': token, 'func': 'delete', 'delete_arr': [{'type': 'file', 'id': id}]}
        async with httpx.AsyncClient() as client:
            req = await client.post('https://www.seedr.cc/oauth_test/resource.php', data=data)
            if 'invalid_token' in req.text:
                raise TokenExpired('Access token expired. Need to make new API Instance.')
            else:
                return loads(req.text)

    def delete_file(self, id):
        res = asyncio.run(self.delete_file_async(id))
        return res

    async def rename_async(self, id, name):
        token = self.token
        data = {'access_token': token, 'func': 'rename', 'rename_to': name, 'file_id': id}
        async with httpx.AsyncClient() as client:
            req = await client.post('https://www.seedr.cc/oauth_test/resource.php', data=data)
            if 'invalid_token' in req.text:
                raise TokenExpired('Access token expired. Need to make new API Instance.')
            else:
                return loads(req.text)

    def rename(self, id, name):
        res = asyncio.run(self.rename_async(id, name))
        return res
