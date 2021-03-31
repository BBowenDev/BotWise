from Classes.ngram import nGram

class Normalizer ():
    def __init__(self):
        self.PUNC_FILTER = "!\"$%&()'*+,-./:;<=>?[\\]^_`{|}~\t\n" #filter does not include # or @
        self.CAP_FILTER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.NUM_FILTER = '1234567890'        
        self.STOP_FILTER = ["a","about","above","after","again","against","all","am","an",
                 "and","any","are","as","at","be","because","been","before","being",
                 "below","between","both","but","by","could","did","do","does","doing",
                 "down","during","each","few","for","from","further","had","has","have",
                 "having","he","hed","hell","hes","her","here","heres","hers","herself",
                 "him","himself","his","how","hows","i","id","ill","im","ive","if","in",
                 "into","is","it","its","its","itself","lets","me","more","most","my",
                 "myself","nor","of","on","once","only","or","other","ought","our",
                 "ours","ourselves","out","over","own","same","she","shed","shell",
                 "shes","should","so","some","such","than","that","thats","the",
                 "their","theirs","them","themselves","then","there","theres","these",
                 "they","theyd","theyll","theyre","theyve","this","those","through","to",
                 "too","under","until","up","very","was","we","wed","well","were","weve",
                 "were","what","whats","when","whens","where","wheres","which","while",
                 "who","whos","whom","why","whys","with","would","you","youd","youll",
                 "youre","youve","your","yours","yourself","yourselves"]
    
    def norm_unicode(self, text):
        token = self.tokenize(text)
        
        for word in token:
            recode = ""
            for char in range(0, len(word)-1):
                recode = ""
                if str(word[char] + word[char+1]) == "\\u":
                    recode = str(word[char] + word[char+1] + word[char+2] + word[char+3] + word[char+4] + word[char+5])
                    break 
            remove = recode
            remove.encode("ascii", "ignore")
            word.replace(recode, remove).replace("b'", "")
        
        return " ".join(token)
    
    def norm_punctuation(self, text):
        token = list(text)
        final = []
        punctuation = nGram()
        
        for pos, char in enumerate(token):
            if char in self.PUNC_FILTER:
                punctuation.append(char, pos)
            else:
                final.append(char)    
            
            #ensure that punctuation is properly disconnected from words
            if (pos != len(token)-1) and (pos > 0):
                if token[pos-1].isalnum() and token[pos+1].isalnum() and not (char.isalnum() or char == " "):
                    token[pos] = token[pos] + " "
                if token[pos] == "@" or token[pos] == "#" and not token[pos-1] == " ":
                    token[pos] = " " + token[pos]
       
        return "".join(final), punctuation

    def norm_numbers(self, text):
        token = list(text)
        number = nGram()
        
        for pos, char in enumerate(token):
            if char in self.NUM_FILTER:
                number.append(char, pos)
        return text, number

    def norm_capitals(self, text):
        token = self.tokenize(text)
        capital = nGram()
        
        for word in token:
            for pos, char in enumerate(word):
                if char in self.CAP_FILTER:
                    capital.append(char, pos)
        
        return " ".join(token).lower(), capital

    def norm_emoji(self, text):
        token = list(text)
        final = []
        emoji = nGram()
        
        for pos, char in enumerate(token):
            if not char.isalnum() and not char in self.PUNC_FILTER and not (char == " " or char == "@" or char == "#"):
                emoji.append(char, pos)
            else:
                final.append(char)
    
        return "".join(final), emoji, len(emoji)
    
    def norm_stop_words(self, text):
        token = self.tokenize(text)
        stopwords = nGram()
        
        for pos, word in enumerate(token):
            if word in self.STOP_FILTER:
                stopwords.append(word, pos)       
        return stopwords 
    
    def norm_hashtags(self, text):
        token = self.tokenize(text)
        final = []
        hashtags = nGram()
        
        for pos, word in enumerate(token):
            if len(word) > 0 and word[0] == "#":
                hashtags.append(word[1:], pos)
            else:
                final.append(word)
        return " ".join(final), hashtags
    
    def norm_link(self, text):
        token = self.tokenize(text)
        final = []
        link = False
        
        for pos, word in enumerate(token):
            if "http" in word:
                link = word
            else: 
                final.append(word)
                
        return " ".join(final), link
        
    def norm_rt(self, text):
        token = self.tokenize(text)
        is_rt = False 
        
        if token[0] == "RT":
            is_rt = True
        
        return " ".join(token), is_rt

    def norm_tagged(self, text):
        token = self.tokenize(text)
        final = []
        tagged = nGram()
        
        for pos, word in enumerate(token):
            if len(word) > 0 and word[0] == "@":
                tagged.append(word[1:], pos)
            else:
                final.append(word)
            
        return " ".join(final), tagged
        

