from pprint import pprint
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import itertools
import urllib.request
import zipfile

class AsosScraper:
     def __init__ (self, driver: webdriver.Chrome(), gender: str):
        self.root = "https://www.asos.com/"
        self.gender = gender
        URL = self.root + gender
        self.driver = driver 
        driver.get(URL)
        self.a = ActionChains(self.driver)  #object of ActionChains; it ads hover over functionality 
        self.links = [] # Initialize links, so if the user calls for extract_links inside other methods, it doesn't throw an error
       
     def extract_links(self, xpath: str): # given a common xpath, this method extracts the unique xpaths in a list and get the 'href' attribute for every unique xpath of an webelement
         xpaths_list = self.driver.find_elements_by_xpath(xpath) 
         self.links = []
         for item in xpaths_list:
            self.links.append(item.find_element_by_xpath('.//a').get_attribute('href'))
     
     def accept_cookies_button(self):
        time.sleep(4)
        click_accept_cookies = self.driver.find_element_by_xpath('//button[@class="g_k7vLm _2pw_U8N _2BVOQPV"]')
        click_accept_cookies.click()
     
     def choose_category(self):  #this method finds the second button (out of 12) from the category buttons top bar, and perform a hover over element function 
        category_button = self.driver.find_element_by_xpath('//*[@id="chrome-sticky-header"]/div[2]/div[2]/nav/div/div/button[2]')
        self.a.move_to_element(category_button).perform()  
        time.sleep(4)            #this will hover over the "New in" category and show the 'New in' subcategories

     def get_submenu_product_list(self): #this method uses the "extract_links" method to access the first href (self.links[0]) in the "New in" subcategories list, which is "New in -> View all "
         self.extract_links('//*[@id="029c47b3-2111-43e9-9138-0d00ecf0b3db"]/div/div[2]/ul/li[1]/ul/li[*]')
         self.driver.get(self.links[0])
     
     def get_product_list_urls(self): #this method uses the "extract_links" method to extract the hrefs for every product in the 'New in/View all' 
        self.extract_links('//*[@id="plp"]/div/div/div[2]/div/div[1]/section[1]/article')
        self.product_urls = self.links #save the list with hrefs in another variable that will be reffered to in the following methods
        
     def product_information(self): #this method will extract the product info, details and images from every product using it's given href
        self.xpath_dict = {
                'Product Name' : '//*[@id="aside-content"]/div[1]/h1', 
                'Price' : '//*[@id="product-price"]/div/span[2]/span[4]/span[1]', 
                'Product Details' : '//*[@id="product-details-container"]/div[1]/div/ul/li', 
                'Product Code' : '/html/body/div[2]/div/main/div[2]/section[2]/div/div/div/div[2]/div[1]/p', 
                'Colour' : '//*[@id="product-colour"]/section/div/div/span' 
                }
        url_counter = 0
        #for i,url in enumerate(self.product_urls): #TODO: use enumerate
        for url in self.product_urls:
            self.driver.get(url)
            url_counter += 1
            if url_counter == 4: #breaks after 3 items just for testing purposes
               break 
            self.product_information_dict = {f'Product{url_counter}':{'Product Name' : [], 'Price' : [],'Product Details' : [], 'Product Code' : [],'Colour': []}}
            

            try: #find details info
               for key in self.xpath_dict:
                  # click_show_more_button = self.driver.find_element_by_xpath(
                  #         '//*[@id="product-details-container"]/div[4]/div/a[1]')
                  # click_show_more_button.click()
                  if key == 'Product Details':
                     details_container = self.driver.find_elements_by_xpath(self.xpath_dict[key])
                     for detail in details_container:
                        self.product_information_dict[f'Product{url_counter}'][key].append(detail.text)

                  else:
                     dict_key = self.driver.find_element_by_xpath(self.xpath_dict[key])
                     self.product_information_dict[f'Product{url_counter}'][key].append(dict_key.text)

            except:
                  self.product_information_dict[f'Product{url_counter}'][key].append('No information found')
                   
            #download the each product images to the images folder        
            self.xpath_src_list = self.driver.find_elements_by_xpath('//*[@id="product-gallery"]/div[1]/div[2]/div[*]/img')
            self.src_list = []                                        
            for xpath_src in self.xpath_src_list:
               self.src_list.append(xpath_src.get_attribute('src'))
        
            for i,src in enumerate(self.src_list[:-1]):   
               urllib.request.urlretrieve(src, f"images\{self.gender}_Product{url_counter}.{i}.jpg")

            # print(self.product_information_dict)
                     
            # for key in self.xpath_dict:
            #    click_show_more_button = self.driver.find_element_by_xpath(
            #               '//*[@id="product-details-container"]/div[4]/div/a[1]')
            #    click_show_more_button.click()
            #    if key == 'Product Details':
            #       details_container = self.driver.find_elements_by_xpath(self.xpath_dict[key])
            #       for detail in details_container:
            #          self.product_information_dict[f'Product{url_counter}'][key].append(detail.text)
               
            #    elif key != 'Product Details':
            #       dict_key = self.driver.find_element_by_xpath(self.xpath_dict[key])
            #       self.product_information_dict[f'Product{url_counter}'][key].append(dict_key.text)
   
            #    else:
            #       self.product_information_dict[f'Product{url_counter}'][key].append('No information found')
            
            # print(self.product_information_dict[f'Product{url_counter}']['Product Details'])

            # self.xpath_src_list = self.driver.find_elements_by_xpath('//*[@id="product-gallery"]/div[1]/div[2]/div[*]/img')
            # self.src_list = []
            # for xpath_src in self.xpath_src_list:
            #       self.src_list.append(xpath_src.get_attribute('src'))
            #       # print(self.src_list)
            
            # filename = r'C:\Users\Miruna\Desktop\Web Scraper ASOS\ASOS-webscraping-project\images\f"{self.gender}_Product{url_counter}.{i}.jpg"'
            # # destination_path = r'C:\Users\Miruna\Desktop\Web Scraper ASOS\ASOS-webscraping-project\images'
            # for i,src in enumerate(self.src_list):
            #     urllib.request.urlretrieve(src,f"images\{self.gender}_Product{url_counter}.{i}.jpg")
                
            
            print(self.product_information_dict)
            
# time.sleep(10)
# import shutil

# source_folder = r"C:\Users\Miruna\Desktop\Web Scraper ASOS\ASOS-webscraping-project\\"
# destination_folder = r"C:\Users\Miruna\Desktop\Web Scraper ASOS\ASOS-webscraping-project\images"
# files_to_move = [x for x in source_folder if x.endswith('.jpg')]

# # # iterate files
# for file in files_to_move:
#     # construct full file path
#     source = source_folder + file
#     destination = destination_folder + file
#     # move file
#     shutil.move(source, destination)
#     print('Moved:', file)
# print(files_to_move)
# #      def get_image_source(self, link: str) -> None:
# #          self.driver.get(link)
# #          time.sleep(0.5)
         

# #      def download_images(self, i) -> None:
# #          urllib.request.urlretrieve(self.src, f"{self.animal}_{i}.jpg")
    
# #      def get_animal_images(self):
#         #  self.extract_links()
#         # for i, link in enumerate(self.links):
#         #     self.get_image_source(link)
#         #     self.download_images(i)
#         # self.links = []
    

product_search = AsosScraper(webdriver.Chrome(),'men')
# product_search.accept_cookies_button()
# product_search.choose_category()
# product_search.get_submenu_product_list()
# # product_search.choose_subcategory()
# product_search.get_product_list_urls()
# product_search.product_information()