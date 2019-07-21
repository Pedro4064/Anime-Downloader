# Anime Downloader
 Download both anime series and movies from  [twist.moe](https://twist.moe/) as .mp4 using python3.7 and Selenium webDriver


 ![alt text](https://raw.githubusercontent.com/Pedro4064/Anime-Downloader/master/Images/Main%20Screen.png)

## Python Modules
  •To install all modules, run: 
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

  •Change the `driverPath = '/Applications/chromedriver'` to fit the location of the webDriver on your system.<br/>
  •When you are prompted with the mode you wish the code to run in, just press enter. If an error occurs, please try again, but this time enter `iota` as the mode.<br/>
  •Sometimes you are prompted with an error message at the end of runtime. First check if the movie/series was really downloaded before retrying, it may return an error but still have downloaded the media correctly.<br/>
  •If you are on a Windows machine, you will have to change the `os.system('clear')` to `os.system('cls')`


  
