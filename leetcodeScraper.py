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

# Solution URL: 'https://leetcode.com/problems/' + <question_title_slug> + '/discuss/?currentPage=1&orderBy=hot&query=&tag=' + <program language>
DISCUSS_URL = '/discuss/?currentPage=1&orderBy=most_votes&query=&tag='

class leetcodeScraper:

    def __init__(self, category):
        self.category = category
        self.problems = []

    def getProblemList(self):
        problems_json = requests.get(API_URL + self.category).content
        problems_json = json.loads(problems_json)

        for child in problems_json["stat_status_pairs"]:
            if not child["paid_only"]:
                difficulty = child["difficulty"]["level"]
                question_title_slug = child["stat"]["question__title_slug"]
                question_title = child["stat"]["question__title"]
                frontend_question_id = int(child["stat"]["frontend_question_id"])
                total_acs = child["stat"]["total_acs"]
                total_submitted = child["stat"]["total_submitted"]
                acs_rate = '{0:.3}'.format(int(total_acs) / int(total_submitted) * 100)

                self.problems.append({'difficulty':difficulty, 'frontend_question_id':frontend_question_id, 'question_title':question_title, 'question_title_slug':question_title_slug, 'acs_rate':acs_rate})

        self.problems = sorted(self.problems, key=lambda x: (x['frontend_question_id']))

    def getProblem(self, problem):
        difficulty, frontend_question_id, question_title, question_title_slug, acs_rate = problem['difficulty'], problem['frontend_question_id'], problem['question_title'], problem['question_title_slug'], problem['acs_rate']

        difLevel = {1:'easy', 2:'medium', 3:'hard'}

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
            problem_title_html = f'<div id="title"><b>{frontend_question_id}. {question_title.upper()} (Acceptance Rate: {acs_rate}%)\nQUESTION TITLE SLUG: {question_title_slug}\nDIFFICULTY: {difLevel[difficulty].upper()}\n</b></div>\n' 
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
            print(f'[-] Error Occurred: {e}')
            driver.quit()
            return None

    def getSolution(self, question_title_slug, language):
        validLanguages = ['python', 'c', 'java', 'python-3', 'cpp']

        if language not in validLanguages:
            return None

        url = PROBLEM_URL + question_title_slug + DISCUSS_URL + language

        try:
            driver.get(url)

            # Wait 20 secs or until div with id initial-loading disappears
            element = WebDriverWait(driver, 20).until(
                EC.invisibility_of_element_located((By.ID, "initial-loading"))
            )

            # get current tab page source 
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")

            solutionLink_html = soup.find("a", {"class": "title-link__1ay5"}, href=True)
            if solutionLink_html:
                solutionLink = solutionLink_html["href"]
                url = "https://leetcode.com" + solutionLink

                driver.get(url)

                # Wait 20 secs or until div with id initial-loading disappears
                element = WebDriverWait(driver, 20).until(
                    EC.invisibility_of_element_located((By.ID, "initial-loading"))
                )
                
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                solution_html = soup.find("div", {"class": "discuss-markdown-container"})
                
                soup = BeautifulSoup(solution_html.encode(encoding="utf-8"), features="html.parser")

                question_title = question_title_slug.replace('-', ' ').upper()
                solution = question_title + ' SOLUTION (' + language.replace('-', ' ') + ')\n\n' + soup.get_text()

                return solution 
                
        except Exception as e:
            print(f'[-] Error Occurred: {e}')
            driver.quit()
            return None

    # def downloadSolution(self, solutionLink):
        # url = 'https://leetcode.com' + solutionLink

        # try:
            # driver.get(url)

            # # Wait 20 secs or until div with id initial-loading disappears
            # element = WebDriverWait(driver, 20).until(
                # EC.invisibility_of_element_located((By.ID, "initial-loading"))
            # )

            # # get current tab page source
            # html = driver.page_source
            # soup = BeautifulSoup(html, "html.parser")

            # solution_html = soup.find("div", {"class": "discuss-markdown-container"})

            # soup = BeautifulSoup(solution_html.encode(encoding="utf-8"), features="html.parser")
            # return soup.get_text()

        # except Exception as e:
            # print(f'[-] Error Occurred: {e}')
            # driver.quit()
            # return None
