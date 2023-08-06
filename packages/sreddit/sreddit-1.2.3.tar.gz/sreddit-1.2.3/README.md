# SubRedditScraper
#### *Python package for scraping user-inputted subreddits*

## **MODULES**

MODULES | WHAT THEY DO
------------ | -------------
**srtitles** | <ol><li>Navigates to given subreddit</li><li>Scrapes titles of posts</li><li>Scrolls down, and repeats until it reaches the end of the page</li><li>Returns list of all titles found</li><li>_Will eventually put list in a database you can then export._</li></ol>
**srcontent** | Coming soon

<br>

## **USAGE**
### _srtitles_

```python
from sreddit import srtitles
subRedditName = "name of a subreddit"
showProgress = "Yes" #if you don't want to show progress then you can leave string blank
keyWords = ['word', 'wordTwo','wordThree'] #to only gather titles with one or more of these keywords in it. you can leave the list blank ['']
listOfTitles = srtitles.scrapeMe(subRedditName, showProgess, keyWords)
print(listOfTitles)
```





