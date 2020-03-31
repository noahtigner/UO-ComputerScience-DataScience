##Install the required R packages: 1) twitteR: a package that provides an interface to the Twitter web API; 2) tm: a package for text mining; 3) wordcloud: a package for plotting word clouds, and 4) RColorBrewer, a package for creating color palettes. You can run ?? + package name to have a closer look at these packages; 5)
install.packages(c("twitteR","tm","wordcloud","RColorBrewer","ggmap", "leaflet"),dependencies = TRUE)

##Tip: You can highlight a line of code and click Run button to run the code. Alternatively, you can use the shortcut Ctrl + Enter. 

##Load the required packages
library(twitteR)
library(tm)
library(wordcloud)
library(RColorBrewer)
library(ggmap)
library(leaflet)

##Set the keys and token generated for your own app
#consumer.key <- "u55DBTTqoQX2afxY3gfVttkg9"
#consumer.secret <- "4yj85cDbWIS0HSVqXWvTB00lMro0IBVRAlZ5RHxoQwc5andfmg"
#access.token <- "406769652-PGXnBHQzDlS8mjEfHok2KdPYot8PFCG1YP6pmmVH"
#access.secret <- "4B3esMIOmwd41INEtopJ4SyTPEw0iGCQzivXmaK6U0ZwW"

#setup_twitter_oauth(consumer_key = consumer.key, consumer_secret = consumer.secret, access_token = access.token, access_secret = access.secret)

# Part I: Exploring the University of Oregon's Twitter account act --------

# ##Retrieve the Tweets from user "uoregon", which is University of Oregon's official Twitter account
# tweets.uo <- userTimeline("uoregon",n=3200)
# 
# ##Convert tweets list to a data.frame
# tweets.uo.df <- twListToDF(tweets.uo)

