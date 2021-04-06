class Tweet ():
    def __init__(self, normal_data):
        self.meta =  meta = {
            "raw": "", #unedited text from API call 
            "normal": "", #final, normalized text
            "created_at": "", #string of date "YYYY-MM-DD HH:MM:SS"
            "token": None, #tokenized list of normalized tweet 
            "tagged": None, #ngram of tagged users
            "stopwords": None, #ngram of stop words
            "hashtags": None, #ngram of hashtags
            "emoji": None, #ngram of emoji
            "capitals": None, #ngram of capital letters
            "punctuation": None, #ngram of punctuation
            "medium": "", #medium used to post tweet
            "lang": "", #language used in tweet
            "length": 0, #length in char of tweet
            "words": 0, #length in words of tweet
            "likes": 0, #num likes on tweet
            "rts": 0, #num retweets of tweet
            "quotes": 0, #num quote retweets of tweet
            "replies": 0, #num replies to tweet
            "is_reply": False, #True if tweet is reply
            "link": False, #False if no link, string if link
            "attachment": False #False if no attachment, media key string if attachment
            }
    
        self.meta["raw"] = normal_data["raw"]
        self.meta["lang"] = normal_data["lang"]
        self.meta["medium"] = normal_data["medium"]
        self.meta["likes"] = normal_data["likes"]
        self.meta["rts"] = normal_data["rts"]
        self.meta["quotes"] = normal_data["quotes"]
        self.meta["replies"] = normal_data["replies"]
        self.meta["attachment"] = normal_data["attachment"]
        self.meta["created_at"] = normal_data["created_at"]
        self.meta["is_reply"] = normal_data["is_reply"]
    
#Set Methods
    def aggregate(self, normal):
        self.meta["normal"] = normal["normal"]
        self.meta["length"] = normal["length"]
        self.meta["words"] = normal["words"]
        self.meta["token"] = normal["token"]
        self.meta["tagged"] = normal["tagged"]
        self.meta["emoji"] = normal["emoji"]
        self.meta["capitals"] = normal["capitals"]
        self.meta["hashtags"] = normal["hashtags"]
        self.meta["punctuation"] = normal["punctuation"]
        self.meta["stopwords"] = normal["stopwords"]
        self.meta["link"] = normal["link"]
        
   