from selenium import webdriver
import pandas as pd
from bs4 import BeautifulSoup
from csv import DictWriter
from time import sleep

# Adding driver
driver = webdriver.Chrome("./chromedriver")
# Pagination Initilization
BASE_URL = "https://www.naukri.com/full-stack-jobs"

def scrape_jobs():
	# List for storing scrapped data
	job_list = []
	# Hard-coded pagination (for 10 pages)
	for i in range(1,11):
		print("Now scrapping " + BASE_URL + "-" + str(i) + "...")
		# Getting the page
		driver.get(BASE_URL + "-" + str(i))
		# Individual jobs present in class='jobTuple'
		all_jobs = driver.find_elements_by_class_name('jobTuple')
		# Getting individual attributes iteratively
		for job in all_jobs:
			result_html = job.get_attribute('innerHTML')
			soup = BeautifulSoup(result_html, "html.parser")
			try:
				title = soup.find("a", class_="title").text.replace('\n','')
			except:
				title = 'None'
			try:
				location = soup.find("i", class_="naukicon-location").find_next_sibling().text.replace('\n','')
			except:
				location = 'None'
			try:
				company = soup.find("a", class_="subTitle").text.replace('\n','')
			except:
				company = 'None'
			try:
				salary = soup.find("i", class_="naukicon-rupee").find_next_sibling().text.replace('\n','')
			except:
				salary = 'None'
			try:
				experience = soup.find("i", class_="naukicon-experience").find_next_sibling().text.replace('\n','')
			except:
				experience = 'None'
			try:
				description = soup.find("div", class_="job-description").text.replace('\n','')
			except:
				description = 'None'
			try:
				keywords = soup.find("ul", class_="tags has-description").text.replace('\n','')
			except:
				keywords = 'None'
			try:
				if(soup.find("i", class_="naukicon-hot-jobs").find_next_sibling().text.replace('\n','') == "HOT JOB"):
					trending = 1
			except:
				trending = 0
			try:
				if(soup.find("i", class_="naukicon-premium").find_next_sibling().text.replace('\n','') == "PREMIUM"):
					sponsored = 1
			except:
				sponsored = 0

			''' For detailed description
			sum_div = soup.find("a", class_="title")["href"]
			sum_div = job.find_elements_by_class_name("job-description")[0]
			sum_div.click()
			job_desc = driver.find_elements_by_class_name("dang-inner-html").text '''

			# Adding attributes to the 'job_list' iteratively
			job_list.append({
				"title": title,
				"location": location,
				"company": company,
				"salary": salary,
				"experience": experience,
				"description": description,
				"keywords": keywords,
				"trending": trending,
				"sponsored": sponsored
				})

		''' For dynamic pagination
		next_btn = driver.find_element_by_css_selector('a.fright')
		url = next_btn.get_attribute('href') if next_btn else None '''
		sleep(6)

	return job_list

# Function to write into csv
def write_jobs_to_csv(jobs):
	with open("fullstack_dev.csv", "w") as file:
		headers = ["title", "location", "company", "salary", "experience", "description", "keywords", "trending", "sponsored"]
		csv_writer = DictWriter(file, fieldnames=headers)
		csv_writer.writeheader()
		for job in jobs:
			csv_writer.writerow(job)

jobs = scrape_jobs()
write_jobs_to_csv(jobs)

