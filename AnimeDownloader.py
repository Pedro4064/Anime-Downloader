import os
import time
import sys
import requests
from termcolor import colored
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from progress.bar import IncrementalBar




episodeLinks = []
rawLinks = []
aName = ''
mainLink = ''
nEpisodes = 0
directory = ''
driverPath = '/Applications/chromedriver'
xPath = '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li[%s]/a'

userName = 'pedro4064'
password = 'P3dr0twistmoe'

def User():

    global episodeLinks
    global aName
    global mainLink
    global nEpisodes
    global directory

    os.system('clear')

    Logo()
    #Prompt the user for information
    aName     = input('•The name of the anime you wish to download->')
    mainLink  = input('•The link for the first episode->')
    nEpisodes = int(input('•The number of episodes(or the number you want to download)->'))
    directory = input('•The directory you want the save the episodes->')

def GatherLinks(parameter):

    global episodeLinks
    global rawLinks
    global aName
    global mainLink
    global nEpisodes
    global direcotry
    global driverPath
    global xPath

    #Add the headless option
    options = Options()
    options.add_argument('--headless')

    #Specifies the location of the webDriver (path as global variable)
    driver = webdriver.Chrome(options=options, executable_path=driverPath)

    #Go to the mainLink, gather all the episode links and append them to the episodeLinks list
    driver.get(mainLink)
    time.sleep(5)

    print('\n')
    print('Link for all the desired episodes: ')

    constant = 1

    #Checks to see which mode should the code run in (the xPath in darling in the franxx starts at 2, not one)
    if parameter == "iota":

        constant = 2
        print(colored('Iota program running . . . ','green'))

    for i in range(nEpisodes):

        i+=constant #Change to 1 or to 2 deppending on the anime (senko-san is 1, but darling in the franxx in 2)
        episodeLinks.append(driver.find_element_by_xpath(xPath %(i)).get_attribute('href'))
        print(driver.find_element_by_xpath(xPath %(i)).get_attribute('href'))

    print('\n')
    print('Link for all the .mp4 files in the server: ')

    try:

        for link in episodeLinks:

            driver.get(link)
            time.sleep(5) #Wait 5 seconds for the page to finish loading


            rawLinks.append(driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/section/div/div/video').get_attribute('src'))
            print(driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/section/div/div/video').get_attribute('src'))

    except:

        print(colored('[ERROR] Make user you inserter the correct number of episodes, if the error continues change the mode of the code(type "iota" when you are prompted for the mode)'))

def Download():

    global rawLinks
    global aName
    global nEpisodes
    global directory
    global userName
    global password

    episodeNumber = 1
    os.chdir(directory)

    progressBar = IncrementalBar('Episodes Downloaded', max = len(rawLinks))



    #Tries to download, but if fails it's because the authentication failed, so redirect the user to the Settings pag e
    try:
        for link in rawLinks:


            response = requests.get(link, auth = (userName,password))
            with open(aName+'_'+str(episodeNumber)+'.mp4','wb') as videoFile:

                videoFile.write(response.content)

            episodeNumber+=1
            progressBar.next()
    except:
        print(colored('[ERROR] While downloading the episodes ','red'))


def Movie():

    global driverPath

    xPathMovie = '//*[@id="__layout"]/div/div[1]/section/div/div/video'

    os.system('clear')

    Logo()
    print(colored('Movie program being executed ...\n','green'))

    #Prompt the user for aditional information
    pageLink = input('•The link for the anime movie->')
    direcotry = input('•The directory you wish to save the movie in-> ')
    name = input('•The name of the movie you are downloading-> ')

    #Add the headless option
    options = Options()
    options.add_argument('--headless')

    #Specifies the location of the webDriver (path as global variable)
    driver = webdriver.Chrome(options=options, executable_path=driverPath)

    #gathers the link for the mp4 file and then goes to it
    driver.get(pageLink)
    time.sleep(6)

    link = driver.find_element_by_xpath(xPathMovie).get_attribute('src')
    #Changes to the correct directory and then star the download
    os.chdir(direcotry)

    with open(name+'.mp4','wb') as movie:
        print(link)
        response = requests.get(link, auth = ('pedro4064','P3dr0twistmoe'))
        movie.write(response.content)

    quit()

def Logo():
    os.system('clear')

    print("  _____                      _                 _                  _                \n |  __ \\                    | |               | |     /\\         (_)               \n | |  | | _____      ___ __ | | ___   __ _  __| |    /  \\   _ __  _ _ __ ___   ___ \n | |  | |/ _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |   / /\\ \\ | '_ \\| | '_ ` _ \\ / _ \\\n | |__| | (_) \\ V  V /| | | | | (_) | (_| | (_| |_ / ____ \\| | | | | | | | | |  __/\n |_____/ \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_(_)_/    \\_\\_| |_|_|_| |_| |_|\\___|")

    print('\n')
    print('\n')



while True:

    #Clear the variables
    episodeLinks = []
    rawLinks = []
    aName = ''
    mainLink = ''
    nEpisodes = 0
    directory = ''
    driverPath = '/Applications/chromedriver'
    xPath = '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li[%s]/a'

    userName = ''
    password = ''

    try:

        Logo()

        print('1. Series')
        print('2. Movie')

        answer  = input('-> ')
        if answer == '1':

            os.system('clear')
            mode = input('In which mode should the code run (enter for normal mode)?')
            User()
            GatherLinks(mode)
            Download()

        elif answer == '2':
    
            Movie()


        else:
            quit()

        again = input('\nAgaing ?')
        if again.casefold() == 'n':
            quit()



    except Exception as e:
        print(e)
        print(colored('[ERROR] Someting happend along the way, please try again. If the problem continues try with another anime and poset an issue on the github page'))
        print(colored('https://github.com/Pedro4064/AnimeDownloader','yellow'))
