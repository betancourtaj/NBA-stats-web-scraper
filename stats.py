from bs4 import BeautifulSoup
import requests
import csv
from time import sleep, time
from constants import Teams


from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import TimeoutException

class Scrape_Stats(object):
	""" Scrapes www.stats.nba.com """
	def __init__(self, season):
		""" season should be formated like the following: 2016-17.
			month should be fomatted like the following if the month is january: 01
			day should be fomatted like the following if the day is the 2nd: 02
		"""



		"""https://stats.nba.com/players/boxscores-traditional/?Season=2017-18&SeasonType=Regular%20Season&DateFrom=01%2F19%2F2018&DateTo=01%2F19%2F2018"""
		self.season = season
		self.players = []
		self.sources = []

		profile = webdriver.FirefoxProfile()
		options = Options()
		options.add_argument("--headless")

		self.driver = webdriver.Firefox(firefox_options=options)

		self.explicit_wait = 6

	def scrape_season(self):

		index = 1

		while index < 8:

			url = f"https://stats.nba.com/players/boxscores-traditional/?Season={self.season}&SeasonType=Regular%20Season&Month={index}"

			self.driver.get(url)
			print("starting")
			wait = WebDriverWait(self.driver, self.explicit_wait)
			skip = False

			try:
				self.driver.find_element_by_link_text('No statistics are currently available for the selected filters.')
				skip = True
			except:
				print("continuing ")

			if skip == False:
				wait.until(EC.presence_of_all_elements_located((By.XPATH, "//div[@class='stats-table-pagination__info']/select")))
				#self.driver.find_element_by_xpath("//div[@class='stats-table-pagination__info']/select").click()
				#self.driver.find_element_by_link_text("All").click()
				#element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='stats-table-pagination__info']/select/option[0]")))
				#sleep(2)
				#self.driver.find_element_by_xpath("//div[@class='stats-table-pagination__info']/select/option[@label='All']")
				s1 = Select(self.driver.find_element_by_xpath("//div[@class='stats-table-pagination__info']/select"))
				s1.select_by_visible_text('All')

				sleep(7)

				wait.until(EC.presence_of_all_elements_located((By.XPATH, "//table/tbody/tr[278]")))

				print("Found players")

				self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

				res = self.driver.execute_script("return document.documentElement.outerHTML")

				self.sources.append(res)

				print("done")

			else:

				print("page skipped")

			index = index + 1

		self.driver.quit()


	def parse_html(self):
		for source in self.sources:
			soup = BeautifulSoup(source, 'lxml')

			table = soup.find(class_='nba-stat-table__overflow')

			index = 0
			for row in table.find_all('tr'):
				all_table_data = []
				if index != 0:
					for table_data in row.find_all('td'):
						temp = ""
						temp = table_data.text
						if len(temp) != 0 and temp != "" and table_data.text != None:
							all_table_data.append(temp)

					player_name = all_table_data[0]
					team_name = all_table_data[1]
					match_up = all_table_data[2]
					game_date = all_table_data[3]
					W_and_L = all_table_data[4]
					minutes = all_table_data[5]
					points = all_table_data[6]
					fgm = all_table_data[7]
					fga = all_table_data[8]
					fg_percent = all_table_data[9]
					threepm = all_table_data[10]
					threepa = all_table_data[11]
					threep_percent = all_table_data[12]
					ftm = all_table_data[13]
					fta = all_table_data[14]
					ft_percent = all_table_data[15]
					oreb = all_table_data[16]
					dreb = all_table_data[17]
					reb = all_table_data[18]
					ast = all_table_data[19]
					stl = all_table_data[20]
					blk = all_table_data[21]
					tov = all_table_data[22]
					pf = all_table_data[23]
					plus_minus = all_table_data[24]

					player = [player_name, team_name, match_up, game_date, W_and_L, minutes, points, fgm, fga, fg_percent, threepm, threepa, threep_percent,
								ftm, fta, ft_percent, oreb, dreb, reb, ast, stl, blk, tov]
					self.players.append(player)
				index = index + 1


	def write_to_file(self):
		with open('players.csv', 'a',  newline='') as csv_file:

			for player in self.players:
				fieldnames = ['player_name','team_name', 'match_up', 'game_date', 'W_and_L', 'minutes', 'points', 'fgm', 'fga', 'fg_percent', 'threepm', 'threepa',
								'threep_percent', 'ftm', 'fta', 'ft_percent', 'oreb', 'dreb', 'reb', 'ast', 'stl', 'blk', 'tov', 'pf', 'plus_minus']
				writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

				print(player[0])
				print(player[1])
				print(player[2])
				print(player[3])
				print(player[4])
				print(player[5])
				print(player[6])
				print(player[7])
				print(player[8])
				print(player[9])
				print(player[10])
				print(player[11])
				print(player[12])
				print(player[13])
				print(player[14])
				print(player[15])
				print(player[17])
				print()
				print()

				writer.writerow({ 'player_name': player[0], 'team_name': player[1], 'match_up': player[2], 'game_date': player[3], 'W_and_L': player[4], 'minutes': player[5], 'points': player[6], 'fgm': player[7], 'fga': player[8],
					'fg_percent': player[9], 'threepm': player[10], 'threepa': player[11], 'threep_percent': player[12], 'ftm': player[13], 'fta': player[14], 'ft_percent': player[15], 'oreb': player[16], 'dreb': player[17], 'reb': player[18],
					'ast': player[19], 'stl': player[20], 'blk': player[21], 'tov': player[22]})

	def scrape_within_range_of_dates(self, date1, date2):
		pass

	def scrape_day(self):
		pass

	def scrape_current_day(self):
		pass

	def run(self):
		self.scrape_season()
		self.parse_html()
		self.write_to_file()



scrape = Scrape_Stats("2015-16")
scrape.run()


