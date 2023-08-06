# -*- coding: utf-8 -*-
import uuid
import random
import string
import time
import jwt
import datetime
import urllib.parse
from struct import unpack
from os import urandom


def generate_uuid(fmt: str = "-") -> str:
    '''
    生成uuid
    :param fmt: string, 默认为'-'
    :return: string
    '''
    return str(uuid.uuid4()).replace("-", fmt)


def snow_flake(datacenter_id: int = 1, worker_id: int = 1, sequence: int = 0) -> int:
    '''
    :param datacenter_id:  数据中心（机器区域）ID
    :param worker_id:  机器ID
    :param sequence: 其实序号
    :return: int
    '''
    return _SnowFlaskWorker(datacenter_id, worker_id, sequence).uuid()


def generate_rnd_string(n: int = 6, fmt: str = 'O') -> str:
    '''
    生成随机字符串
    :param n: int, 生成的字符串的位数
    :param fmt: str, 生成的字符串的格式
    :return: string, 返回一个随机字符串
    '''
    # 原生字符串
    raw = "abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ123456789"
    # 对应生成随机字符串的hash以及获取字符串长度
    rnd_hash = {
        "L": [0, 22],  # 全部小写
        "U": [23, 46],  # 全部大写
        "N": [47, 55],  # 全部数字
        "O": [0, 55]  # 随机数据
    }
    # 生成区段的key
    fmt = fmt.upper()
    key = rnd_hash.get(fmt, rnd_hash.get("O"))
    # 生成的字符串
    generate_srting = ""
    # 遍历数据
    for i in range(n):
        # 获取随机的索引值
        index = random.randint(*key)
        # 获取当前的字符串,并拼接到返回的字符串
        generate_srting += raw[index]
    # 返回的字符串
    return generate_srting


def generate_unique_id() -> str:
    '''
    生成一个11位唯一ID
    :return: string, 生成一个11位的随机唯一id
    '''
    num = unpack("<Q", urandom(8))[0]
    if num <= 0:
        result = "0"
    else:
        alphabet = string.digits + string.ascii_uppercase + string.ascii_lowercase
        key = []
        while num > 0:
            num, rem = divmod(num, 62)
            key.append(alphabet[rem])
        result = "".join(reversed(key))
    return result


def url_encode(url):
    '''
    url编码
    :param url: 原生的url地址
    :return: 编码后的url地址
    '''
    return urllib.parse.quote(url)


def url_decode(url):
    '''
    url解码
    :param url: url经过编码的地址
    :return: 返回解码后的url编码
    '''
    return urllib.parse.unquote(url)


def jwt_encode(raw: dict, secret: str = '1234567890', expire: int = 7200) -> str:
    '''
    jwt编码
    :param raw: 需要编码的字典
    :param secret: 密钥
    :param expire: 过期时间
    :return: 编码后的字符串
    '''
    try:
        raw.update({"exp": datetime.datetime.now() + datetime.timedelta(seconds=expire)})
        return jwt.encode(raw, secret, algorithm='HS256')  # 加密生成字符串
    except Exception as e:
        return ""


def jwt_decode(raw: str, secret: str = '1234567890') -> dict:
    '''
    jwt解码
    :param raw: 解码的字符串
    :param secret: 密钥
    :return: 解码后的字典
    '''
    try:
        return jwt.decode(raw, secret, algorithms=['HS256'])
    except Exception as e:
        return {}


class _ConstantFlake(object):
    # 64位ID的划分
    WORKER_ID_BITS = 5
    DATACENTER_ID_BITS = 5
    SEQUENCE_BITS = 12
    # 最大取值计算
    MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
    MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)
    # 移位偏移计算
    WOKER_ID_SHIFT = SEQUENCE_BITS
    DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
    TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS
    # 序号循环掩码
    SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)
    # Twitter元年时间戳
    TWEPOCH = 1288834974657


class _InvalidSystemClock(Exception):
    """
    时钟回拨异常
    """
    pass


class _SnowFlaskWorker(_ConstantFlake):
    """
    用于生成IDs
    """

    def __init__(self, datacenter_id, worker_id, sequence=0):
        """
        初始化
        :param datacenter_id: 数据中心（机器区域）ID
        :param worker_id: 机器ID
        :param sequence: 其实序号
        """
        # sanity check
        if worker_id > self.MAX_WORKER_ID or worker_id < 0:
            raise ValueError('worker_id值越界')

        if datacenter_id > self.MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('datacenter_id值越界')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1  # 上次计算的时间戳

    def _gen_timestamp(self):
        """
        生成整数时间戳
        :return:int timestamp
        """
        return int(time.time() * 1000)

    def uuid(self):
        """
        获取新ID
        :return:
        """
        timestamp = self._gen_timestamp()

        # 时钟回拨
        if timestamp < self.last_timestamp:
            raise _InvalidSystemClock

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & self.SEQUENCE_MASK
            if self.sequence == 0:
                timestamp = self._til_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        new_id = ((timestamp - self.TWEPOCH) << self.TIMESTAMP_LEFT_SHIFT) | (
                self.datacenter_id << self.DATACENTER_ID_SHIFT) | \
                 (self.worker_id << self.WOKER_ID_SHIFT) | self.sequence
        return new_id

    def _til_next_millis(self, last_timestamp):
        """
        等到下一毫秒
        """
        timestamp = self._gen_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._gen_timestamp()
        return timestamp