##Read the csv containing the Tweets posted by University of Oregon's official Twitter account, which were retrieved by Dr. Henry Luan on Feb 11, 2019 @3:20pm
## Change the file path to where you store your CSV file
# tweets.uo.df <- read.csv("Tweets_UO_Feb11_19.csv",stringsAsFactors = FALSE)  
# 
# ##Transform the character to Time 
# tweets.uo.df$created <- as.POSIXct(tweets.uo.df$created)
# ##Transform the numeric to character
# tweets.uo.df$replyToSID <- as.character(tweets.uo.df$replyToSID)
# tweets.uo.df$id <- as.character(tweets.uo.df$id)
# tweets.uo.df$replyToUID <- as.character(tweets.uo.df$replyToUID)
# 
# ##Retrieve the dimensions of the uo data.frame
# dim(tweets.uo.df)
# dim(tweets.uo.df)[2]
# ##Retrieve the column names of the data.frame
# colnames(tweets.uo.df)
# ##Obtain the class of the first column values
# class(tweets.uo.df[,1])
# 
# ##Obtain a subset of the Tweets in December, 2018
# tweets.uo.subset <- subset(tweets.uo.df, created >= as.POSIXct('2018-12-01 00:00:00') & created <= as.POSIXct('2019-01-31 23:59:59'))
# ##Get the number of Tweets in December, 2018
# dim(tweets.uo.subset)[1]
# 
# ##Get the number of likes and retweet counts of the third Tweet
# tweets.uo.subset[12,"favoriteCount"]
# tweets.uo.subset[12,"retweetCount"]
# 
# ##Build a corpus for the text from tweets.uo.subset
# ## Corpus: a collection of written texts. For example, it can be the entire works of a particular author or a body of writing on a particular subject. In our context, corpus is a collection of the content in those posted Tweets.
# corpus.uo <- Corpus(VectorSource(tweets.uo.subset$text))
# ##Remove punctuations from the Tweets
# corpus.uo <- tm_map(corpus.uo, removePunctuation)
# ##Remove numbers from the Tweets
# corpus.uo <- tm_map(corpus.uo, removeNumbers)
# ##Remove Emoji from the Tweets
# ## Learn more about regular expression at: https://rstudio-pubs-static.s3.amazonaws.com/74603_76cd14d5983f47408fdf0b323550b846.html
# removeEmoji <- function(x) {
#   gsub("\\p{So}|\\p{Cn}", "", x, perl = TRUE)
# }
# corpus.uo <- tm_map(corpus.uo, content_transformer(removeEmoji))
# 
# ##Remove Special character from the Tweets
# removeSpecialChar <- function(x){
#   gsub("[^[:alnum:]///' ]", "", x)
# }
# corpus.uo <- tm_map(corpus.uo, content_transformer(removeSpecialChar))
# ##Convert to lower case
# corpus.uo <- tm_map(corpus.uo, content_transformer(tolower))
# ##Remove the stopwords in English from the Tweets
# ##Stopwords: Most common words used in a language
# corpus.uo <- tm_map(corpus.uo, removeWords, stopwords("english"))
# 
# ##Remove extra whitespace; multiple whitespace characters are collapsed to a single blank
# corpus.uo <- tm_map(corpus.uo, stripWhitespace)
# ##Remove URLs
# removeURL <- function(x){
#   gsub("http[^[:space:]]*","",x)
# }
# corpus.uo <- tm_map(corpus.uo, content_transformer(removeURL))
# 
# ##Convert the corpus to a term document matrix, which gives the frequency of terms that occur in a collection of documents
# tdm.uo <- TermDocumentMatrix(corpus.uo, control = list(wordLengths=c(1,Inf)))
# 
# ##Convert the term document matrix to a matrix
# ## rows: number of different words in the corpus
# ## columns: number of Tweets retrieved
# matrix.uo <- as.matrix(tdm.uo) 
# 
# ## Calculate the frequency of each word in all the Tweets in a decreasing order
# word.freq.uo <- sort(rowSums(matrix.uo), decreasing = TRUE)
# ##The number of unique words in the corpus 
# length(word.freq.uo)
# ## The first element of word.freq.uo shows the most frequent word and times repeated
# word.freq.uo[1]
# 
# ## Plot the word cloud of UO's Tweets
# wordcloud(words=names(word.freq.uo), freq = word.freq.uo, min.freq = 4, random.order = FALSE, colors = brewer.pal(9, "Greens")[-(1:4)])


# Part II: Retrieving geo-tagged Tweets related to Flu ------------------
# tweets.flu <- searchTwitter("flu", since = "2019-02-09", until="2019-02-10", geocode = "44.0521,-123.0868,1000km", n=10000)

## Instead of using the function searchTwitter, we read the csv file uploaded in Canvas. 
tweets.snowstorm.df <- read.csv("Tweets_Snowstorm_Feb11_19.csv",stringsAsFactors = FALSE)
##Transform the character to Time 
tweets.snowstorm.df$created <- as.POSIXct(tweets.snowstorm.df$created)
##Transform the numeric to character
tweets.snowstorm.df$replyToSID <- as.character(tweets.snowstorm.df$replyToSID)
tweets.snowstorm.df$id <- as.character(tweets.snowstorm.df$id)
tweets.snowstorm.df$replyToUID <- as.character(tweets.snowstorm.df$replyToUID)

##Extract the data between Feb 09 and Feb 10, 2019
tweets.snowstorm.df <- subset(tweets.snowstorm.df, created >= as.POSIXct('2019-02-09 00:00:00') & created <= as.POSIXct('2019-02-10 23:59:59'))

##Remove the Tweets without latitude and longitude coordinates
tweets.snowstorm.df <- subset(tweets.snowstorm.df,longitude != "NA")

##Using leaflet to map the flu data
leaflet(data=tweets.snowstorm.df) %>%
  addTiles() %>%
  addCircleMarkers(lng = ~longitude, lat=~latitude,color="red",radius = 10, stroke = T, fillOpacity = 0.8)



