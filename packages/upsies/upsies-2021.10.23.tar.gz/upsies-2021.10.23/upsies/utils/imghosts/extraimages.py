# """
# Image uploader for extraimages.net
# """

# import json
# import time

# from ... import errors
# from ...utils import html, http
# from .base import ImageHostBase

# import logging  # isort:skip
# _log = logging.getLogger(__name__)


# class ExtraimagesImageHost(ImageHostBase):
#     """Upload images to extraimages.net"""

#     name = 'extraimages'

#     default_config = {
#         'base_url': 'https://extraimages.net',
#     }

#     async def _upload(self, image_path):
#         auth_token = await self._get_auth_token()
#         _log.debug('Auth token: %r', auth_token)

#         try:
#             response = await http.post(
#                 url=self.options['base_url'] + '/api/1/upload',
#                 cache=False,
#                 data={
#                     'type': 'file',
#                     'action': 'upload',
#                     'timestamp': int(time.time()),
#                     'auth_token': auth_token,
#                     'nsfw': '0',
#                 },
#                 files={
#                     'source': image_path,
#                 },
#             )
#         except errors.RequestError as e:
#             # Error response is undocumented. I looks like this:
#             raise
#             try:
#                 info = json.loads(e.text)
#                 raise errors.RequestError(f'{info["status_txt"]}: {info["error"]["message"]}')
#             except (TypeError, ValueError, KeyError):
#                 raise errors.RequestError(f'Upload failed: {e.text}')

#         _log.debug('%s: Response: %r', self.name, response)
#         info = response.json()
#         _log.debug('%s: JSON: %r', self.name, info)

#         # try:
#         #     return {
#         #         'url': info['image']['image']['url'],
#         #         'thumbnail_url': info['image']['medium']['url'],
#         #     }
#         # except KeyError:
#         #     raise RuntimeError(f'Unexpected response: {response}')

#     async def _get_auth_token(self):
#         response = await http.get(
#             url=self.options['base_url'] + '/',
#             cache=False,
#         )
#         doc = html.parse(response)
#         auth_token_tag = doc.find('input', attrs={'name': 'auth_token'})
#         if auth_token_tag:
#             return auth_token_tag['value']
#         else:
#             raise RuntimeError('Failed to find auth_token')
