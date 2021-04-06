from Classes.account import Account
from Classes.tweet import Tweet
from Classes.packager import Packager
from Classes.normalizer import Normalizer
from Classes.comparator import Comparator
from Classes.grabber import Grabber
import time
import sys

if __name__ == "__main__":
    grabber = Grabber(sys.argv[1])

print("**********************************")
print("BotWise")
print("**********************************")

#Create driver class object instances
normalizer = Normalizer()

#Take user input, retrieve from Twitter API
acct_raw = input("Enter account: @")
print()

start_time = time.time()
#grabber() calls API, normalizer() frames API data, account() creates new account with data
account = Account(normalizer.normalize_user_fetch(grabber.grab_user(acct_raw)))

#grabber() looks up user by ID number
#grabber() calls API, normalizer() frames API data, returns dictionary metadata list
id_raw = grabber.user_lookup(acct_raw)
tweets_raw = normalizer.normalize_content_fetch(grabber.grab_content(id_raw))

#prepare tweet profile and auxiliary metadata, then aggregate all account data to finalize account model
account.format_account(tweets_raw)

#package account data
packager = Packager(acct_raw)

#OPTIONAL: package data to output file
#packager.package(account)

acct_packed = packager.package(account, rtn=True, sd_keys=True)

#format pacakged data
for pos, data in enumerate(acct_packed):
    if data == True:
        acct_packed[pos] = [1]
    elif data == False:
        acct_packed[pos] == [0]
        
    if not type(data) == list:
        acct_packed[pos] = [data]

#prepare to unpack the test max allowance
maxpack = Packager("base_max", filetype="json")

#unpack the model list [average, standard deviation] and prepare comparator with model and max allowance
modelpack = Packager("base_model", filetype="json")
comparator = Comparator(modelpack.unpackage_json(), test_max=maxpack.unpackage_json())

#set number of acceptable deviations from the norm
ranges = [1.5, 1.75, 2.0]
passes = 0

#compare account to model, return the Z scores, and convert to B values
for drange in ranges:
    comparator.set_range(drange)    
    passes += comparator.compare(acct_packed, output=True)
    
if passes > 1:
    print(">>> ACCOUNT IS LIKELY A BOT")
else:
    print(">>> ACCOUNT IS NOT LIKELY A BOT")

print("ACCOUNT ANALYZED IN", str(time.time()-start_time), "SECONDS")
