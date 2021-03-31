from Classes.comparator import Comparator
from Classes.packager import Packager
from Classes.account import Account
from Classes.tweet import Tweet
from Classes.normalizer import Normalizer
from Classes.grabber import Grabber

class Tester():
     def __init__(self, test_list, max_num=100, API=True):
        self.test_list = test_list + ".tsv"
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
        self.json_data = []
        
        #M Values data frame has format:
        """
        [{1.5: 0.0,
          1.75: 0.0,
          2.0: 0.0
          }]
        """
        self.m_vals = []
        
     def test(self):
        normalizer = Normalizer()
        packager = Packager("test_passage")
        
        #import list of real accounts to test
        testlist = open(self.test_list, "r")
        lines = testlist.readlines()
       
        if self.USE_API:
            #For each account in test_list, grab and aggregate data
            testnum = 0
            for acct in lines:
                try:    
                    if testnum == self.max_num:
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
                    testnum += 1
                
                    #append raw JSON data, save to object, and normalize to tweet list
                    json_data["tweet_data"] = content_data["data"]                    
                    self.json_data.append(json_data)
                    tweets_raw = normalizer.normalize_content_fetch(content_data)
                    
                    #prepare tweet profile and auxiliary metadata, aggregate all account data to finalize account model
                    account.format_account(tweets_raw)
                    
                    #package and store account data in packager()
                    packager.store(account)
                    self.accounts.append(account)
                    
                    #output raw JSON data for later use
                    jPackager = Packager("json_test_data", filetype="json")
                    jPackager.package_json(self.json_data)
                    continue
            
            #rather than have errors crash the testing process, just skip that account and continue
                except Exception as e:
                    print(acct_raw + "--", e)
                    continue 
            
        #if API flag is false, use preexisting JSON data
        else:
             #unpackage JSON account and tweet data
               jPackager = Packager("json_test_data", filetype="json")
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
                   self.accounts.append(account)
        
        #package all data (either from API or JSON) to CSV
        packager.package_all()

        accounts = []
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
            accounts.append(acct_packed)
        
        #unpack the model list [average, standard deviation] and prepare comparator
        modelpack = Packager("model_base", filetype="json")
        comparator = Comparator(modelpack.unpackage_json())
        
        #set number of acceptable deviations from the norm and create containers
        ranges = [1.5, 1.75, 2.0]
        z_val = []
        p_vals = {1.5: [], 1.75: [], 2.0: []}
        m_vals = {1.5: 0.0, 1.75: 0.0, 2.0: 0.0}
        
        #compare account to model and find Z (z-score), P (list of z-scores), B (average of P), and M(95th percentile of B) values
        for drange in ranges:
            comparator.set_range(drange)
            for acct in accounts:
                #find the z score of the account compared to training set
                z_val = comparator.compare(acct, zv=True)
                
                #find the B value and append to P
                p_vals[drange].append(sum(z_val) / len(z_val))
            
            #sort the p_vals at drange and select the B value in the 95th percentile
            percentile = int(len(p_vals[drange])*0.05)
            m_vals[drange] = sorted(p_vals[drange])[-percentile]
                
        self.m_vals = [m_vals]
        print("P VALUES:", p_vals)
        print("M VALUES:", self.m_vals)

        #output max value data as JSON
        jPackager = Packager("None", filetype="json")
        jPackager.package_json(self.m_vals, "test_max")

tester = Tester("test_real_list", max_num=100, API=True)
tester.test()