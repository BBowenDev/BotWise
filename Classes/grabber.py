import requests, json, time

class Grabber ():
    def __init__(self):
        TW_TOKEN_BEARER = ""
        self.headers = self.create_headers(TW_TOKEN_BEARER)
        self.wait_num = 0 
    
    def create_content_url(self, id_num):
        #QUERY DETERMINES WHAT CONTENT IS RETURNED AND FROM WHERE
            #query, start_time, end_time, since_id, until_id, max_results,
            #next_token, expansions, tweet.fields, media.fields, poll.fields,
            #place.fields, user.fields
        
        #TWEET FIELDS DETERMINE WHAT METADATA IS RETURNED [CSV LIST]
            # attachments, author_id, context_annotations,
            # conversation_id, created_at, entities, geo, id,
            # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
            # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
            # source, text, and withheld
        tweet_fields = "tweet.fields=public_metrics,created_at,text,in_reply_to_user_id,source,lang,attachments"
        max_num = "max_results=25" #maximum number of tweets to be returned [between 5 and 100]
        url = "https://api.twitter.com/2/users/{}/tweets?{}&{}".format(id_num, tweet_fields, max_num)
        return url
    
    def create_user_url(self, username):
        #USERNAME- 1 OR MORE IN CSV
        query = "usernames={}".format(username)
        
        #USER FIELDS DETERMINE WHAT METADATA IS RETURNED [CSV LIST]
            # created_at, description, entities, id, location, name,
            # pinned_tweet_id, profile_image_url, protected,
            # public_metrics, url, username, verified, and withheld
        user_fields = "user.fields=created_at,description,id,location,name,pinned_tweet_id,profile_image_url,public_metrics,url,username"
        
        #"user.fields=public_metrics,description,location,pinned_tweet_id"
        
        url = "https://api.twitter.com/2/users/by?{}&{}".format(query, user_fields)
        return url
    
    def create_check_url(self, id_nums):
        url = "https://api.twitter.com/2/users?ids={}".format(id_nums)
        return url
    
    def create_headers(self, bearer_token):
        headers = {"Authorization": "Bearer {}".format(bearer_token)}
        return headers
    
    def connect_to_endpoint(self, url):
        response = requests.request("GET", url, headers=self.headers)
        
        #if API times out grabber()
        if response.status_code == 429:
            self.wait_num += 1
            print("-->", url)
            print("WAITED", self.wait_num*960, "SEC")
            time.sleep(960)
            response = requests.request("GET", url, headers=self.headers)
        elif not response.status_code == 200 and not response.status_code == 429:
            print("-->", url)
            raise Exception(response.status_code, response.text)
            
        return response.json()
    
    
#TWITTER CONTENT DRIVER
    def grab_content(self, id_num):
        url = self.create_content_url(id_num)
        return self.connect_to_endpoint(url)
        
    def user_lookup(self, username):
        url = "https://api.twitter.com/2/users/by?usernames={}".format(username)
        return self.connect_to_endpoint(url)["data"][0]["id"]
    
#TWITTER USER DRIVER
    def grab_user(self, username):
        url = self.create_user_url(username)
        return self.connect_to_endpoint(url)
    
    def grab_check(self, id_nums):
        url = self.create_check_url(id_nums)
        return self.connect_to_endpoint(url)