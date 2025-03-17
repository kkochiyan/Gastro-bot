import json
import uuid
import aiohttp
from yandex_cloud_ml_sdk import YCloudML

from bot import AUTHORIZATION_KEYS, DEEPSEEK_API_KEY, IAM_TOKEN_YANDEX, FOLDER_ID

async def get_gigachat_token(auth_key):
    url = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json',
        'RqUID': str(uuid.uuid4()),
        'Authorization': f'Basic {auth_key}'
    }

    payload = {
        'scope': 'GIGACHAT_API_PERS'
    }

    async with aiohttp.ClientSession() as session:
         async with session.post(
             url=url,
             headers=headers,
             data=payload,
             ssl=False
         ) as response:
             result = await response.json()
             access_token = result.get('access_token')

    return access_token

async def get_token_balance(token):
    url = 'https://gigachat.devices.sberbank.ru/api/v1/balance'

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url=url, headers=headers, ssl=False) as response:
            if response.status == 200:
                balance_data = await response.json()
                return balance_data
            elif response.status == 403:
                print("Ошибка доступа: возможно, у вас нет прав на использование API.")
            elif response.status == 401:
                print("Ошибка авторизации: неверный токен.")
            else:
                print(f"Ошибка: {response.status}")
                return None

async def get_need_auth_key(auth_keys):
    for auth_key in auth_keys:
        token = await get_gigachat_token(auth_key)

        balance = await get_token_balance(token)
        remaining_tokens = 0

        for item in balance.get('balance', []):
            if item['usage'] == 'GigaChat':
                remaining_tokens = item['value']
                break

        if remaining_tokens > 0:
            return token

async def generate_recipe_with_GigaChat(promt: str):
    token = await  get_need_auth_key(AUTHORIZATION_KEYS)

    url = 'https://gigachat.devices.sberbank.ru/api/v1/chat/completions'

    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": promt,
            }
        ],
    })

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(url=url, headers=headers, data=payload, ssl=False) as response:
                if response.status == 200:
                    result = await response.json()
                    return result["choices"][0]["message"]["content"]
                else:
                    print(f'GigaChat вернул ошибку: {response.status}')
                    return None
        except Exception as e:
            print(f'Ошибка при запросе к GigaChat: {e}')
            return None

async def generate_recipe_with_deepseek(prompt: str):
    url = "https://api.deepseek.com/v1/chat/completions"

    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 1000
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=payload) as response:
            if response.status == 200:
                result = await response.json()
                return result["choices"][0]["message"]["content"]
            else:
                print(f"Ошибка {response.status}: {await response.text()}")
                return "Ошибка при запросе к DeepSeek"


def generate_recipe_with_yandex(prompt: str):
    sdk = YCloudML(
        folder_id="b1glo5o4rvrl7hnan9q1", auth=f'{IAM_TOKEN_YANDEX}'
    )
    model = sdk.models.completions("yandexgpt-lite", model_version="rc")
    model = model.configure(temperature=0.3)
    result = model.run(
        [
            {"role": "system", "text": ""},
            {
                "role": "user",
                "text": prompt,
            },
        ]
    )

    return result
