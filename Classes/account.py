from Classes.ngram import nGram
from Classes.normalizer import Normalizer
from Classes.tweet import Tweet
import datetime

class Account ():
    def __init__(self, normal):
        #raw metadata processed by normalizer() from grabber() return 
        self.meta = {
            "user_name": "", #user internal name ("@_____")
            "user_display": "", #user display name
            "user_bio": "", #unedited user bio
            "followers": 0, #number of users following account
            "following": 0, #number of users account follows
            
            "num_total_tweets": 0, #total number of account tweets
            "num_read": 0, #number of tweets captured by API call
            "num_tweets_ngram": 0, #number of tweets ngramized by normalizer() (original tweets)
            
            "num_rts": 0, #number of retweets in API call
            "num_replies": 0, #number of reply tweets in API call
            "num_langs": 0, #total number of primary languages in tweets
            "num_mediums": 0, #total number of platforms used to post tweets
            "num_links": 0, #number of ngramized tweets with links
            "num_attachments": 0, #number of ngramized tweets with attachments
            
            "num_days": 0, #total number of days since account creation
            "HAS_PROFILE_PIC": False, #true if account has profile pic
            "HAS_LINK": False, #true if account has bio link
            "HAS_LOCATION": False, #true if account has listed location
            "HAS_PINNED": False #true if account has pinned tweet    
            }   
        
        #aggregate metadata from tweets
        self.agg_meta = {
            "lengths": [], #total length of each tweet
            "words": [], #total num of words in each tweet
            
            "per_diem": nGram(), #ngram of activity rate by day {"YYYY-MM-DD":0,}
            "days_times": nGram(), #ngram of daily activity rate {"YYYY-MM-DD HH:MM:SS": 0,}
            "mediums": nGram(), #ngram of mediums used to post tweet
            "langs": nGram(), #ngram of languages in tweets
            
            "capitals": nGram(), #ngram of capital letters in tweets
            "stopwords": nGram(), #ngram of stop words in tweets
            "hashtags": nGram(), #ngram of hashtags in tweets
            "tags": nGram(), #ngram of tagged users in tweets
            "punctuation": nGram(), #ngram of punctuation in tweets
            "emoji": nGram(), #ngram of emoji in tweets
            
            "user_bio": {}, #dict of length, capitals, punctuation, emoji, stopwords, tags, hashtags ngrams of bio
            "user_name": {}, #dict of length, capitals ngram, punctuation ngram, numbers ngram of username
            "user_display": {} #dict of length, capitals ngram, punctuation ngram, emoji ngram of display name 
            }
        
        #calcualted meta processed from raw metadata, tweets by account()
        self.calc_meta = {
            "avg_daily": 0.0, #average number of tweets per day
            "follow_ratio": 0, #ratio of followers to following
            "rt_ratio": 0, #ratio of retweets to read tweets
            "reply_ratio": 0, #ratio of replies to read tweets
            "original_ratio": 0, #ratio of original tweets to read tweets
            "link_ratio": 0, #ratio of tweets w/ links
            "attachment_ratio": 0, #ratio of tweets w/ attachments
            
            "per_diem_rate": [], #list of change in num of tweets per day
            "days_between": [], #list of days between days active
            "times_between": [], #list of seconds between tweets
        
            "langs_ratio": [], #list of change in language usage
            "mediums_ratio": [], #list of change in medium usage
            }

        #list of tweet objects
        self.tweets = []
        
        #requirements to establish a new user object
        self.meta["user_name"] = normal["user_name"]
        self.meta["user_display"] = normal["user_display"]
        self.meta["user_bio"] = normal["user_bio"]
        self.meta["followers"] = normal["followers"]
        self.meta["following"] = normal["following"]
        self.meta["num_total_tweets"] = normal["num_total_tweets"]
        self.meta["num_days"] = normal["date"]
        self.meta["HAS_PINNED"] = normal["HAS_PROFILE_PIC"]
        self.meta["HAS_PROFILE_PIC"] = normal["HAS_PROFILE_PIC"]
        self.meta["HAS_LOCATION"] = normal["HAS_LOCATION"]
        self.meta["HAS_LINK"] = normal["HAS_LINK"]
        
    
