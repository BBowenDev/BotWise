from trainer import Trainer
from tester import Tester
from comparator import Comparator
from packager import Packager
import time

start_time = time.time()
trainer = Trainer("train_list", max_num=700, API=True)
tester = Tester("test_real_list", max_num=100, API=True)
packager = Packager("none")
comparator = Comparator()

fields = {
    "name_length": [], "name_capitals_num": [], "name_capitals_pos": [],
    "name_punctuation_num": [], "name_punctuation_pos": [], "name_numbers_num": [],
    "name_numbers_pos": [], "display_length": [], "display_capitals_num": [],
    "display_capitals_pos": [], "display_punctuation_num": [], "display_punctuation_pos": [],
    "display_emoji_num": [], "display_emoji_pos": [], "bio_length": [], 
    "bio_capitals_num": [], "bio_capitals_pos": [], "bio_punctuation_num": [],
    "bio_punctuation_pos": [], "bio_emoji_num": [], "bio_emoji_pos": [],
    "bio_stopwords_num": [], "bio_stopwords_pos": [], "bio_tags_num": [],
    "bio_tags_pos": [], "bio_hashtags_num": [], "bio_hashtags_pos": [],
    "has_profile_pic": [], "has_link": [], "has_location": [],
    "has_pinned": [], "follow_ratio": [], "avg_daily": [],
    "per_diem": [], "per_diem_rate": [], "days_between": [], "times_between": [],
    "original_ratio": [], "rt_ratio": [], "reply_ratio": [],
    "num_langs": [], "langs_ratio": [], "num_mediums": [],
    "mediums_ratio": [], "link_ratio": [], "attachment_ratio": [],
    "lengths": [], "words": [], "capitals_num": [],
    "capitals_pos": [], "stopwords_num": [], "stopwords_pos": [],
    "hashtags_num": [], "hashtags_pos": [], "tags_num": [],
    "tags_pos": [], "punctuation_num": [], "punctuation_pos": [],
    "emoji_num": [], "emoji_pos": []
    }

#build the training set from train_list of accounts
trainset = trainer.build()

#holds the standard deviation for each training account
set_dev = []
devs = []

train_num = 0
for line in trainset:
    #for each datapoint in each set, add to the collection
    for key in packager.sd_keys:
        #fix standard deviation with True and False to 1 and 0
        if line[packager.sd_keys[key]] == True:
            line[packager.sd_keys[key]] = [1] 
        elif line[packager.sd_keys[key]] == False:
            line[packager.sd_keys[key]] = [0] 
       
        #make each item into a list for easy concatination
        if not type(line[packager.sd_keys[key]]) == list:
            line[packager.sd_keys[key]] = [line[packager.sd_keys[key]]]
        
        #append item to fields list
        fields[key] += line[packager.sd_keys[key]]    
        
        #find the standard deviation and append
        devs.append(comparator.standard_dev(line[packager.sd_keys[key]]))

    #append the standard deviation set
    set_dev.append(devs)
    devs = []
    train_num += 1

#output the standard deviation of each account
devpackager = Packager("std_dev_base")
devpackager.package_dataset(set_dev, multi=True)

#for each point of comparison in train set, determine the standard deviaiton of the whole set
standard_devs = []
for key in fields.keys():
    standard_devs.append(comparator.standard_dev(fields[key])) 

#package standard deviations model
jPackager = Packager("model_base", filetype="json")
jPackager.package_json(standard_devs)

print("MODEL TRAINED IN", str(time.time()-start_time), "SECONDS")

start_time = time.time()

#build the testing set from the test_real or test_bot 
tester.test()

print("MODEL TESTED IN", str(time.time()-start_time), "SECONDS")

