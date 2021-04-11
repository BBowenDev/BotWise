from Classes.trainer import Trainer
from Classes.comparator import Comparator
from Classes.packager import Packager

class Tester():
     def __init__(self, grabber, test_list="list_test", test_num=100, API=True):
        self.grabber = grabber
        self.test_list = test_list + ".tsv"
        self.test_num = test_num
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
        self.json_test_data = []
    
     def test(self):
        packager = Packager("output_test")
        trainer = Trainer(self.grabber, API=True)
        self.accounts = []
        
        #import training list of accounts
        testlist = open(self.test_list, "r")
        lines = testlist.readlines()
        
        #For each account in test_list, grab and aggregate data
        testnum = 0
        for acct in lines:  
            if testnum == self.test_num:
                break
            
            json_data, account = trainer.build(acct)
            
            #package and store account data in packager()
            if not account == None:
                packager.store(account)
                self.json_test_data.append(json_data)
                self.accounts.append(account)
                testnum += 1
            
        #output raw JSON data for later use
        jPackager = Packager("data_test_json", filetype="json")
        jPackager.package_json(self.json_test_data)
        
        #package all account data
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
        
        #prepare to unpack the test max allowance
        maxpack = Packager("base_max", filetype="json")
        
        #unpack the model list [average, standard deviation] and prepare comparator with model and max allowance
        modelpack = Packager("base_model", filetype="json")
        comparator = Comparator(modelpack.unpackage_json(), test_max=maxpack.unpackage_json())
        
        #set number of acceptable deviations from the norm
        ranges = [1.5, 1.75, 2.0]
        passes = {1.5: 0, 1.75: 0, 2.0: 0}

        for drange in ranges:
            for account in accounts_formatted:
                comparator.set_range(drange)
                passes[drange] += comparator.compare(account)
            print("PASSAGE AT", str(drange)+":", self.test_num-passes[drange], "/", self.test_num) 
