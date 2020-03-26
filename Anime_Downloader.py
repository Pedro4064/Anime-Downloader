import os
import time
import sys
import requests
from tqdm import tqdm
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
# from concurrent.futures import ThreadPoolExecutor
import threading


class Moe(webdriver.Chrome,webdriver.chrome.options.Options,webdriver.common.by.By,webdriver.support.ui.WebDriverWait):

    def __init__(self, driverPath:str = '/usr/local/bin/chromedriver'):

        # Added the headless option 
        self.options = webdriver.chrome.options.Options()
        self.options.add_argument('--headless')
        self.options.add_argument('--headless')
        self.options.add_argument('--no-sandbox')
        self.options.add_argument('--disable-gpu')

        # Initialize the web driver
        self.driver = webdriver.Chrome(driverPath,options=self.options)

        # The wait for elements config -> 10 seconds
        self.wait = webdriver.support.ui.WebDriverWait(self.driver,10)

        # Main twist Mow url 
        self.mainURL = 'https://twist.moe'
  
    def __format_data(referers,raw_urls,episode_numbers):

        formatte_data = [{'episode_number':episode_number,'referer':referer, 'raw_url': raw_url} for episode_number,referer,raw_url in zip(episode_numbers,referers,raw_urls)]

        return formatte_data

    def get_raw_urls(self, url:'The anime url', nEpisodes:'The number of episodes it will try to get the url from'):

        urls = []
        rawUrls = []
        episode_numbers = []

        
        # Go to the url
        self.driver.get(url)

        # Check to see if it is a movie or a series, they have different xPaths
        try:

            # wait for the first element to appear, if there is an element it is a series, set the firstItem as an xPath for series
            firstItem = '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li[2]/a'
            ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, firstItem)))

        except:

            try:
                # Since it is not a series it must be a movie, set the firstItem xPath to match that of a movie
                print('Trying to get the url of a movie...')
                firstItem = '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li/a'
                
                ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, firstItem)))
        
            except:
                # It can be a yota case, so set the correct xpath
                print('Trying to get the url for yota...')
                firstItem = '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li[1]/a'
                
                ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, firstItem)))
        
        time.sleep(3)


        # Search for urls - starting from the 1st url on page
        for i in range(1,nEpisodes+2):

            try:

                # find and append the url in a list
                url = self.driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li[%d]/a' %(i)).get_attribute('href')
                urls.append(url)
            
                if __name__ == '__main__':
                    print(url)

            except:

                if i !=1:
                    break
                else:
                    continue
                
        
        print()
        print()
        
        #  Go to each url and get the raw url 
        for episode_number,url in enumerate(urls):

            try:

                # go to the url
                self.driver.get(url)
                

                # wait for the first item to load
                ok = self.wait.until(webdriver.support.expected_conditions.visibility_of_element_located((webdriver.common.by.By.XPATH, firstItem)))
                time.sleep(5)
             
                
                # get the raw URL
                rawUrl = self.driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/section/div/div/video').get_attribute('src')
                rawUrls.append(rawUrl)
                episode_numbers.append(episode_number)

                if __name__ == '__main__':
                    print(rawUrl)

            except Exception as e:
                print(e)

        # return two lists, one with the mp4 urls and another with their respective 'referers'
        print()
        print()

        return [{'episode_number':episode_number,'referer':referer, 'raw_url': raw_url} for episode_number,referer,raw_url in zip(episode_numbers,urls,rawUrls)]

    def finish(self):

        # close the webdriver
        self.driver.quit()

    

# Functions that will be used to instantiate and interact with user on terminal
anime_name = ''
main_link = ''
number_of_episodes = ''
episodes_data = []
progress_bars = []
first_episode = ''
last_episode = ''

def logo():
    os.system('clear')

    print("  _____                      _                 _                  _                \n |  __ \\                    | |               | |     /\\         (_)               \n | |  | | _____      ___ __ | | ___   __ _  __| |    /  \\   _ __  _ _ __ ___   ___ \n | |  | |/ _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |   / /\\ \\ | '_ \\| | '_ ` _ \\ / _ \\\n | |__| | (_) \\ V  V /| | | | | (_) | (_| | (_| |_ / ____ \\| | | | | | | | | |  __/\n |_____/ \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_(_)_/    \\_\\_| |_|_|_| |_| |_|\\___|")

    print('\n')
    print('\n')

