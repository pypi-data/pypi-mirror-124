import os

from loguru import logger


def get_token():
    logger.info('get_token is call')
    return 'xq_a_token=9bdd7d382e4b866e62c97739f4f11e95ae078042;'
    # if os.environ.get('XUEQIUTOKEN') is None:
    #     return 'xq_a_token=9bdd7d382e4b866e62c97739f4f11e95ae078042;'
    #     # raise Exception(cons.NO_TOKEN_ERROR_MSG)
    #
    # return os.environ['XUEQIUTOKEN']


def set_token(token):
    os.environ['XUEQIUTOKEN'] = token
    return os.environ['XUEQIUTOKEN']
