from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def custom_driver(disable_images=True):

    options = Options()
    options.add_argument("enable-automation")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-extensions")
    options.add_argument("--dns-prefetch-disable")
    options.add_argument("--disable-gpu")
    options.page_load_strategy = 'eager'
    
    if disable_images:
        chrome_prefs = {}
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        options.experimental_options["prefs"] = chrome_prefs


    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    return driver