def end_logo():

    komi = """⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣤⣤⣶⣶⣶⣶⣶⣦⣤⣤⣄⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣴⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡴⣻⣽⣿⣿⣿⣿⣿⣿⡿⣿⣿⡿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⡾⠋⣸⣿⣿⣿⣿⣿⣿⠟⠁⢀⣿⣿⡀⣟⣿⣿⣿⠿⣿⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣴⢋⣾⣾⣿⣿⣯⡿⣽⡟⠁⠀⠀⠘⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣼⣿⣿⣿⣿⣿⣿⠿⠿⣿⣿⣷⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠃⣾⣿⣿⣿⣿⣿⣿⠏⠀⠀⠀⠀⠀⠙⣟⢿⣿⣿⣿⣿⣿⣿⡌⠿⣿⣿⣿⣿⣿⡷⣦⣄⢹⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
    All Done!!!!            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣿⣿⣿⣿⣿⣿⣿⠏⠀⡠⠖⠛⠉⠉⠙⠛⠦⠀⠈⠙⠛⠛⠿⠛⠛⠉⠉⠛⠛⢿⣧⠘⣿⣿⣿⡏⡀⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⣿⣿⣿⣿⣿⡟⠀⠞⠀⢀⣴⣿⣿⣶⡄⠀⠀⠀⠀⠀⠀⠀⢠⣶⣿⣿⣶⡀⠀⠹⡄⢸⣿⣿⣿⣿⠃⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠩⠛⢿⣿⣿⣇⠀⠀⠀⢸⣿⣿⣿⣿⣿⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⡇⠀⠀⠀⠀⣿⣿⣿⡁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢹⣿⣿⡏⠁⠀⠀⠀⠙⠛⠛⠛⠁⠀⠀⠀⠀⠀⠀⠀⡈⠙⠛⠛⠋⠀⠀⠀⠀⠀⠈⣠⣄⠀⡆⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⣼⣿⣿⡇⠀⠀⠀⠁⠒⠀⠀⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠐⠀⠀⠒⠈⠀⠀⠀⠀⣐⠀⠁⢀⠇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⠛⠊⣀⠞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣶⠋⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣦⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣴⣿⡿⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣿⣿⣿⣿⣶⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣤⣶⣿⣿⣿⡇⣿⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣤⡄⠀⠀⠀⣠⣤⣶⣾⣿⣿⣿⣿⣿⣿⡿⢃⢸⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣤⣄⡿⠁⣿⠛⣿⣿⣿⣿⣿⣿⣿⡇⠀⠀⠀⣿⣿⣿⣿⣿⣿⣿⣛⣻⣏⣁⢸⠸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⡇⣸⣿⣿⣿⣿⣿⣿⣿⡟⠁⡇⠀⠀⠀⣿⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣾⡄⢇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⣿⣿⣧⣿⣿⣿⣿⠿⠿⢛⠏⠀⠀⠸⡀⠀⢠⠇⠀⠀⠹⡛⠻⠿⣿⣿⣿⣿⣿⣷⠸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⠛⠋⠉⠀⠀⠀⡌⠀⠀⠀⠀⠳⣀⠏⢀⠀⠀⠀⢱⠀⠀⠀⠈⠉⠛⣿⣿⡆⢧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣿⣿⣿⣧⠂⠀⠀⠀⠀⣜⡠⣴⣶⢥⣍⠲⡋⠒⣡⣼⣳⢢⣄⣣⠀⠀⠀⠀⠀⠘⣿⣷⢸⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⣿⣿⣿⣿⡘⡀⠀⠀⠀⢠⢣⢣⢿⣏⣞⣿⣹⡿⣽⣻⣻⣣⢻⡇⠀⠀⠀⢠⠁⠀⢹⣿⣾⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣿⣿⣿⣿⣿⠷⠥⡀⠀⠀⠘⡞⡎⡞⣟⡿⡟⠉⢿⣷⣣⢧⢻⣻⠁⠀⠀⢀⠂⠀⠀⠀⣿⣿⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀"""

    print(komi)

