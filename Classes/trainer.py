from Classes.account import Account
from Classes.tweet import Tweet
from Classes.packager import Packager
from Classes.normalizer import Normalizer
from Classes.grabber import Grabber

class Trainer ():  
    def __init__(self, train_list, max_num=700, API=True):
        self.train_list = train_list + ".tsv"
        self.max_num = max_num
        self.USE_API = API

        #JSON data frame has format:
        """
        [{"user_name": "", 
          "user_id": "",
          "account_data": {},
          "tweet_data": {}
          },
        ]
        """
        self.json_data = []
        
    def build(self):
        #Create packager to input, store, and output data
        packager = Packager("train_set")
        
    #set to True if API should be used, False if pulling from existing data
        if self.USE_API:
            #import training list of accounts
            trainlist = open(self.train_list, "r")
            lines = trainlist.readlines()
            
            #For each account in train_list, grab and aggregate data
            trainnum = 0
            for acct in lines:
                try:    
                    
                    if trainnum == self.max_num:
                        break
                    
                    #format and split raw account info
                    data_raw = acct.replace("\n", "").split("\t")
                    acct_raw = data_raw[0]
                    id_raw = data_raw[1]
                    
                    #reset objects to clear previous data
                    grabber = Grabber()
                    normalizer = Normalizer()
                    
                    #grabber() calls API, normalizer() frames API data, account() creates new account with data
                    #if account is inaccessible, ignore and print error
                    user_data = grabber.grab_user(acct_raw)
                    if "errors" in user_data.keys():
                        print(acct_raw + "--", user_data["errors"][0]["detail"])
                        continue 
                    
                    #append raw data to JSON data and normalize to account
                    json_data = {"user_name": acct_raw, "user_id": id_raw, "accunt_data": user_data["data"][0], "tweet_data": {}}
                    account = Account(normalizer.normalize_user_fetch(user_data))
                    
                    #grabber() calls API, normalizer() frames API data, returns dictionary metadata list
                    #if content is inaccessible, ignore and print error
                    content_data = grabber.grab_content(id_raw)
                    if "errors" in content_data.keys():
                        print(acct_raw + "--", content_data["errors"][0]["detail"])
                        continue
                    elif content_data["meta"]["result_count"] == 0:
                        print(acct_raw + "--", "insuf tweets")
                        continue
                
                    #if data capture is successful, increment number of trained accounts
                    trainnum += 1
                    
                    #append raw JSON data, save to object, and normalize to tweet list
                    json_data["tweet_data"] = content_data["data"]                    
                    self.json_data.append(json_data)
                    tweets_raw = normalizer.normalize_content_fetch(content_data)

                    #prepare tweet profile and auxiliary metadata, aggregate all account data to finalize account model
                    account.format_account(tweets_raw)
                    
                    #package and store account data in packager()
                    packager.store(account)
                    
                    #output raw JSON data for later use
                    jPackager = Packager("json_train_data", filetype="json")
                    jPackager.package_json(self.json_data)
                    continue
            
            #rather than have errors crash the training process, just skip that account and continue
                except Exception as e:
                    print(acct_raw + "--", e)
                    continue 
            #package all account data
            packager.package_all() 
        
        
    #if the API flag is false, pull data from local storage
        else:
            #unpackage JSON account and tweet data
            jPackager = Packager("json_train_data", filetype="json")
            train_data = jPackager.unpackage_json()
            
            #for each account and tweet set in
            for pos, acct in enumerate(train_data):
                normalizer = Normalizer()
                
                #format account data and normalize to Account() object
                account = Account(normalizer.normalize_user_fetch(train_data[pos]["account_data"], JSON=True))
                
                #format tweet data and normalize to Tweet() object list
                tweets_raw = normalizer.normalize_content_fetch(train_data[pos]["tweet_data"], JSON=True)
    
                #prepare tweet profile and auxiliary metadata, then aggregate all account data to finalize account model
                account.format_account(tweets_raw)
                 
                #package and store account data in packager()
                packager.store(account)
                
        #return trainable account data to preset
        return packager.rows