#METADATA CALCULATION METHODS
    def set_follow_ratio(self):
        #following ratio = followers / following
        
        #prevent division by 0 error by slightly augmenting data
        if self.meta["following"] == 0:
            self.meta["following"] += 1
        
        self.calc_meta["follow_ratio"] = self.meta["followers"] / self.meta["following"]

    def set_days(self):
        old = self.meta["num_days"].split("-")
        start = datetime.date(int(old[0]), int(old[1]), int(old[2]))
        today = datetime.date.today()
        self.meta["num_days"] = (today - start).days

    def set_avg_daily(self):
        if self.meta["num_total_tweets"] == 0:
            self.calc_meta["avg_daily"] = 0.0
        elif self.meta["num_days"] < 1:
            self.calc_meta["avg_daily"] = float(self.meta["num_total_tweets"])   
        else:
            self.calc_meta["avg_daily"] = float(self.meta["num_total_tweets"]) / float(self.meta["num_days"])

    def set_per_diem_rate(self):
        daily = []
        for day in self.agg_meta["days_times"].ngram.keys():  
            daily.append(self.agg_meta["days_times"].ngram[day]["number"]  )
       
        change = []
        for day, num in enumerate(daily):
            if day > 0: 
                change.append(abs(daily[day-1]-num))
                
        self.calc_meta["per_diem_rate"] = change
    
    def set_days_between(self):
        daily = []
        for day in self.agg_meta["per_diem"].ngram:
            daily.append(datetime.datetime.strptime(day, '%Y-%m-%d'))
        
        change = []
        for pos, day in enumerate(daily):
            if pos > 0:
                change.append(abs((daily[pos-1] - day).days))
        self.calc_meta["days_between"] = change
       
    def set_time_ratio(self):
        #dict of days with matching times {"YY-MM-DD": ["HH:MM:SS"]}
        days = {}
        for date_time in self.agg_meta["days_times"].ngram.keys():
            date = date_time.split(" ")
            day = date[0]
            time = date[1]
            
            if day in days.keys():
                days[day].append(time)
            else:
                days[day] = [time]
        
        change = []
        start = datetime.datetime(2006, 3, 1)
        for key in days.keys():
            seconds = [] 
            for pos, time in enumerate(days[key]):
                date = str(key + " " + days[key][pos])
                day = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
                seconds.append((start - day).total_seconds())
            
            difference = []
            for pos, sec in enumerate(seconds):
                if pos > 0:
                    #translate from seconds to hours with / 3600
                    difference.append(abs(seconds[pos-1] - sec) / 3600)
            change += difference
        self.calc_meta["times_between"] = change
        
    def change_ratio(self, gram):
        ratio = []
        
        changes = gram.get_sorted_nums()
        if len(changes) == 1:
            return [0.0]
        
        for pos, entry in enumerate(changes):
            if pos > 0:
                ratio.append(abs(changes[pos-1] - changes[pos]))
        return ratio


