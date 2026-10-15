from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, ElementClickInterceptedException)
import time

def create_driver():
	options = Options()
	options.add_experimental_option("excludeSwitches", ["enable-automation"])
	options.add_experimental_option("useAutomationExtension", False)
	options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36")
	options.add_argument("--disable-blink-features=AutomationControlled")
	driver = webdriver.Chrome(options=options)
	return driver

def open_manga(driver, url):
	driver.get(url)
	print("Page Title:", driver.title)

	css_selector = 'button.open-viewer.book-begin.ga'
	button = driver.find_element(By.CSS_SELECTOR, css_selector)
	button.click()



def switch_to_reader(driver):
	all_windows = driver.window_handles
	driver.switch_to.window(all_windows[-1])
	Read_Now = driver.find_element(By.PARTIAL_LINK_TEXT,'すぐに読む')
	Read_Now.click()

def capture_pages(driver, output_folder):
	folder_name = output_folder
	os.makedirs(folder_name, exist_ok=True)
	total_image_count = 0
	wait_element = WebDriverWait(driver, 10)
	while True:
		image_elements = driver.find_elements(By.CSS_SELECTOR, 'div.page_image img.image')

		for img_element in image_elements:
			if img_element.is_displayed():
				file_name = f"manga_page_{total_image_count}.png"
				file_path = os.path.join(folder_name, file_name)
				img_element.screenshot(file_path)
				print(f"成功擷取頁面並儲存為: {file_path}")
				total_image_count += 1

		try:
			next_page = wait_element.until(
				EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.flip.flip-left')))

			next_page.click()
			print("已點擊下一頁，等待畫面載入...")

			time.sleep(2)
		except (TimeoutException, ElementClickInterceptedException):
			print("【系統提示】找不到下一頁按鈕，已達最後一頁，結束爬取迴圈。")
			break
