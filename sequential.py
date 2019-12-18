import requests
from bs4 import BeautifulSoup
import time

#Class that represents a URL that has been previously scored
class scoredUrl:
    #Initializes with the URL and score as well as an array representation of the URL's text
    def __init__(self, url, score):
        self.url = url
        self.score = score
        self.articleArray = self.getAsArray(url)

    #Given a URL will return an array representation of the paragraph text present in the article
    #Removes HTML, JS, and CSS scripts as well as any empty lines. Comments shared with main 
    def getAsArray(self, url):
        response = requests.get(url)
        responseText = response.text.encode('UTF-8')
        soup = BeautifulSoup(response.text, "html.parser")
        s = soup.find_all('p')
        string1 = str(s)
        arrayS = string1.split(' ')
        arrayS = [word.replace('<p', '').replace('</p>', '').replace('<code>', '').replace('</code>', '')
            .replace('class=', '').replace('href=', '').replace('>', '').replace('<p', '')
            .replace('\"', '').replace('\"', '').replace(',','') for word in arrayS]
        arrayS = list(filter(None, arrayS))
        return arrayS
    
    #Get method for object URL
    def getUrl(self):
        return self.url

    #Get method for object score
    def getScore(self):
        return self.score

    #Get the array representation of the URL's text
    def getList(self):
        return self.articleArray

#firstArticle - user article as an array
#secondArticle - another article to be compared with
def compare(firstArticle, secondArticle):
    totalCounter = float(len(secondArticle)) #total length of the second article serving as the comparison 
    matchCounter = 0.0 #initialize a counter of the amount of times words have matched in the article
    for i in firstArticle: #loops through all the words in the first article
        for j in secondArticle: #loops through all the words in the second article
            if j == i: #words match
                matchCounter = matchCounter + 1 #increment the amount of matches
    return matchCounter / totalCounter #retuns a percentage of matches


if __name__ == "__main__":
    #start = time.time() #starts time
    userUrl = 'https://www.nytimes.com/2018/06/10/world/canada/g-7-justin-trudeau-trump.html' 
    response = requests.get(userUrl) #scrapes the url 

    responseText = response.text.encode('UTF-8') #encodes the web scraping
    
    soup = BeautifulSoup(response.text, "html.parser") #parses
    
    s = soup.find_all('p') #returns all paragraph text within the URL

    string1 = str(s) #stringifys the paragraph text
    
    arrayS = string1.split(' ') #makes the string into an array

    #replaces all HTML, CSS and JS scipts and tags
    arrayS = [word.replace('<p', '').replace('</p>', '').replace('<code>', '').replace('</code>', '')
        .replace('class=', '').replace('href=', '').replace('>', '').replace('<p', '')
        .replace('\"', '').replace('\"', '').replace(',','') for word in arrayS]

    arrayS = list(filter(None, arrayS)) #filters empty elements

    article1 = scoredUrl('https://www.foxnews.com/media/trudeau-johnson-macron-appear-to-be-mocking-trump-at-nato-summit-in-surfaced-video', 6.5)
    article2 = scoredUrl('https://www.nbcnews.com/politics/donald-trump/trump-calls-trudeau-two-faced-after-hot-mic-catches-nato-n1095351', 8.0)
    article3 = scoredUrl('https://www.dailymail.co.uk/news/article-7753821/Justin-Trudeau-Emmanuel-Macron-Boris-Johnson-caught-appearing-gossip-Trump.html', 5.0)
    article4 = scoredUrl('https://www.theguardian.com/us-news/2019/dec/04/trump-describes-trudeau-as-two-faced-over-nato-hot-mic-video', 7.0)
    article5 = scoredUrl('https://abcnews.go.com/Politics/trudeau-washington-move-past-feud-trump-lobby-usmca/story?id=63820427', 6.0)
    article6 = scoredUrl('https://www.usatoday.com/story/news/politics/2018/11/01/trade-wars-canada-not-ready-forgive-trumps-insulting/1648045002/', 8.5)
    article7 = scoredUrl('https://www.scmp.com/news/world/article/2150067/trump-tweets-he-instructed-us-representatives-not-endorse-g7-joint', 2.4)
    article8 = scoredUrl('https://thehill.com/homenews/administration/472972-trump-caught-on-hot-mic-criticizing-media-talking-about-two-faced', 9.0)

    articleList = [article1, article2, article3, article4, article5, article6, article7, article8]
    
    totalTime = 0 
    runs = 100
       
    while runs > 0: 
    	start = time.time()
	firstMostSimilar = 0 #most similar article percentage
    	firstMostName = None #article object that has the highest percentage
    	secondMostSimilar = 0 #second most similar article
    	secondMostName = None #article object for the article with the second highest percentage

    	for i in articleList: #loops through the articles in the comparison list
        	n = compare(arrayS, i.getList()) #calls the compare method for the user URL and the current article from the list
        	if n > firstMostSimilar: #if the compare percentage is greater than the first most similar
            		if firstMostSimilar > secondMostSimilar: 
                		secondMostSimilar = firstMostSimilar #second gets the values of the first 
                		secondMostName = firstMostName 
            		firstMostSimilar = n #first gets the values of the current iteration
            		firstMostName = i
        	#print("Article ", articleList.index(i) + 1, " -- ", n, "% similar") #print article index and similarity
        averageScore = (firstMostName.getScore() + secondMostName.getScore()) / 2 #computes average
        #print("User article average rating of:",averageScore) 
  
        end = time.time() #ends time
        totalTime = totalTime + (end - start)
        runs = runs - 1 
        #print(end - start) #prints time difference

    print(totalTime/100)	



