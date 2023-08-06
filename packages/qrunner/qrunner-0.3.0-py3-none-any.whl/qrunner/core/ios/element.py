import time

from qrunner.core.ios.driver import Driver
from qrunner.core.ios.driver import relaunch_wda
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

    @relaunch_wda
    def find_element(self, retry=3, timeout=3):
        self._element = d.xpath(self.xpath) if self.xpath else d(**self._kwargs)[self.index]
        while not self._element.wait(timeout=timeout):
            if retry > 0:
                retry -= 1
                time.sleep(2)
            else:
                return None
        return self._element

    @relaunch_wda
    def exists(self, retry=0):
        logger.info(f'判断元素是否存在: {self.element_loc}')
        status = self.find_element(retry=retry) is not None
        logger.info(status)
        if not status:
            driver.allure_shot(f'元素定位失败: {self.element_loc}')
        return status

    @relaunch_wda
    def click(self):
        logger.info(f'点击元素: {self.element_loc}')
        element = self.find_element()
        if element is None:
            driver.allure_shot(f'元素定位失败: {self.element_loc}')
            return AssertionError(f'not found element {self._kwargs}')
        element.click()

    @relaunch_wda
    def click_exists(self):
        logger.info(f'点击元素: {self.element_loc}')
        element = self.find_element(retry=0)
        if element is None:
            driver.allure_shot(f'元素定位失败: {self.element_loc}')
            return AssertionError(f'not found element {self._kwargs}')
        element.click_exists()

    @relaunch_wda
    def send_keys(self, content):
        logger.info(f'定位元素: {self.element_loc} ,并输入: {content}')
        element = self.find_element()
        if element is None:
            driver.allure_shot(f'元素定位失败: {self.element_loc}')
            return AssertionError(f'not found element {self._kwargs}')
        element.click()
        element.clear_text()
        d.send_keys(str(content))
        time.sleep(1)

    @relaunch_wda
    @property
    def info(self):
        logger.info(f'获取元素{self.element_loc}的info')
        element = self.find_element()
        if element is None:
            driver.allure_shot(f'元素定位失败: {self.element_loc}')
            return AssertionError(f'not found element {self._kwargs}')
        _info = {
            'name': element.name,
            'label': element.label,
            'value': element.value,
            'text': element.text,
            'className': element.className,
            'visible': element.visible,
            'enabled': element.enabled,
            'displayed': element.displayed
        }
        logger.info(f'元素info：{_info}')
        return _info

    @relaunch_wda
    def scroll(self):
        logger.info(f'滚动到该元素: {self.element_loc}')
        element = self.find_element()
        if element is None:
            driver.allure_shot(f'元素定位失败: {self.element_loc}')
            return AssertionError(f'not found element {self._kwargs}')
        element.scroll()




