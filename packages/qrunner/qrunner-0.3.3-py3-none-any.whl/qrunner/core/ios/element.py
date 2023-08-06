import inspect
import time

from qrunner.core.ios.driver import d, driver, relaunch_wda
from qrunner.utils.log import logger


class Element:
    def __init__(self, **kwargs):
        self.index = kwargs.pop('index', 0)
        self.xpath = kwargs.get('xpath', '')
        self._kwargs = kwargs
        self._element = None

    @relaunch_wda
    def find_element(self, retry=3, timeout=3):
        logger.info(f'查找元素: {self._kwargs}')
        self._element = d.xpath(self.xpath) if self.xpath else d(**self._kwargs)[self.index]
        while not self._element.wait(timeout=timeout):
            if retry > 0:
                retry -= 1
                logger.warning(f'重试 查找元素： {self._kwargs}')
                time.sleep(1)
            else:
                frame = inspect.currentframe().f_back
                caller = inspect.getframeinfo(frame)
                logger.warning(f'【{caller.function}:{caller.lineno}】未找到元素 {self._kwargs}')
                return None
        return self._element

    @property
    @relaunch_wda
    def info(self):
        logger.info(f'获取元素 info 属性: {self._kwargs}')
        element = self.find_element(retry=0)
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        _info = element.info
        logger.info(f'元素info: {_info}')
        return _info

    # 用于常见分支场景判断
    @relaunch_wda
    def exists(self, timeout=1):
        logger.info(f'判断元素是否存在: {self._kwargs}')
        return self.find_element(retry=0, timeout=timeout) is not None

    @relaunch_wda
    def click(self):
        logger.info(f'点击元素: {self._kwargs}')
        element = self.find_element()
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        element.click()

    @relaunch_wda
    def send_keys(self, text, clear=True):
        logger.info(f'定位元素并输入{text}: {self._kwargs}')
        element = self.find_element()
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        element.click()
        if clear:
            element.clear_text()
        element.set_text()

    @relaunch_wda
    def scroll(self):
        logger.info(f'scroll to 元素: {self._kwargs}')
        element = self.find_element()
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        element.scroll()



