import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import DesiredCapabilities
import configparser
from src.util.utilities2 import Utilities
import sys
import os

class DriverFactory:


    #HINT: set another dir to chrome:  https://stackoverflow.com/questions/45500606/set-chrome-browser-binary-through-chromedriver-in-python



    '''
    Retorna webdriver
    Parâmetros: chrome, firefox, phantomjs
    '''
    # def create_driver(self, type, headless=False):
    #     self.create_driver(type, headless, None)


    # def create_driver(self, type, headless=False, path_to_download=None, install_extension=None, largura=1440, altura=900):
    def create_driver(self, type, headless=False, path_to_download=None, install_extension=None, largura=800, altura=800, kiosk=False):
        try:
            #util = Utilities()
            util = Utilities(sys.argv[0], os.getpid(), test_config_dir_direto=True)
            config = util.get_config()
            #config = configparser.ConfigParser()
            #config.read('config/config.ini')

            print(f'path_to_download = {path_to_download}')


            try:
                dir_extensions = config['extensions_chrome']['dir_extensions']
                print(f'create_driver: dir_extensions={dir_extensions}')
            except Exception as e:
                print(f'create_driver: DEU erro no dir_extensions: {e}')
                dir_extensions = ''

            try:
                extensions_to_install = config['extensions_chrome']['extensions_to_install']
                print(f'create_driver: extensions_to_install={extensions_to_install}')


            except Exception as e:
                print(f'create_driver: DEU erro no extensions_to_install: {e}')
                extensions_to_install = ''



            if type == 'chrome' or type == '':
                    #print('chrome 001')
                    chrome_options = Options()
                    chrome_options.add_argument('log-level=3')
                    chrome_options.add_argument(f'{path_to_download}')

                    # chrome_options.add_argument("enable-automation")

                    chrome_options.add_argument('disable-infobars')
                    # chrome_options.add_argument("--disable-login-animations")
                    # chrome_options.add_argument("--disable-notifications")
                    # chrome_options.add_argument("--disable-default-apps")

                    # chrome_options.add_argument("--no-sandbox")


                    # chrome_options.add_argument("--dns-prefetch-disable")
                    # chrome_options.add_argument("--dns-prefetch-disable")

                    #chrome_options.add_argument('--user-agent=Mozilla/5.0 (iPhone; CPU iPhone OS 10_3 like Mac OS X) AppleWebKit/602.1.50 (KHTML, like Gecko) CriOS/56.0.2924.75 Mobile/14E5239e Safari/602.1')

                    # mobile_emulation = {"deviceName": "Nexus 5"}
                    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
                    #print('chrome 002')


                    if install_extension == True:
                        try:
                            list_extensions_to_install=extensions_to_install.split(';')
                            print(f'create_driver: list_extensions_to_install: {list_extensions_to_install}')
                            qtde_extensions_to_install=len(list_extensions_to_install)
                            while qtde_extensions_to_install > 0:
                                valor_indice=qtde_extensions_to_install-1
                                print(f'create_driver: instalando Extensão local {list_extensions_to_install[valor_indice]}')
                                #chrome_options.add_extension('Save-to-Pocket_v3.0.0.11.crx')
                                chrome_options.add_extension(f'{dir_extensions}/{list_extensions_to_install[valor_indice]}')
                                print(f'create_driver: Instalado! Extensão local {dir_extensions}/{list_extensions_to_install[valor_indice]}')
                                time.sleep(2)
                                qtde_extensions_to_install -= 1

                        except Exception as e:
                            print(f'create_driver: DEU erro if install_extension: {e}')

                    # chrome_options.add_argument('window-size=800,800');
                    # chrome_options.add_argument('window-size=1000,900');
                    # chrome_options.add_argument(f'window-position=-{largura},1')
                    chrome_options.add_argument(f'window-position=1,1')
                    chrome_options.add_argument(f'window-size={largura},{altura}')

                    if kiosk == True:
                        chrome_options.add_argument("--start-maximized")
                        chrome_options.add_argument("--kiosk")  ##esse é muito interessante para colocar no raspberry e na tv



                    # chrome_options.add_experimental_option('useAutomationExtension', False)
                    # chrome_options.add_experimental_option('excludeSwitches', ['load-extension', 'enable-automation'])




                    # chrome_options.add_argument('--shm-size')  # enio 30/10/2020
                    chrome_options.add_argument('--disable-impl-side-painting')  # enio 30/10/2020
                    chrome_options.add_argument('--disable-accelerated-2d-canvas')  # enio 30/10/2020
                    chrome_options.add_argument('--disable-accelerated-jpeg-decoding')  # enio 30/10/2020
                    chrome_options.add_argument('--no-sandbox')  # enio 30/10/2020
                    chrome_options.add_argument('--test-type=ui')  # enio 30/10/2020

                    chrome_options.add_argument('--force-device-scale-factor=1')

                    chrome_options.add_argument('--dns-prefetch-disable')
                    chrome_options.add_argument('--always-authorize-plugins')
                    chrome_options.add_argument('--aggressive-cache-discard')
                    chrome_options.add_argument('--disable-cache')
                    chrome_options.add_argument('--disable-application-cache')
                    chrome_options.add_argument('--disable-offline-load-stale-cache')
                    chrome_options.add_argument('--disk-cache-size=1000')
                    chrome_options.add_argument('--no-proxy-server')







                    chrome_options.add_argument('--disable-dev-shm-usage')  # 3nio
                    chrome_options.add_argument("--ignore-certificate-errors")  #



                    if headless == True:
                        # chrome_options.add_argument('window-size=1000,900');
                        # chrome_options.add_argument(f'window-size={largura},{altura}')
                        chrome_options.add_argument("headless")
                        # chrome_options.add_argument("disable-gpu") #
                        # chrome_options.add_argument("--test-type") #enio
                        # chrome_options.add_argument('--no-sandbox') #enio
                        # chrome_options.add_argument('--disable-dev-shm-usage') #3nio
                        # chrome_options.add_argument('--use-gl=swiftshader') #
                        # chrome_options.add_argument("--ignore-certificate-errors")#
                        # chrome_options.add_argument('--disable-popup-blocking')    #add enio
                        chrome_options.add_argument('--disable-gpu')    #add enio #
                        # chrome_options.add_argument('--disable-gpu-sandbox')  # enio 30/10/2020
                        # chrome_options.binary_location = config['drivers']['chrome_path']
                        print('create_driver: chrome 005 headless true')

                    prefs = {}
                    # Add preferências para não exibit PDF viewer
                    prefs["download.prompt_for_download"] = False
                    prefs["plugins.always_open_pdf_externally"] = True
                    # prefs["profile.default_content_setting_values.notifications"] = 2

                    prefs["profile.password_manager_enabled"] = False
                    prefs["credentials_enable_service"] = False

                    # print('chrome 003')
                    # Configuração para ceitar qualquer certificados
                    # capabilities = DesiredCapabilities.CHROME.copy()
                    capabilities = {}
                    capabilities['acceptSslCerts'] = True
                    capabilities['acceptInsecureCerts'] = True
                    print('create_driver: chrome 004')

                    if not path_to_download is None:
                        #print('chrome 006')
                        print('create_driver: Iniciando chrome em path alternativo:' + path_to_download)
                        prefs['download.default_directory'] = path_to_download
                        prefs['download.prompt_for_download'] = False
                        print('create_driver: chrome 007')



                    print('create_driver: chrome 008')
                    chrome_options.add_experimental_option('prefs', prefs)
                    chromepath = config['drivers']['chrome_path']
                    print(f'create_driver: chrome 009 chromepath={chromepath}')
                    #driver = webdriver.Chrome(chromepath, chrome_options=chrome_options,desired_capabilities=capabilities)  # Optional argument, if not specified will search path.
                    print('create_driver: chrome 009b')
                    #driver = webdriver.Chrome(executable_path=chromepath,chrome_options=chrome_options,desired_capabilities=capabilities)  # Optional argument, if not specified will search path.



                    # mobile_emulation = {"deviceName": "Nexus 5"}
                    # chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

                    # driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities=chrome_options.to_capabilities())

                    print(f'create_driver: chrome 009c chromepath={chromepath} / chrome_options={chrome_options} / capabilities={capabilities}')

                    driver = webdriver.Chrome(executable_path=chromepath,chrome_options=chrome_options,desired_capabilities=capabilities)  # Optional argument, if not specified will search path.

                    print('create_driver: chrome 0010 carregado driver')
                    # try:
                    #     print('\n\n\n------\n-------\nchrome position window: ini')
                    #
                    #     # driver.Manage().Window.Position = new System.Drawing.Point(2000, 1)
                    #     # driver.Manage().Window.Maximize();
                    #
                    #     # time.sleep(2)
                    #     # driver.set_window_position(300, 0)
                    #     # time.sleep(2)
                    #     # # driver.maximize_window()
                    #     # time.sleep(2)
                    #     # driver.set_window_position(-1200, 0)
                    #     # time.sleep(2)
                    #     # #driver.maximize_window()
                    #     # # time.sleep(2)
                    #     # # driver.set_window_position(100, 100)
                    #     # # time.sleep(2)
                    #     # driver.set_window_size(largura, altura)
                    #     print('chrome position window: fim\n------\n-------\n\n\n')
                    #     time.sleep(2)
                    # except Exception as e:
                    #     print(f'\n\n\n------\n-------\n\n\nerro chrome position window: {e}')
                    #     time.sleep(20)

                    #print('chrome 010')
                    try:
                        print('create_driver: chrome 0011a vai tentar if headless == True')
                        if headless == True:
                            print('create_driver: chrome 0011b dentro if headless == True')
                            print('create_driver: chrome 011 headless true')
                            driver.command_executor._commands["send_command"] = (
                                "POST",
                                '/session/$sessionId/chromium/send_command')
                            params = {
                                'cmd': 'Page.setDownloadBehavior',
                                'params': {
                                    'behavior': 'allow',
                                    'downloadPath': path_to_download
                                }
                            }
                            driver.execute("send_command", params)
                        print('create_driver: chrome 0011c saiu if headless == True')


                        print('create_driver: chrome 012')
                    except Exception as e:
                        print(f'create_driver: erro no if headless == True POST - {e}')

                    print('create_driver: chrome 0013 vai para return driver')
                    return driver

            elif type == 'firefox':
                    #print('chrome 013')
                    firefoxpath = config['drivers']['firefox_path']
                    driver = webdriver.Firefox(firefoxpath)
                    return driver

            elif type == 'phantomjs':
                    phantomjspath = config['drivers']['phantomjs_path']
                    driver = webdriver.PhantomJS(phantomjspath)
                    return driver
        except Exception as e:
            print(f'create_driver: DEU erro ao criar driver {e}')
