from Classes.account import Account
from Classes.packager import Packager
from Classes.comparator import Comparator
from Classes.normalizer import Normalizer

class Trainer ():  
    def __init__(self, grabber, train_list="list_train", list_max="list_max", train_num=700, max_num=100, API=True):
        self.grabber = grabber
        self.train_list = train_list + ".tsv"
        self.list_max = list_max + ".tsv"
        self.train_num = train_num
        self.max_num = max_num
        self.USE_API = API

        self.accounts = []        

        #JSON data frame has format:
        """
        [{"user_name": "", 
          "user_id": "",
          "account_data": {},
          "tweet_data": {}
          },
        ]
        """
        self.json_train_data = []
        self.json_max_data = []
        
        #M Values data frame has format:
        """
        [{1.5: 0.0,
          1.75: 0.0,
          2.0: 0.0
          }]
        """
        self.m_vals = []
        
    def train_build(self):
        #Create packager to input, store, and output data
        packager = Packager("output_train")
        
        #set to True if API should be used, False if pulling from existing data
        if self.USE_API:
            #import training list of accounts
            trainlist = open(self.train_list, "r")
            lines = trainlist.readlines()
            
           #For each account in test_list, grab and aggregate data
            testnum = 0
            for acct in lines:  
                if testnum == self.train_num:
                    break
                
                json_data, account = self.build(acct)
                
                #package and store account data in packager()
                if not account == None:
                    self.json_train_data.append(json_data)
                    packager.store(account)
                    testnum += 1
                
            #output raw JSON data for later use
            jPackager = Packager("data_train_json", filetype="json")
            jPackager.package_json(self.json_train_data)
            
            #package all account data
            packager.package_all() 
          
    #if the API flag is false, pull data from JSON
        else:
            #unpackage JSON account and tweet data
            jPackager = Packager("data_train_json", filetype="json")
            train_data = jPackager.unpackage_json()
            
            #for each account and tweet set in the train data, format to account
            for pos, acct in enumerate(train_data):
                account = self.json_build(train_data, pos)
                 
                #package and store account data in packager()
                packager.store(account)
                
        #return trainable account data to preset
        return packager.rows 


    def max_build(self):
        normalizer = Normalizer()
        packager = Packager("output_max")
        
        self.accounts = []
        
        #import list of real accounts to test
        testlist = open(self.list_max, "r")
        lines = testlist.readlines()
       
        if self.USE_API:
            #For each account in test_list, grab and aggregate data
            testnum = 0
            for acct in lines:  
                if testnum == self.max_num:
                    break
                
                json_data, account = self.build(acct)
                
                #package and store account data in packager()
                if not account == None:
                    self.json_max_data.append(json_data)
                    packager.store(account)
                    self.accounts.append(account)
                    testnum += 1
            
            #output raw JSON data for later use
            jPackager = Packager("data_max_json", filetype="json")
            jPackager.package_json(self.json_max_data)
            
        #if API flag is false, use preexisting JSON data
        else:
            #unpackage JSON account and tweet data
            jPackager = Packager("data_max_json", filetype="json")
            train_data = jPackager.unpackage_json()
               
            self.json_build(train_data)
            
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
                self.accounts.append(account)
        
        #package all data (either from API or JSON) to CSV
        packager.package_all()

        accounts_formatted = []
        for line in self.accounts:
            #package account data
            acct_packed = packager.package(line, rtn=True, sd_keys=True)
            
            #format pacakged data
            for pos, data in enumerate(acct_packed):
                if data == True:
                    acct_packed[pos] = [1]
                elif data == False:
                    acct_packed[pos] == [0]
                if not type(data) == list:
                    acct_packed[pos] = [data] 
                accounts_formatted.append(acct_packed)
        
        #unpack the model list [average, standard deviation] and prepare comparator
        modelpack = Packager("base_model", filetype="json")
        comparator = Comparator(modelpack.unpackage_json())
        
        #set number of acceptable deviations from the norm and create containers
        ranges = [1.5, 1.75, 2.0]
        z_val = []
        p_vals = {1.5: [], 1.75: [], 2.0: []}
        m_vals = {1.5: 0.0, 1.75: 0.0, 2.0: 0.0}
        
        #compare account to model and find Z (z-score), P (list of z-scores), B (average of P), and M(95th percentile of B) values
        for drange in ranges:
            comparator.set_range(drange)
            for acct in accounts_formatted:
                #find the z score of the account compared to training set
                z_val = comparator.compare(acct, zv=True)
                
                #find the B value and append to P
                p_vals[drange].append(sum(z_val) / len(z_val))
            
            #sort the p_vals at drange and select the B value in the 95th percentile
            percentile = int(len(p_vals[drange])*0.05)
            m_vals[drange] = sorted(p_vals[drange])[-percentile]
                
        return m_vals


    def build(self, acct):
        #format and split raw account info
        data_raw = acct.replace("\n", "").split("\t")
        acct_raw = data_raw[0]
        id_raw = data_raw[1]
        
        #reset objects to clear previous data
        normalizer = Normalizer()
        
        try:
            #grabber() calls API, normalizer() frames API data, account() creates new account with data
            #if account is inaccessible, ignore and print error
            user_data = self.grabber.grab_user(acct_raw)
            if "errors" in user_data.keys():
                print(acct_raw + "--", user_data["errors"][0]["detail"])
                return None, None 
            
            #append raw data to JSON data and normalize to account
            json_data = {"user_name": acct_raw, "user_id": id_raw, "accunt_data": user_data["data"][0], "tweet_data": {}}
            account = Account(normalizer.normalize_user_fetch(user_data))
            
            #grabber() calls API, normalizer() frames API data, returns dictionary metadata list
            #if content is inaccessible, ignore and print error
            content_data = self.grabber.grab_content(id_raw)
            if "errors" in content_data.keys():
                print(acct_raw + "--", content_data["errors"][0]["detail"])
                return None, None
                
            elif content_data["meta"]["result_count"] == 0:
                print(acct_raw + "--", "insuf tweets")
                return None, None
        
            #append raw JSON data, save to object, and normalize to tweet list
            json_data["tweet_data"] = content_data["data"]                    
            
            tweets_raw = normalizer.normalize_content_fetch(content_data)
        
            #prepare tweet profile and auxiliary metadata, aggregate all account data to finalize account model
            account.format_account(tweets_raw)
        
        #rather than have errors crash the testing process, just skip that account and continue
        except Exception as e:
            print(acct_raw + "--", e)
            return None, None
        
        return json_data, account 


    def json_build(self, train_data, position):
        normalizer = Normalizer()
        
        #format account data and normalize to Account() object
        account = Account(normalizer.normalize_user_fetch(train_data[position]["account_data"], JSON=True))
        
        #format tweet data and normalize to Tweet() object list
        tweets_raw = normalizer.normalize_content_fetch(train_data[position]["tweet_data"], JSON=True)

        #prepare tweet profile and auxiliary metadata, then aggregate all account data to finalize account model
        account.format_account(tweets_raw)
        
        return account