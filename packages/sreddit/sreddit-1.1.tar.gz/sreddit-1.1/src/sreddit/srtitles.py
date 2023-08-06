from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time


def scrapeMe(channelName):
    channelName = channelName.lower().replace(" ", "") #make name of reddit channel lowercase
    #Don't show the chromedriver.
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--log-level=3")
    browser = webdriver.Chrome(chrome_options=options)
    try:
        browser.get(f"https://www.reddit.com/r/{channelName}") #get the reddit channel page
    except:
        print("Invalid channel name")
    #--------------------------------------------------------------------------------------#
    #CALCULATING HOW MANY TIMES WE NEED TO SCROLL THE SUBREDDIT
    scrollyNeedsABreak = 0.75 #the amount of time to wait between each scroll (so that page can load)

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(scrollyNeedsABreak)
        # Calculate new scroll height. compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    titleTexts = browser.find_elements_by_class_name("_eYtD2XCVieq6emjKBH3m") #find all the post title elements on the page
    numToScroll = (len(titleTexts)) // 10 #divide the number of titletexts by 10 (typically 10 posts a page before needing to scroll)
    # print(numToScroll)

    #--------------------------------------------------------------------------------------#
    #GATHERING TITLE TEXTS
   
    allTitleTexts = [] #empty list to later append titles
    for y in range(numToScroll):
        for x in range(len(titleTexts)):
            heading = titleTexts[x].text
            alreadyExist = allTitleTexts.count(heading)
            if alreadyExist > 0:
                continue #continue on if the heading is already in allTitleTexts
            else:
                if len(heading) > 0: 
                    # print(str(x) + ": "+ heading)
                    allTitleTexts.append(heading) #append heading to allTitleTexts
                else:
                    continue #continue on if the title is empty
        browser.execute_script("window.scrollTo(0,document.body.scrollHeight)") #scroll down the page
        time.sleep(0.6)
    
    return allTitleTexts

