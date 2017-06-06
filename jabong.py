#By Shikha Panwar
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import sys

import unittest, time, re
import csv
 

path_to_chromedriver = '/home/shikha/Document/libraries/chromedriver' # change path to chrome driver as needed

class Sel(unittest.TestCase):
    def setUp(self):
        
        opt = webdriver.ChromeOptions()
        # this extension disables loading of images in the browser, hence increasing speed
        opt.add_extension("/home/shikha/Document/libraries/Block-image_v1.1.crx") # change path to the extension as needed
        self.driver = webdriver.Chrome(executable_path = path_to_chromedriver, chrome_options=opt)

        self.driver.implicitly_wait(30)
        self.base_url = "http://www.jabong.com/men/clothing/polos-tshirts/?sort=popularity&dir=desc&source=topnav_men"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_sel(self):
        
        driver = self.driver
        delay = 2
        driver.get(self.base_url )
        # the page is loaded
        for i in range(1,250)  :
            time.sleep(delay)
            element = self.driver.find_element_by_tag_name('footer');
            element.location_once_scrolled_into_view
            x = self.driver.find_element_by_class_name('load-more-products')
            if x.is_displayed() and x.is_enabled() :
                x.click()
            print i


        #output csv file to save the list

        ofile  = open('tshirt_list.csv', "wb")
        writer = csv.writer(ofile, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        #format of csv is ["Title", "Original Price", "Discounted Price", "URL"]
        writer.writerow(["Title", "Original Price", "Discounted Price", "URL" ])

        html_source = driver.page_source
        data = html_source.encode('utf-8')
        soup = BeautifulSoup(data)
        mydivs = soup.findAll("div", { "class" : "product-tile"})


        count = 0

        for div in mydivs:

            count = count + 1;
            if count >10000 :
                break
            title_tag = div.find('div',{"h4"} )
            title = title_tag.text

            original_price_tag = div.find('span', {"class" : "prev-price"})

            if original_price_tag :
                original_price = original_price_tag.text
                temp = div.find('span', {"class" : "product-price"})
                if temp :
                    discounted_price_tag = temp
                else :
                    temp = original_price_tag
                    temp = temp.find_next_sibling("div", class_="standard-price")     
                        

            else :
                original_price_tag = div.find('span', {"class" : "standard-price"})
                discounted_price_tag = original_price_tag

            original_price = original_price_tag.text
            discounted_price = discounted_price_tag.text
            url  = "http://www.jabong.com" + div.find("a")["href"]
            if count == 1 :  # this is because the first one is within a section of dummy class
                continue 
            writer.writerow([title.encode('utf-8'), original_price.encode('utf-8'), discounted_price.encode('utf-8'), url.encode('utf-8') ])

        ofile.close()


        print "No. of Tshirt list saved in file tshirt_list.csv = " + str(len(mydivs))
    

if __name__ == "__main__":
    unittest.main()
