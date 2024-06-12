from types import TracebackType
from typing import Type
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from tqdm import tqdm
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException

class Land_page(webdriver.Chrome):
    def __init__(self, driver_path=r"./chromedriver",
                 tear_down=False):
        self.driver_path = driver_path
        self.tear_down = tear_down
        os.environ["PATH"] += os.pathsep + os.path.abspath(self.driver_path)
        chrome_options = Options()
        chrome_options.add_experimental_option("detach", True)
        super(Land_page, self).__init__(options=chrome_options)
        self.implicitly_wait(15)
        
    def __exit__(self, exc_type: Type[BaseException], exc: BaseException, traceback: TracebackType):
        if self.tear_down:
            self.quit()

    def land_page(self, url):
        self.get(url)

    def pull_all_images_on_page(self, first_n_elements=1000):
        all_links = set()
        n = 0
        last_height = self.execute_script("return document.body.scrollHeight")

        while n < first_n_elements:
            self.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
            time.sleep(3)  # Allow time for new content to load

            div_list = self.find_elements(By.CSS_SELECTOR, 'div[class="Pj7 sLG XiG ho- m1e"]')
            new_links = set()
            for div in div_list:
                try:
                    img = div.find_element(By.TAG_NAME, 'img')
                    link = img.get_attribute('src')
                    if link and link not in all_links:
                        new_links.add(link)
                        n += 1
                        if n >= first_n_elements:
                            break
                except StaleElementReferenceException:
                    continue
                except NoSuchElementException:
                    continue

            all_links.update(new_links)
            print(f"Collected {len(all_links)} unique images so far.")

            # Check if the scroll reached the bottom of the page
            new_height = self.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

        if self.tear_down:
            self.quit()
        return list(all_links)
    
def get_org_link(link):
    link = link.split('/')
    link[3] = 'originals'
    return '/'.join(link)

def write2data(img_links):
    with open('C:\Workspace\Aimesoft\Building\Project1_data_tools\data\img_links.txt', 'a') as f:
        for link in img_links:
            f.write(get_org_link(link) + '\n')

if __name__ == '__main__':
    all_links = []
    urls = ['https://www.pinterest.com/search/pins/?q=design%20building&rs=typed',
            'https://www.pinterest.com/search/pins/?q=design%20single%20building&rs=typed']
    for url in urls:
        try:
            land_page = Land_page()
            land_page.land_page(url)
            links = land_page.pull_all_images_on_page(first_n_elements=700)
            all_links.extend(links)
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            land_page.quit()  # Ensure the driver is closed in any case

    # print(len(all_links))
    # print(all_links)
    all_links = list(set(all_links))
    img_links = [get_org_link(link) for link in all_links]
    write2data(img_links)
    