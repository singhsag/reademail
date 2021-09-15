import fetch_urls as urls
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import datetime


class ClickUrlsAndWait:
    @staticmethod
    def test():
        global counter, url_list
        global write
        write = False
        try:
            url_list = urls.get_urls_list()
            counter = 0
            for url in url_list:
                chrome_options = Options()
                chrome_options.add_argument("--headless")
                chrome_options.add_argument("--disable-gpu")
                chrome_options.add_argument("--no-sandbox")
                chrome_options.add_argument("enable-automation")
                chrome_options.add_argument("--disable-infobars")
                chrome_options.add_argument("--disable-dev-shm-usage")
                driver = webdriver.Chrome(options=chrome_options)

                if "paid-to-read-email.com/open" in url:
                    driver.get(url)
                    time.sleep(5)
                    window_before = driver.window_handles[0]
                    driver.find_element_by_id("paidemail").click()
                    time.sleep(5)
                    driver.switch_to.window(window_before)
                    time.sleep(5)
                    status = driver.find_elements_by_xpath("//*[contains(text(),'credited')]")
                    if status:
                        counter = counter + 1
                    driver.close()
                if "paid-to-read-email.com/mail" in url:
                    print('inside second if')
                    driver.get(url)
                    print('inside second if got url')
                    time.sleep(5)
                    window_before = driver.window_handles[0]
                    driver.find_element_by_xpath("//a[contains(@href,'paid-to-read-email.com/inbox')"
                                                 " and @class='content_block_bt_1']").click()
                    time.sleep(5)
                    driver.switch_to.window(window_before)
                    time.sleep(5)
                    status = driver.find_elements_by_xpath("//*[contains(text(),'Thank you')]")
                    driver.find_element_by_xpath(" //a[contains(text(), 'PaidEmail')]").click()
                    time.sleep(2)
                    if status:
                        counter = counter + 1
                    driver.close()
            write = False
            final = 'On ' + str(datetime.datetime.now()) + ' available links are ' + str(len(url_list)) + \
                    ' and total successful number of clicks - ' + str(counter)
            print(final)
            with open("status.txt", "a") as a_file:
                a_file.write("\n")
                a_file.write(final + "\n")
                write = True
        except:
            time.sleep(20)
        finally:
            if not write:
                final = 'On ' + str(datetime.datetime.now()) + ' available links are ' + str(len(url_list)) + \
                        ' and total successful number of clicks - ' + str(counter)
                with open("status.txt", "a") as a_file:
                    a_file.write("\n")
                    a_file.write(final + "\n")


clickUrls = ClickUrlsAndWait()
clickUrls.test()
