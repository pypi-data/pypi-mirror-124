import inspect
import time
from qrunner.utils.log import logger
from qrunner.core.android.driver import driver, d


# 安卓原生元素
class Element:
    def __init__(self, **kwargs):
        self.index = kwargs.pop('index', 0)
        self.xpath = kwargs.get('xpath', '')
        self._kwargs = kwargs
        self._element = None

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
    def info(self):
        logger.info(f'获取元素 info 属性: {self._kwargs}')
        element = self.find_element(retry=0)
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        _info = element.info
        logger.info(f'元素info: {_info}')
        return _info

    # 用于常见分支场景判断
    def exists(self, timeout=1):
        logger.info(f'判断元素是否存在: {self._kwargs}')
        return self.find_element(retry=0, timeout=timeout) is not None

    def click(self):
        logger.info(f'点击元素: {self._kwargs}')
        element = self.find_element()
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        element.click()

    def send_keys(self, text, clear=True):
        logger.info(f'定位元素并输入{text}: {self._kwargs}')
        element = self.find_element()
        if element is None:
            raise AssertionError(f'未定位到元素: {self._kwargs}')
        element.click()
        d.send_keys(str(text), clear=clear)
        d.send_action('search')
        d.set_fastinput_ime(False)





