# Install and Activate Packages
install.packages("RCurl")
install.packages("ROAuth")
install.packages("RJSONIO")
install.packages("stringr")
install.packages("streamR")

library(streamR)
library(RCurl)
library(RJSONIO)
library(stringr)

# Set directory to save data
## Provide the inputs
path_filesaving = "/home/ubuntu/happyplaces/newyork/streaming" # Please provide the path to save all the data
setwd(path_filesaving)

# The City of New York,
loc_tw = "New York" # city name
loc_tw_bx = c(-74.262714,40.492848,-73.693046,40.919761) # lon_min, lat_min, lon_max, lat_max


# PART 1: Declare Twitter API Credentials & Create Handshake
library(ROAuth)
requestURL <- "https://api.twitter.com/oauth/request_token"
accessURL <- "https://api.twitter.com/oauth/access_token"
authURL <- "https://api.twitter.com/oauth/authorize"

## Please provide your consumerKey and comsumerSecret from dev.twitter.com

#HapplyPlaces13
#Add the consumer key, secret; accesstoken, accesstoken secret
consumerKey <- "XXXXX" 
consumerSecret <- "XXXXX" 
accessToken <- "XXXXX" 
accessTokenSecret <- "XXXXX" 

my_oauth <- createOAuthToken(consumerKey, consumerSecret, accessToken, accessTokenSecret)

### STOP HERE!!! ###

# PART 2: Save the my_oauth data to an .Rdata file
save(my_oauth, file = "my_oauth.Rdata")

library(streamR)
load("my_oauth.Rdata")
filterStream(file.name = "tweets.json", # Save tweets in a json file
             track = c(""), 
             # Collect tweets mentioning keywords
             #language = "en",
             timeout = 60, 
             # Keep connection alive for 60 seconds
             oauth = my_oauth) # Use my_oauth file as the OAuth credentials


library(streamR)
load("my_oauth.Rdata")

merge.data<- write.csv("1.csv", fileEncoding = "UTF-8")   #create an initial data

while(1)
# 3 (testing) or 168 (collecting for 7 days)
{Flag = FALSE
	Result = tryCatch(
	{
		min=as.numeric(  format(Sys.time(), "%M"))
		sec=as.numeric(  format(Sys.time(), "%S"))
		diff=3600-60*min-sec

		filterStream(file.name = "tweets.json", # Save tweets in a json file
					 track = c(""), # Collect tweets mentioning keywords
					 #language = "en",
					 location = loc_tw_bx,
					 # latitude/longitude pairs providing southwest and northeast corners of the bounding box.
					 timeout = diff, 
					 # Keep connection alive for 60 seconds (testing) or 3600 seconds (collection)
					 verbose = TRUE,
					 # Generates some output to the R console with information about the capturing process.
					 oauth = my_oauth) # Use my_oauth file as the OAuth credentials


		tweets.df <- parseTweets("tweets.json") 
		
		}, error = function(err){
		
			file.remove("tweets.json")
			Flag <<- TRUE
			
	
		})
		if(Flag){
      
      next
    }
#parse the json file and save to a data frame called tweets.df. Simplify = FALSE 
#ensures that we include lat/lon information in that data frame.

datatime = format(Sys.time(),"%Y%m%d%H%M")
file_name = paste0("tweets_",loc_tw,"_",datatime,".csv", collapse = NULL)
write.csv(tweets.df, file=file_name, fileEncoding = "UTF-8")

file.remove("tweets.json")   #delete the last hour data
}