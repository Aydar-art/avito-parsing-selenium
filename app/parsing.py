from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from settings import url

def get_page(url):
    options = Options()
    options.add_argument('--headless=new')

    driver = webdriver.Chrome(options=options)

    driver.get(url)
    driver.quit()


if __name__ == "__main__":
    get_page(url)