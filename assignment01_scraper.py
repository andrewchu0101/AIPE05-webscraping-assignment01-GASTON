from project_mangaz import scraper

def main():
	driver = scraper.create_driver()
	url = input("Enter url: ")
	output_folder = input("Enter output folder name:")
	# https://www.mangaz.com/book/detail/157901
	try:
		scraper.open_manga(driver, url)
		scraper.switch_to_reader(driver)
		scraper.capture_pages(driver, output_folder)

	finally:
		driver.quit()


if __name__ == "__main__":
    main()