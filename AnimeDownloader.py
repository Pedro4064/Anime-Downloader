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
referers = []
aName = ''
mainLink = ''
nEpisodes = 0
directory = '/animes'
driverPath = '/usr/local/bin/chromedriver'
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

def GatherLinks(parameter):

    global episodeLinks
    global rawLinks
    global referers
    global aName
    global mainLink
    global nEpisodes
    global direcotry
    global driverPath
    global xPath
    global starEpisode

    #Add the headless option
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    #Specifies the location of the webDriver (path as global variable)
    driver = webdriver.Chrome(options=options)

    #Go to the mainLink, gather all the episode links and append them to the episodeLinks list
    driver.get(mainLink)
    time.sleep(7)

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

        # Goes link by link to get the raw .mp4 link
        linkNumber = 1

        for link in episodeLinks:

            # If the episode number is less than the starEpisode number(which by default is 1) go to next link, else extract the raw link
            if linkNumber <starEpisode:
                
                # Update the link number and print to notify the user that it will skip the episodes 
                print("Skiping",linkNumber,"episode")
                linkNumber+=1
                continue
            
            # Extrect the raw link
            else:
                driver.get(link)
                time.sleep(5) #Wait 5 seconds for the page to finish loading

                # append the episode link to be used as referer in the get request
                referers.append(link)

                # Append the mp4 file url
                rawLinks.append(driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/section/div/div/video').get_attribute('src'))
                print(driver.find_element_by_xpath('//*[@id="__layout"]/div/div[1]/section/div/div/video').get_attribute('src'))
                
                linkNumber+=1

    except:

        print(colored('[ERROR] Make user you inserter the correct number of episodes, if the error continues change the mode of the code(type "iota" when you are prompted for the mode)'))

def Download():

    global rawLinks
    global referers
    global aName
    global nEpisodes
    global directory
    global userName
    global password
    global starEpisode

    # Set the episode number to the starEpisode(passed as an argument to start the download from)->If no argument is passed, the startEpisode = 1
    # So the program won't rewrite another episode and will name the .mp4 file correctly
    episodeNumber = starEpisode
    os.chdir(directory)

    progressBar = IncrementalBar('Episodes Downloaded', max = len(rawLinks))



    #Tries to download, but if fails print an error message
    try:

        for link,referer in zip(rawLinks,referers):

            # Set up the session config
            session = requests.Session()
            session.headers.update({'referer':referer})

            # print('referer:',referer)
            # print('raw:',link)

            done = False
            while done == False:
                # Make a request to the url
                response = session.get(link)
                
                fileName = aName+'_'+str(episodeNumber)+'.mp4'
                

                # Create the .mp4 file and write binary content
                with open(aName+'_'+str(episodeNumber)+'.mp4','wb') as videoFile:

                    videoFile.write(response.content)

                # Check to see the size of the file, if it is too small and error happened
                if os.path.getsize(fileName) < 10000:
                    done = False
                    print(os.path.getsize(fileName))
                else:
                    done = True


                # Update the episode number for namming purposes, and update the progress bar
            episodeNumber+=1
            progressBar.next()

    except:
        print(colored('[ERROR] While downloading the episodes ','red'))

def Movie():

    global driverPath
    global direcotry

    xPathMovie = '//*[@id="__layout"]/div/div[1]/section/div/div/video'

    os.system('clear')

    Logo()
    print(colored('Movie program being executed ...\n','green'))
    #Prompt the user for aditional information
    pageLink = input('•The link for the anime movie->')
    name = input('•The name of the movie you are downloading-> ')

    #Add the headless option
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')

    #Specifies the location of the webDriver (path as global variable)
    driver = webdriver.Chrome(options=options)

    #gathers the link for the mp4 file and then goes to it
    driver.get(pageLink)
    time.sleep(6)

    link = driver.find_element_by_xpath(xPathMovie).get_attribute('src')
    #Changes to the correct directory and then star the download
    os.chdir(direcotry)

    done = False

    while done == False:
        with open(name+'.mp4','wb') as movie:
            print('raw:',link)
            print('referer:',pageLink)
            # Set up the session config for the get request
            session = requests.Session()
            session.headers.update({'referer':pageLink})
            response = session.get(link)

            movie.write(response.content)

        
        # Check to see the size of the file, if it is too short an error happened, so try again
        fileName = name+'mp4'
        
        if os.path.getsize(fileName) < 10000:
            print(os.path.getsize(fileName))
            done = False
        else:
            done = True
    quit()

def Logo():
    os.system('clear')

    print("  _____                      _                 _                  _                \n |  __ \\                    | |               | |     /\\         (_)               \n | |  | | _____      ___ __ | | ___   __ _  __| |    /  \\   _ __  _ _ __ ___   ___ \n | |  | |/ _ \\ \\ /\\ / / '_ \\| |/ _ \\ / _` |/ _` |   / /\\ \\ | '_ \\| | '_ ` _ \\ / _ \\\n | |__| | (_) \\ V  V /| | | | | (_) | (_| | (_| |_ / ____ \\| | | | | | | | | |  __/\n |_____/ \\___/ \\_/\\_/ |_| |_|_|\\___/ \\__,_|\\__,_(_)_/    \\_\\_| |_|_|_| |_| |_|\\___|")

    print('\n')
    print('\n')

def EndLogo():

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

if __name__ == '__main__':

    #Clear the variables
    episodeLinks = []
    rawLinks = []
    aName = ''
    mainLink = ''
    nEpisodes = 0
    starEpisode = 1
    driverPath = '/Applications/chromedriver'
    xPath = '//*[@id="__layout"]/div/div[1]/section/main/div[2]/div[3]/ul/li[%s]/a'

    userName = ''
    password = ''

    # Check if any parameters were passed 
    if len(sys.argv) != 1:
        
        # If the argument passed is -h, desplay a walkthrough message
        if sys.argv[1] == '-h':
            Logo()
            print(colored('You may start the download from any episode, just pass the number of such episode as an argument','yellow'))
            print(colored('ex: python3.X AnimeDownloader.py 13 ----> It will start the download from episode 13','yellow'))
            quit()

        # If the argument passed is not -h, check if it was a number 
        try:

            # the starEpisode will be the parameter passed
            starEpisode = int(sys.argv[1])

            #If the argument is a number, prompt the user for the mode in which the program should run
            Logo()
            mode = input('In which mode should the code run (enter for normal mode)?')
            
            #If the argument is a number, prompt the user for information
            Logo()
            print(colored("Program will download starting from "+str(starEpisode)+"\n","green"))

            aName     = input('•The name of the anime you wish to download->')
            mainLink  = input('•The link for the first episode->')
            nEpisodes = int(input('•The number of episodes in the series->'))
            directory = input('•The directory you want the save the episodes->')

            # Go to the download process
            GatherLinks(mode)
            Download()

            # print the final logo
            EndLogo()

            
        # If not a number, print an error massage and quit the program
        except Exception as e:
            print(e)
            print(colored("The argument passed was neither -h (for info) nor a number (to start the download from)","red"))
            quit()
    
    # If no argument is passed
    else:
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
