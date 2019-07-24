# Anime Downloader
 Download both anime series and movies from  [twist.moe](https://twist.moe/) as .mp4 using python 3(or later) and Selenium webDriver
 

 ![alt text](https://raw.githubusercontent.com/Pedro4064/Anime-Downloader/master/Images/Main%20Screen.png)

## Python Modules
  •To install all modules run: <br/>
   `python -m pip install -r /path/to/requirements.txt`
### Preinstalled  
  •os<br/>
  •time<br/>
  •sys<br/>
  •requests<br/>
### Needs to be installed separately  
  •[termcolor](https://pypi.org/project/termcolor/)<br/>
  •[selenium](https://pypi.org/project/selenium/)<br/>
  •[progress](https://pypi.org/project/progress/)<br/>

## Chrome Driver

  •You also need to download [chromedriver](http://chromedriver.chromium.org/downloads) to use with selenium module.<br/> 
  *If you are on the raspberry pi, follow this [instructions](https://www.reddit.com/r/selenium/comments/7341wt/success_how_to_run_selenium_chrome_webdriver_on/). <br/>
## Notes
  •You may start the download from any episode, and not just the first one, by passing the episode number as an argument:<br/>
  `python3.x AnimeDonwloader.py 13` -> and it will start the download from the 13th episode<br/>
  •Change the `driverPath = '/Applications/chromedriver'` to fit the location of the webDriver on your system.<br/>
  •When you are prompted with the mode you wish the code to run in, just press enter. If an error occurs, please try again, but this time enter `iota` as the mode.<br/>
  •If you are on a Windows machine, you will have to change the `os.system('clear')` to `os.system('cls')`

