# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['emo_platform']

package_data = \
{'': ['*'], 'emo_platform': ['tokens/.gitkeep']}

install_requires = \
['aiohttp', 'fastapi', 'requests', 'uvicorn']

setup_kwargs = {
    'name': 'emo-platform-api-sdk',
    'version': '0.1.0',
    'description': 'emo platform api python sdk',
    'long_description': '# BOCCO emo platform api python sdk (β version)\n\n## How to install\n### Using poetry (if you want to use in python virtual environment)\nIf poetry has not been installed, please see [this page](https://python-poetry.org/docs/) to install.\n\n```bash\n# Python 3.7+ required\npoetry install --no-dev\n```\n\nWhen you execute python code,\n\n```bash\npoetry run python your_python_code.py\n```\n\n### Using PyPl\n\n```\n# Python 3.7+ required\n$ pip3 install emo-platform-api-sdk\n```\n\n## Setting api tokens\n\nYou can see access token & refresh token from dashboard in [this page](https://platform-api.bocco.me/dashboard/login) after login.\n\nThen, set those tokens as environment variables.\n\n```bash\nexport EMO_PLATFORM_API_ACCESS_TOKEN="***"\nexport EMO_PLATFORM_API_REFRESH_TOKEN="***"\n```\n\n## Usage Example\n\nYou can also see other examples in "examples" directory.\n\n### Note\n- When you initialize emo_platform.Client, two json files (emo-platform-api.json & emo-platform-api_previous.json) are created in the path where emo_platform module was installed.\n\t- These files are used to store the tokens information.\n\t- See the documentation for details.\n- You can change the path where these json files are created, as shown below.\n\n```python\nimport os\nfrom emo_platform import Client\n\nCURRENT_DIR = os.path.abspath(os.path.dirname(__file__))\n\nclient = Client(token_file_path=CURRENT_DIR)\n```\n\n### Example1 : Using client\n```python\nfrom emo_platform import Client, Head\n\nclient = Client()\n\nprint(client.get_account_info())\nprint(client.get_stamps_list())\n\nroom_id_list = client.get_rooms_id()\nroom_client = client.create_room_client(room_id_list[0])\n\nprint(room_client.get_msgs())\nroom_client.move_to(Head(10,10))\n```\n\n### Example2 : Receive webhook\n\nIn another terminal, execute ngrok and copy URL forwarded to http://localhost:8000.\n```bash\nngrok http 8000\n```\n\n```python\nfrom emo_platform import Client, WebHook\n\nclient = Client()\n# Please replace "YOUR WEBHOOK URL" with the URL forwarded to http://localhost:8000\nclient.create_webhook_setting(WebHook("YOUR WEBHOOK URL"))\n\n@client.event(\'message.received\')\ndef message_callback(data):\n\tprint(data)\n\n@client.event(\'illuminance.changed\')\ndef illuminance_callback(data):\n\tprint(data)\n\nclient.start_webhook_event()\n\n```\n',
    'author': 'Keita Ito',
    'author_email': 'kito@ux-xu.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://yukai.github.io/emo-platform-api-python/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