def user_interface():

    global anime_name
    global number_of_episodes
    global first_episode
    global last_episode
    global main_link

    os.system('clear')
    logo()

    #Prompt the user for information
    anime_name     = input('•The name of the anime you wish to download->')
    main_link  = input('•The link for the first episode->')
    first_episode = input('•The episode you want to start the download from (enter ⏎ if you want to start from the first one) - ')
    last_episode = input('•The last episode you want download (enter ⏎ if you want to download up until the last one) - ')

def get_anime_data():

    global main_link
    global episodes_data
    global first_episode
    global last_episode

    # Instatiate the Moe class
    moe = Moe()

    # Get the referers and raw urls for the anime
    episodes_data = moe.get_raw_urls(url=main_link, nEpisodes=1000)

    # Format the list to contain only the episodes the user wants to download
    # Try to transform the input data to int, if it fails the user typed enter and it will downlaod from the start
    try :

        first_episode = int(first_episode)
        episodes_data = episodes_data[first_episode-1:]

    except:

        # If the user wants to download from the first episode, don't change the list
        episodes_data = episodes_data

    # Try to transform the input data  for last_episode to int, if it fails the user typed enter and it will downlaod until the last episode
    try:

        last_episode = int(last_episode)
        episodes_data = episodes_data[:last_episode]

    except:

        # If the user wants to download until the last episode, don't change the list
        episodes_data = episodes_data

def create_progress_bars():
    global episodes_data
    global progress_bars

    progress_bar_number = len(episodes_data) - 1
    
    # Create a list containing tqdm objects (progress bars)
    for episode_data in episodes_data:
        
        # Set up the session config, make the get request and check the size of the file
        session = requests.Session()
        session.headers.update({'referer':episode_data['referer']})
        response = session.get(episode_data['raw_url'], stream=True)
        content_size = int(response.headers['Content-Length'])

        # Create a progress bar object and add to the dict
        progress_bar = tqdm(total = content_size, position = progress_bar_number)
        episode_data['progress_bar'] = progress_bar
        
        # Update the progress bar number
        progress_bar_number-=1

def download_episode():

    global episodes_data
    global anime_name

    # check if the list is empty (if it is,all episodes were already downloaded, return None)
    if len(episodes_data) == 0:
        return None  

    # Get the data 
    episode_data = episodes_data[0]
    # print(episode_data)

    # Remove that episode_data from the list of episodes so other threads don't download the same episode
    episodes_data = episodes_data[1:]

    # Change to the correct directory 
    os.chdir('/animes')


    ######## start download sequence ########
     # Set up the session config
    session = requests.Session()
    session.headers.update({'referer':episode_data['referer']})

    # Make the get request
    response = session.get(episode_data['raw_url'], stream=True)

    # Format the file name
    file_name = anime_name+'_'+str(episode_data['episode_number'])+'.mp4'


    # Create the file and open it in Write binary mode
    with open(file_name,'wb') as video_file:

        # Go over the blocks of the response to avoid holding everything in memory
        for chunk in response.iter_content(512):
            
            # Write to file
            video_file.write(chunk)

            # update the progress bar
            episode_data['progress_bar'].update(512)

    # When it finishes, use recursion to call itself again and download another episode
    download_episode()


if __name__ == "__main__":
    
    logo()
    user_interface()
    get_anime_data()
    create_progress_bars()

    # Create up to 5 Threads (number of episodes downloaded concurrently)
    if len(episodes_data) >= 5:
        number_of_pools = 5
    else:
        number_of_pools = len(episodes_data)

    # with ThreadPoolExecutor(max_workers=number_of_pools) as excecutor:

    threads = []

    for i in range(number_of_pools):

        # Start each thread
        threads.append(threading.Thread(target=download_episode))
        threads[i].start()


    for thread in threads:

        thread.join()
