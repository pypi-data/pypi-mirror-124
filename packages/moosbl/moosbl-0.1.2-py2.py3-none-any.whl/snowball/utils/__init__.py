import httpx
from loguru import logger as log
from tenacity import retry, wait_fixed, stop_after_attempt

from .token import get_token


@retry(wait=wait_fixed(2), stop=stop_after_attempt(5))
def fetch(url, **kwargs):
    is_token = kwargs.pop('token', True)

    headers = {
        'Accept-Language': 'zh-Hans-CN;q=1, ja-JP;q=0.9',
        'Accept-Encoding': 'br, gzip, deflate',
        'User-Agent': 'Xueqiu iPhone 11.8',
        'Accept': 'application/json',
        'Host': "stock.xueqiu.com",
        'Connection': 'keep-alive',
        'Cookie': get_token() if is_token else '',
    }

    headers.update(kwargs.pop('headers', {}))

    client = httpx.Client()

    try:
        response = client.get(url, headers=headers, **kwargs)
        response.raise_for_status()

        return response.json()
    except httpx.HTTPStatusError as ex:
        log.warning(ex.response.text)
        log.warning('请求失败，正重试...')
    except httpx.ConnectError:
        log.warning('网络连接失败，请重试...')
    except IndexError as e:
        log.warning('数据解析错误，请求太频繁，请稍后重试...')
        log.debug(e)

    return None