#DRIVER METHODS
    #Tokenize a string 
    def tokenize(self, text):
        return text.split(" ")
    
    #Returns normalized tweet, metadata dict
    def normalize_tweet(self, text):
        normalized_meta = {
            "raw": text, #original tweet
            "normal": "", #normalized tweet
            "length": 0, #length of original tweet
            "words": 0, #number of words in tweet
            "token": [], #tokenized version of tweet before stop words
            "tagged": None, #nGram of tagged accounts
            "emoji": None, #nGram of tweet emoji
            "capitals": None, #nGram of tweet capital letters
            "hashtags": None, #nGram of tweet hashtags
            "punctuaton": None, #nGram of tweet punctuation
            "stopwords": None, #nGram of tweet stop words
            "link": False} #false if no link, string if link 
        
        #tweets are normalized in the order:
        #white spaces, unicode characters, retweet (break if True), links, capital letters, punctuation, 
        #tags, hashtags, emoji, stop words
        
        normalized_meta["normal"] = " ".join(text.split())
        #normalized_meta["normal"] = self.norm_unicode(normalized_meta["normal"])
        normalized_meta["normal"], is_rt = self.norm_rt(normalized_meta["normal"])
        if is_rt:
            return "RT"
    
        normalized_meta["normal"], normalized_meta["link"] = self.norm_link(normalized_meta["normal"])
        normalized_meta["normal"], normalized_meta["capitals"] = self.norm_capitals(normalized_meta["normal"])
        normalized_meta["normal"], normalized_meta["emoji"], num_emoji = self.norm_emoji(normalized_meta["normal"])
        normalized_meta["normal"], normalized_meta["punctuation"] = self.norm_punctuation(normalized_meta["normal"])
        normalized_meta["normal"], normalized_meta["tagged"] = self.norm_tagged(normalized_meta["normal"])
        normalized_meta["normal"], normalized_meta["hashtags"] = self.norm_hashtags(normalized_meta["normal"])
        normalized_meta["length"] = len(normalized_meta["normal"]) + num_emoji #links do not count towards character count, but emoji do
        normalized_meta["token"] = self.tokenize(normalized_meta["normal"])
        normalized_meta["words"] =  len(normalized_meta["token"]) #number of words not including above removals
        normalized_meta["stopwords"] = self.norm_stop_words(normalized_meta["normal"])   
        return normalized_meta
    
    def normalize_bio(self, text):
        normalized_meta = {
            "length": 0,
            "words": 0,
            "captials": None,
            "tags": None,
            "hashtags": None,
            "emoji": None,
            "punctuation": None,
            "stopwords": None}
        
        normal = " ".join(text.split())
        #normal = self.norm_unicode(normal)
        normal, normalized_meta["capitals"] = self.norm_capitals(normal)
        normal, normalized_meta["punctuation"] = self.norm_punctuation(normal)
        normal, normalized_meta["tags"] = self.norm_tagged(normal)
        normal, normalized_meta["hashtags"] = self.norm_hashtags(normal)
        normal, normalized_meta["emoji"], num_emoji = self.norm_emoji(normal)
        normalized_meta["length"] = len(normal) + num_emoji
        normalized_meta["words"] =  len(self.tokenize(normal))
        normalized_meta["stopwords"] = self.norm_stop_words(normal)
        return normalized_meta
    
    def normalize_user_name(self, text):
        normalized_meta = {
            "length": 0,
            "capitals": None,
            "punctuation": None,
            "numbers": None}
        
        normal = text
        normalized_meta["length"] = len(normal) 
        normal, normalized_meta["capitals"] = self.norm_capitals(normal)
        normal, normalized_meta["numbers"] = self.norm_numbers(normal)
        normal, normalized_meta["punctuation"] = self.norm_punctuation(normal)
        return normalized_meta
    
    def normalize_user_display(self, text):
        normalized_meta = {
            "length": 0,
            "capitals": None,
            "punctuation": None,
            "emoji": None}
        
        normal = text
        normal, normalized_meta["capitals"] = self.norm_capitals(normal)
        normal, normalized_meta["emoji"], num_emoji = self.norm_emoji(normal)
        normalized_meta["length"] = len(normal) + num_emoji
        normal, normalized_meta["punctuation"] = self.norm_punctuation(normal)
        return normalized_meta
        

