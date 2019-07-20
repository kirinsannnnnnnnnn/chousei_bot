from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys

def get_url(event_name="test_event_name", event_kouho="test_kouho", event_memo=None):
  options = ChromeOptions()
  options.add_argument("--headless")
  driver = Chrome(options=options)
  driver.get("https://chouseisan.com/")

  driver.find_element_by_xpath(
      '//*[@id="name"]').send_keys(
      event_name)
  if event_memo is not None:
    driver.find_element_by_xpath(
        '//*[@id="comment"]').send_keys(
        event_memo)

  driver.find_element_by_xpath(
      '//*[@id="kouho"]').send_keys(
      event_kouho)

  driver.find_element_by_xpath(
      '//*[@id="createBtn"]').click()    
  final_url = driver.find_element_by_xpath(
      '//*[@id="listLink"]/div').click()

  final_url = driver.current_url

  # driver.save_screenshot("test.png")

  return final_url
