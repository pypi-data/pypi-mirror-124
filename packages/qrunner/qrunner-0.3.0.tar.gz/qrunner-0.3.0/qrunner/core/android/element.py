import time
from qrunner.core.android.driver import Driver
from qrunner.utils.log import logger


# 初始化driver
driver = Driver()
d = driver.d


class Element:
    def __init__(self, *args, **kwargs):
        self.element_loc = kwargs
        self.xpath = kwargs.get('xpath', '')
        self.index = kwargs.pop('index', '')
        self._kwargs = kwargs
        self._element = None

    def find_element(self, retry=3, timeout=3):
        self._element = d.xpath(self.xpath) if self.xpath else d(**self._kwargs)[self.index]
        while not self._element.wait(timeout=timeout):
            if retry > 0:
                retry -= 1
                time.sleep(2)
            else:
                return None
        return self._element

    def exists(self, retry=0):
        logger.info(f'判断元素是否存在: {self.element_loc}')
        status = self.find_element(retry=retry) is not None
        logger.info(status)
        if not status:
            driver.allure_shot(f'元素定位失败: {self.element_loc}')
        return status

    def click(self):
        logger.info(f'点击元素: {self.element_loc}')
        element = self.find_element()
        if element is None:
            driver.allure_shot(f'元素定位失败: {self.element_loc}')
            return AssertionError(f'not found element {self._kwargs}')
        element.click()

    def click_exists(self):
        logger.info(f'点击元素: {self.element_loc}')
        element = self.find_element(retry=0)
        if element is None:
            driver.allure_shot(f'元素定位失败: {self.element_loc}')
            return AssertionError(f'not found element {self._kwargs}')
        element.click_exists()

    def send_keys(self, content, clear=True):
        logger.info(f'定位元素: {self.element_loc} ,并输入: {content}')
        element = self.find_element()
        if element is None:
            driver.allure_shot(f'元素定位失败: {self.element_loc}')
            return AssertionError(f'not found element {self._kwargs}')
        element.click()
        d.send_keys(str(content), clear=clear)
        time.sleep(1)

    @property
    def info(self):
        logger.info(f'获取元素{self.element_loc}的info')
        element = self.find_element()
        if element is None:
            driver.allure_shot(f'元素定位失败: {self.element_loc}')
            return AssertionError(f'not found element {self._kwargs}')
        _info = element.info
        logger.info(f'元素info：{_info}')
        return _info