#AGGREGATION METHODS
    def aggregate(self, tweets):
        self.set_days()
        self.set_avg_daily() #daily average of tweets
        self.set_follow_ratio() #ratio of followers to following
    
        #agg_meta data aggregation        
        for tweet in self.tweets:
            #append tweet ints
            self.agg_meta["lengths"].append(tweet.meta["length"])
            self.agg_meta["words"].append(tweet.meta["words"])
            
            #append tweet strings
            self.agg_meta["mediums"].append(tweet.meta["medium"])
            self.agg_meta["langs"].append(tweet.meta["lang"])
            self.agg_meta["days_times"].append(tweet.meta["created_at"])
            self.agg_meta["per_diem"].append(tweet.meta["created_at"][:10])
            
            #append tweet ngrams
            self.agg_meta["capitals"].append_all(tweet.meta["capitals"])
            self.agg_meta["stopwords"].append_all(tweet.meta["stopwords"])
            self.agg_meta["hashtags"].append_all(tweet.meta["hashtags"])
            self.agg_meta["tags"].append_all(tweet.meta["tagged"])
            self.agg_meta["punctuation"].append_all(tweet.meta["punctuation"])
            self.agg_meta["emoji"].append_all(tweet.meta["emoji"])
            
            if tweet.meta["link"] != False:
                self.meta["num_links"] += 1
            if tweet.meta["is_reply"] != False:
                self.meta["num_replies"] += 1
            if tweet.meta["attachment"] != False:
                self.meta["num_attachments"] += 1
            
        #additional calc meta requiring aggregation of tweet data 
        self.meta["num_langs"] = len(self.agg_meta["langs"])
        self.meta["num_mediums"] = len(self.agg_meta["mediums"])
        self.calc_meta["reply_ratio"] = float(self.meta["num_replies"] / self.meta["num_read"])
        self.calc_meta["rt_ratio"] = float(self.meta["num_rts"] / self.meta["num_read"])
        self.calc_meta["original_ratio"] = float((self.meta["num_read"] - self.meta["num_rts"]) / float(self.meta["num_read"]))
        self.calc_meta["link_ratio"] = self.meta["num_links"] / self.meta["num_read"]
        self.calc_meta["attachment_ratio"] = self.meta["num_attachments"] / self.meta["num_read"]
        self.calc_meta["langs_ratio"] = self.change_ratio(self.agg_meta["langs"])
        self.calc_meta["mediums_ratio"] = self.change_ratio(self.agg_meta["mediums"])
        self.set_per_diem_rate()
        self.set_time_ratio()
        self.set_days_between()
    
    def aggregate_empty(self):
        self.set_days()
        self.set_follow_ratio() #ratio of followers to following 
        
        #append mandated zeros
        self.calc_meta["avg_daily"] = 0.0
        self.agg_meta["lengths"] = [0]
        self.agg_meta["words"] = [0]
        self.meta["num_langs"] = 0
        self.meta["num_mediums"] = 0
        self.calc_meta["reply_ratio"] = 0.0
        self.calc_meta["rt_ratio"] = 0.0
        self.calc_meta["original_ratio"] = 0.0
        self.calc_meta["link_ratio"] = 0.0
        self.calc_meta["attachment_ratio"] = 0.0
        self.calc_meta["langs_ratio"] = 0.0
        self.calc_meta["mediums_ratio"] = 0.0
        self.calc_meta["per_diem_rate"] = [0]
        self.calc_meta["times_between"] = [0]
        self.calc_meta["days_between"] = [0]
    
    def format_account(self, tweets_raw):
        normalizer = Normalizer()
        
        #preprepare account metadata for aggregation
        self.agg_meta["user_bio"] = normalizer.normalize_bio(self.meta["user_bio"])
        self.agg_meta["user_name"] = normalizer.normalize_user_name(self.meta["user_name"])
        self.agg_meta["user_display"] = normalizer.normalize_user_display(self.meta["user_display"])
        
        if tweets_raw == "NULL":
            self.aggregate_empty()
        
        else:
            tweets_read = len(tweets_raw)
            tweets = []
            rts = 0
            
            for new_tweet in tweets_raw:
                #attempts to normalize tweet text. If retweet, increment retweet count and continue
                #if not retweet, create new Tweet() object, aggregate data, and add to tweets list
                 normalized = normalizer.normalize_tweet(new_tweet["raw"])
                 if normalized != "RT":
                     tweet = Tweet(new_tweet)
                     tweet.aggregate(normalized)
                     tweets.append(tweet)
                 else:
                     rts = rts + 1 
            
            #preprepare tweet stats metadata for aggregation
            self.tweets = tweets
            self.meta["num_tweets_ngram"] = len(tweets)
            self.meta["num_read"] = tweets_read
            self.meta["num_rts"] = rts
            
            #aggregate all account data to finalize account model
            self.aggregate(tweets) 