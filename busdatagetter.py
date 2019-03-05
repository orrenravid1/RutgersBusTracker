from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

browser = webdriver.Chrome()

browser.get('https://rutgers.transloc.com/m/')

busroutes = browser.find_element_by_class_name("section_content")
for elem in busroutes.find_elements_by_tag_name('li'):
    print(elem.text)
    print(elem.tag_name)

'''
# Get all html of the webpage
elem = browser.find_element_by_xpath("//*")
print(elem.get_attribute('innerHTML'))
'''