#API CALL NORMALIZER
    def normalize_user_fetch(self, text, JSON=False):
        if JSON:
            data = text
        else:
            data = text["data"][0] 
        
        metrics = data["public_metrics"]
        normal = {}
        
        normal["user_name"] = data["username"]
        normal["user_display"] = data["name"]
        normal["user_bio"] = data["description"]
        normal["followers"] = metrics["followers_count"]
        normal["following"] = metrics["following_count"]
        normal["num_total_tweets"] = metrics["tweet_count"] 
        normal["date"] = data["created_at"][:10]
        
        if "pinned_tweet_id" in data.keys():
            normal["HAS_PINNED"] = True
        else:
            normal["HAS_PINNED"] = False
        
        if "profile_image_url" in data.keys():
            normal["HAS_PROFILE_PIC"] = True
        else:
            normal["HAS_PROFILE_PIC"] = False
        
        if "location" in data.keys():
            normal["HAS_LOCATION"] = True
        else:
            normal["HAS_LOCATION"] = False   
        
        if "url" in data.keys():
            normal["HAS_LINK"] = True
        else:
            normal["HAS_LINK"] = False
        
        return normal

    def normalize_content_fetch(self, text, JSON=False):
        normal = [] #a list of dictionaries containing tweet data
        tweets_raw = {}
        
        if JSON == True:
            tweets_raw = text
       
        elif not "data" in text.keys():
            return "NULL"
       
        else:
            tweets_raw = text["data"]
    
        for tweet in tweets_raw:
            meta = {}
            metrics = tweet["public_metrics"]
            
            meta["raw"] = tweet["text"]
            meta["medium"] = tweet["source"]
            meta["likes"] = metrics["like_count"]
            meta["rts"] = metrics["retweet_count"]
            meta["quotes"] = metrics["quote_count"]
            meta["replies"] = metrics["reply_count"]
            meta["created_at"] = tweet["created_at"][:10] + " " + tweet["created_at"][11:19]
            
            if tweet["lang"] == "und":
                meta["lang"] = "en"
            else:
                meta["lang"] = tweet["lang"]
            
            if "attachments" in tweet.keys():
                if "media_keys" in tweet["attachments"].keys():
                    meta["attachment"] = tweet["attachments"]["media_keys"]
                else:
                    meta["attachment"] = False
            else:
                    meta["attachment"] = False
           
            if "in_reply_to_user_id" in tweet.keys():
                meta["is_reply"] = True
            else:
                meta["is_reply"] = False
            
            normal.append(meta)
            
        return normal