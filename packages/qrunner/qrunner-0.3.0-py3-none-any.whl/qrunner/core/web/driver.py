import requests
from selenium import webdriver
from qrunner.utils.log import logger
from conf.config import conf
from qrunner.core.android.element import driver


class Driver(object):
    # _instance = {}
    #
    # def __new__(cls, serial_no=None):
    #     if serial_no not in cls._instance:
    #         cls._instance[serial_no] = super().__new__(cls)
    #     return cls._instance[serial_no]

    def __init__(self, serial_no=None, pkg_name=None):
        if not serial_no:
            self.serial_no = conf.get_name('device', 'serial_no')
        else:
            self.serial_no = serial_no
        if not pkg_name:
            self.pkg_name = conf.get_name('app', 'pkg_name')

        logger.info(f'启动webdriver')
        options = webdriver.ChromeOptions()
        options.add_experimental_option('androidDeviceSerial', self.serial_no)
        options.add_experimental_option('androidPackage', self.pkg_name)
        options.add_experimental_option('androidUseRunningApp', True)
        options.add_experimental_option('androidProcess', self.pkg_name)
        self.d = webdriver.Chrome(options=options)
        self.d.set_page_load_timeout(10)

    def back(self):
        logger.info('返回上一页')
        self.d.back()

    def send_keys(self, value):
        logger.info(f'输入文本: {value}')
        driver.send_keys(value)

    def switch_input(self):
        logger.info('切换输入法')
        driver.d.set_fastinput_ime(enable=False)

    def screenshot(self, filename, timeout=3):
        driver.wait_shot(filename, timeout=timeout)

    def get_page(self):
        page_source = self.d.page_source
        logger.info(f'获取页面内容: \n{page_source}')
        return page_source

    def get_wins(self):
        logger.info(f'获取当前打开的窗口列表')
        return self.d.window_handles

    def switch_win(self, old_windows):
        logger.info('切换到最新的window')
        current_windows = self.d.window_handles
        newest_windows = [window for window in current_windows if window not in old_windows]
        if newest_windows:
            self.d.switch_to.window(newest_windows[0])

    def close(self):
        logger.info('关闭webdriver')
        self.d.close()

    # @relaunch
    # def execute_js(self, script, element):
    #     logger.info(f'执行js脚本: \n{script}')
    #     self.d.execute_script(script, element)

    # 在页面元素被覆盖的情况下使用
    def click(self, element):
        self.d.execute_script('arguments[0].click();', element)








