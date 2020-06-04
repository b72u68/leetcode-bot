import subprocess
import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

# Setup Selenium Webdriver
CHROMEDRIVER_PATH = r'./driver/chromedriver.exe' 
options = Options()
options.headless = True
# Disable Warning, Error and Info logs
# Show only fatal errors
options.add_argument("--log-level=3")
driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, options=options)

# Leetcode API URL to get json file
API_URL = 'https://leetcode.com/api/problems/'

# Problem URL: 'https://leetcode.com/problems/' + '{problem title}'
PROBLEM_URL = 'https://leetcode.com/problems/'

class leetcodeScaper:

    def __init__(self, category, difficulty):
        self.category = category
        self.difficulty = difficulty
        self.problems = []

    def getProblemList(self):
        problems_json = requests.get(API_URL + self.category).content
        problems_json = json.loads(problems_json)

        for child in problems_json["stat_status_pairs"]:
            if not child["paid_only"] and child["difficulty"]["level"] == self.difficulty:
                question_title_slug = child["stat"]["question__title_slug"]
                question_title = child["stat"]["question__title"]
                frontend_question_id = child["stat"]["frontend_question_id"]
                total_acs = child["stat"]["total_acs"]
                total_submitted = child["stat"]["total_submitted"]
                acs_rate = '{0:.2f}'.format(int(total_acs) / int(total_submitted) * 100)

                self.problems.append((frontend_question_id, question_title, question_title_slug, acs_rate))

        self.problems = sorted(self.problems, key=lambda x: (x[3]))

        return self.problems

    def downloadProblem(self, problem):
        frontend_question_id, question_title, question_title_slug, acs_rate = problem
        url = PROBLEM_URL + question_title_slug

        try:
            driver.get(url)

            # Wait 20 secs or until div with id initial-loading disappears
            element = WebDriverWait(driver, 20).until(
		EC.invisibility_of_element_located((By.ID, "initial-loading"))
	    )

            # Get current tab page source
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            # Construct HTML
            problem_title_html = f'<div id="title"><b>{frontend_question_id}. {question_title.upper()} (Acceptance Rate: {acs_rate}%)</b></div>\n' 
            problem_html = problem_title_html + str(soup.find("div", {"class": "content__u3I1 question-content__JfgR"})) + '<br><br><hr><br>'
            
            # # Append Contents to a HTML file
            # with open("out.html", "wb") as f:
                # f.write(problem_html.encode(encoding="utf-8"))
                # f.close()

            # html = open("out.html", "r")
            soup = BeautifulSoup(problem_html.encode(encoding="utf-8"), features="html.parser")
            return soup.get_text()

            # print('\n[+] Converting HTML file to image')
            # subprocess.run("./htmltoimage/wkhtmltoimage.exe out.html out.png")
            # print('[+] File converted successfully')

        except Exception as e:
            print(f'Error Occurred: {e}')
            driver.quit()
            return None
