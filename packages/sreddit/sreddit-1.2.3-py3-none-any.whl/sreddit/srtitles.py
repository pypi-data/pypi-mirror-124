from get_chrome_driver import GetChromeDriver
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time

def scrapeMe(channelName, showProgress, keyWords):
    channelName = channelName.lower().replace(" ", "") #make name of reddit channel lowercase and remove any spaces
    get_driver = GetChromeDriver() 
    get_driver.install() #download chromedriver
    #Driver options
    options = Options()
    options.add_argument("--headless") #don't show chromedriver
    options.add_argument("--log-level=3") #me no likey log
    browser = webdriver.Chrome(options=options)
    try:
        browser.get(f"https://www.reddit.com/r/{channelName}") #get the subreddit page
    except:
        print("Invalid channel name")

    #--------------------------------------------------------------------------------------#
    #SCROLLING THE PAGE AND FINDING ELEMENTS
    scrollyNeedsABreak = 0.75 #the amount of time to wait between each scroll (so that page can load)

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    allTitleTexts = [] #list to put title texts in

    if showProgress.lower() == "y" or showProgress.lower() == "yes":
        countTitles = 0 #to keep track of how many titles have been found 
        while True:
            titleTexts = browser.find_elements_by_class_name("_eYtD2XCVieq6emjKBH3m") #find elements of this class
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down to bottom
            for x in range(len(titleTexts)): 
                heading = titleTexts[x].text #get the text version of the title text
                #check to see if the heading already exists
                alreadyExist = allTitleTexts.count(heading)
                if alreadyExist > 0:
                    continue #if it exists we move onnnnn
                else:
                    if len(heading) > 0 and any(word in heading for word in keyWords) == True: #check to make sure the heading actually has content and that a word in it is in the keyword list
                        # print(str(x) + ": "+ heading)
                        countTitles +=1 
                        print(f"Titles Found: {countTitles}", end="\r")
                        allTitleTexts.append(heading) #add heading to list
                    else:
                        continue #if no content in heading and/or the word doesn't show in keywords then we move onnnn
            # Wait to load page
            time.sleep(scrollyNeedsABreak) 

            # Calculate new scroll height and ompare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height: #if it's the same height then we have reached the end of the road
                break
            last_height = new_height
    else:
        while True:
            titleTexts = browser.find_elements_by_class_name("_eYtD2XCVieq6emjKBH3m") #find elements of this class
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);") # Scroll down to bottom
            for x in range(len(titleTexts)): 
                heading = titleTexts[x].text #get the text version of the title text
                #check to see if the heading already exists
                alreadyExist = allTitleTexts.count(heading)
                if alreadyExist > 0:
                    continue #if it exists we move onnnnn
                else:
                    if len(heading) > 0 and any(word in heading for word in keyWords) == True: #check to make sure the heading actually has content and that a word in it is in the keyword list
                        allTitleTexts.append(heading) #add heading to list
                    else:
                        continue #if no content in heading and/or the word doesn't show in keywords then we move onnnn
            # Wait to load page
            time.sleep(scrollyNeedsABreak) 

            # Calculate new scroll height and ompare with last scroll height
            new_height = browser.execute_script("return document.body.scrollHeight")
            if new_height == last_height: #if it's the same height then we have reached the end of the road
                break
            last_height = new_height

    return allTitleTexts

