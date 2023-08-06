# SubRedditScraper
## *Python package for scraping user-inputted subreddits*

### **MODULES**

MODULES | WHAT THEY DO
------------ | -------------
**srtitles** | <ul><li>Takes user input as a subreddit name Navigates to subreddit</li><li>Loads the entire page (since reddit uses infinte scrolling)</li><li>Scrapes titles of posts and returns them in a list</li><li>_Will eventually put list in a database you can then export._</li></ul>
**srcontent** | Coming soon

<br>

### **HOW TO USE:**
### _srtitles_

```python
from sreddit import srtitles
subRedditName = "name of a subreddit"
listOfTitles = srtitles.scrapeMe(subRedditName)
print(listOfTitles)
```
<b>N.B -</b> Put chromdriver.exe in the same folder as your code in order to run the modules, and some subreddits have a lot of pages and it takes time for each page to load for infinite scrolling... Get a cup of tea in the meanwhile <3.




