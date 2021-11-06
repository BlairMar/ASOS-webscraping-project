import pprint
import os
import time
import json
import itertools
import urllib.request
import selenium
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from tqdm import tqdm

class AsosScraper:
    def __init__(self, driver, gender: str):
        self.root = "https://www.asos.com/"
        self.gender = gender
        URL = self.root + gender
        self.driver = driver
        driver.get(URL)
        # object of ActionChains; it ads hover over functionality
        self.a = ActionChains(self.driver)
        self.links = []  # Initialize links, so if the user calls for extract_links inside other methods, it doesn't throw an error


    def choose_category(self):
        self.links = [] #href links to be scraped
        category_list = ['Clothing', 'Shoes', 'Accessories', 'Sportswear', 'Face + Body']
        elements_to_hover = [] #selenium web elements for the categories in category_list
        


        main_category_elements = self.driver.find_elements_by_xpath('//*[@id="chrome-sticky-header"]/div[2]/div[2]/nav/div/div/button[*]')
        #print(main_category_elements)
        
        for element in main_category_elements:
            main_category_heading = element.find_element_by_tag_name("span").find_element_by_tag_name("span").text
            if main_category_heading in category_list:
                elements_to_hover.append(element)
                #print(main_category_heading)
        #print(elements_to_hover)       

        for element in elements_to_hover:
            self.a.move_to_element(element).perform()
            time.sleep(3)
            subcategory_elements_list = self.driver.find_element_by_xpath('/html/body/div[3]/div/div[2]/header/div[3]/div/div[2]/div[2]/nav/div/div/div[4]/div/div[2]/ul/li[1]/ul').find_elements_by_tag_name("li")
            #print(subcategory_elements_list)
            
            for element in subcategory_elements_list:
                
                if element.find_element_by_tag_name("a").text == 'View all':
                    self.links.append(element.find_element_by_xpath('.//a').get_attribute('href'))
                    
                elif element.find_element_by_tag_name("a").text == 'New in':
                    self.links.append(element.find_element_by_xpath('.//a').get_attribute('href'))
                
                else:
                    pass
            
            print(self.links)



        



        



'''
#, main_category_xpath = '//*[@id="chrome-sticky-header"]/div[2]/div[2]/nav/div/div/button[*]'
    def choose_category(self):
        main_category_xpath = '//*[@id="chrome-sticky-header"]/div[2]/div[2]/nav/div/div/button[*]'
        self.subcategory_xpath = '/html/body/div[3]/div/div[2]/header/div[3]/div/div[2]/div[2]/nav/div/div/div[4]/div/div[2]/ul/li[1]/ul/li[*]/a'
        grandchildren = []
        category_list = ['Clothing', 'Shoes', 'Accessories', 'Sportswear', 'Face + Body']
        button_category_headings = self.driver.find_elements_by_xpath(main_category_xpath)

        for button in button_category_headings:
            grandchild = button.find_element_by_tag_name("span").find_element_by_tag_name("span").text
            if grandchild in category_list:
                #self.a.move_to_element(button).perform()
                #self.go_to_products_page(main_category_xpath)
            print(grandchild)
            print(button)
            grandchildren.append(grandchild)
         
        print(grandchildren)
'''



product_search = AsosScraper(webdriver.Chrome(),'men')
product_search.choose_category()
product_search.driver.quit()