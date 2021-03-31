import csv
import io
import json

class Packager ():
    def __init__(self, filename, filetype="csv"):
        self.file = filename + "." + filetype
        self.rows = []
    
    #keys and locations in fields for the 60 points of comparison
    sd_keys = {'name_length': 1, 'name_capitals_num': 3, 'name_capitals_pos': 4, 'name_punctuation_num': 6, 
                     'name_punctuation_pos': 7, 'name_numbers_num': 9, 'name_numbers_pos': 10, 'display_length': 12, 
                     'display_capitals_num': 14, 'display_capitals_pos': 15, 'display_punctuation_num': 17, 
                     'display_punctuation_pos': 18, 'display_emoji_num': 20, 'display_emoji_pos': 21, 'bio_length': 22, 
                     'bio_capitals_num': 24, 'bio_capitals_pos': 25, 'bio_punctuation_num': 27, 'bio_punctuation_pos': 28, 
                     'bio_emoji_num': 30, 'bio_emoji_pos': 31, 'bio_stopwords_num': 33, 'bio_stopwords_pos': 34, 
                     'bio_tags_num': 36, 'bio_tags_pos': 37, 'bio_hashtags_num': 39, 'bio_hashtags_pos': 40, 
                     'has_profile_pic': 41, 'has_link': 42, 'has_location': 43, 'has_pinned': 44, 'follow_ratio': 47, 
                     'avg_daily': 49, 'per_diem': 50, 'per_diem_rate': 51, 'days_between': 52, 'times_between': 53, 
                     'original_ratio': 57, 'rt_ratio': 59, 'reply_ratio': 61, 'num_langs': 62, 'langs_ratio': 63, 
                     'num_mediums': 64, 'mediums_ratio': 65, 'link_ratio': 67, 'attachment_ratio': 69, 'lengths': 70, 
                     'words': 71, 'capitals_num': 73, 'capitals_pos': 74, 'stopwords_num': 76, 'stopwords_pos': 77, 
                     'hashtags_num': 79, 'hashtags_pos': 80, 'tags_num': 82, 'tags_pos': 83, 'punctuation_num': 85, 
                     'punctuation_pos': 86, 'emoji_num': 88, 'emoji_pos': 89}
    
    #keys and locations for all 90 data points collected
    keys = {'user_name': 0, 'name_length': 1, 'name_capitals': 2, 'name_capitals_num': 3, 
            'name_capitals_pos': 4, 'name_punctuation': 5, 'name_punctuation_num': 6, 
            'name_punctuation_pos': 7, 'name_numbers': 8, 'name_numbers_num': 9, 'name_numbers_pos': 10, 
            'display_name': 11, 'display_length': 12, 'display_capitals': 13, 'display_capitals_num': 14, 
            'display_capitals_pos': 15, 'display_punctuation': 16, 'display_punctuation_num': 17, 
            'display_punctuation_pos': 18, 'display_emoji': 19, 'display_emoji_num': 20, 
            'display_emoji_pos': 21, 'bio_length': 22, 'bio_capitals': 23, 'bio_capitals_num': 24, 
            'bio_capitals_pos': 25, 'bio_punctuation': 26, 'bio_punctuation_num': 27, 'bio_punctuation_pos': 28, 
            'bio_emoji': 29, 'bio_emoji_num': 30, 'bio_emoji_pos': 31, 'bio_stopwords': 32, 'bio_stopwords_num': 33, 
            'bio_stopwords_pos': 34, 'bio_tags': 35, 'bio_tags_num': 36, 'bio_tags_pos': 37, 'bio_hashtags': 38, 
            'bio_hashtags_num': 39, 'bio_hashtags_pos': 40, 'has_profile_pic': 41, 'has_link': 42, 
            'has_location': 43, 'has_pinned': 44, 'followers': 45, 'following': 46, 'follow_ratio': 47, 
            'num_days': 48, 'avg_daily': 49, 'per_diem': 50, 'per_diem_rate': 51, 'days_between': 52, 
            'times_between': 53, 'num_total_tweets': 54, 'num_read': 55, 'num_tweets_ngram': 56, 
            'original_ratio': 57, 'num_rts': 58, 'rt_ratio': 59, 'num_replies': 60, 'reply_ratio': 61, 
            'num_langs': 62, 'langs_ratio': 63, 'num_mediums': 64, 'mediums_ratio': 65, 'num_links': 66, 
            'link_ratio': 67, 'num_attachments': 68, 'attachment_ratio': 69, 'lengths': 70, 'words': 71, 
            'capitals': 72, 'capitals_num': 73, 'capitals_pos': 74, 'stopwords': 75, 'stopwords_num': 76, 
            'stopwords_pos': 77, 'hashtags': 78, 'hashtags_num': 79, 'hashtags_pos': 80, 'tags': 81, 
            'tags_num': 82, 'tags_pos': 83, 'punctuation': 84, 'punctuation_num': 85, 'punctuation_pos': 86, 
            'emoji': 87, 'emoji_num': 88, 'emoji_pos': 89
            }
    
    fields = [  #username data
                "user_name", "name_length", "name_capitals", "name_capitals_num",
                "name_capitals_pos", "name_punctuation", "name_punctuation_num",
                "name_punctuation_pos", "name_numbers", "name_numbers_num", "name_numbers_pos",
                
                #display name data
                "display_name", "display_length", "display_capitals", "display_capitals_num",
                "display_capitals_pos", "display_punctuation", "display_punctuation_num",
                "display_punctuation_pos", "display_emoji", "display_emoji_num", "display_emoji_pos",
                
                #bio data 
                "bio_length", "bio_capitals", "bio_capitals_num", "bio_capitals_pos",
                "bio_punctuation", "bio_punctuation_num", "bio_punctuation_pos", "bio_emoji",
                "bio_emoji_num", "bio_emoji_pos", "bio_stopwords", "bio_stopwords_num", "bio_stopwords_pos",
                "bio_tags", "bio_tags_num", "bio_tags_pos", "bio_hashtags", "bio_hashtags_num", "bio_hashtags_pos",
                
                #profile data  
                "has_profile_pic", "has_link", "has_location", "has_pinned",
                
                #follow data
                "followers", "following", "follow_ratio",
                
                #day data 
                "num_days", "avg_daily", "per_diem", "per_diem_rate", "days_between", "times_between",
                
                #tweet numbers data
                "num_total_tweets", "num_read", "num_tweets_ngram", 
                
                #tweet types data
                "original_ratio", "num_rts", "rt_ratio", "num_replies", "reply_ratio", 
                 
                #per tweet data
                "num_langs", "langs_ratio", "num_mediums", "mediums_ratio",  
                
                #tweet items data
                "num_links", "link_ratio", "num_attachments", "attachment_ratio", 
                
                #tweet size data
                "lengths", "words", 
                 
                #tweet content data
                "capitals", "capitals_num", "capitals_pos", "stopwords", "stopwords_num", "stopwords_pos",  
                "hashtags", "hashtags_num", "hashtags_pos", "tags", "tags_num", "tags_pos", "punctuation", 
                "punctuation_num", "punctuation_pos", "emoji", "emoji_num", "emoji_pos" 
                ]
    
    
    def package(self, account, rtn=False, sd_keys=False):
        row = [account.meta["user_name"], account.agg_meta["user_name"]["length"],
               list(account.agg_meta["user_name"]["capitals"].ngram.keys()), account.agg_meta["user_name"]["capitals"].get_numbers(),
               account.agg_meta["user_name"]["capitals"].get_positions(), list(account.agg_meta["user_name"]["punctuation"].ngram.keys()), 
               account.agg_meta["user_name"]["punctuation"].get_numbers(), account.agg_meta["user_name"]["punctuation"].get_positions(),
               list(account.agg_meta["user_name"]["numbers"].ngram.keys()), account.agg_meta["user_name"]["numbers"].get_numbers(), 
               account.agg_meta["user_name"]["numbers"].get_positions(),
               
               account.meta["user_display"], account.agg_meta["user_display"]["length"],
               list(account.agg_meta["user_display"]["capitals"].ngram.keys()), account.agg_meta["user_display"]["capitals"].get_numbers(),
               account.agg_meta["user_display"]["capitals"].get_positions(), list(account.agg_meta["user_display"]["punctuation"].ngram.keys()), 
               account.agg_meta["user_display"]["punctuation"].get_numbers(), account.agg_meta["user_display"]["punctuation"].get_positions(),
               list(account.agg_meta["user_display"]["emoji"].ngram.keys()), account.agg_meta["user_display"]["emoji"].get_numbers(), 
               account.agg_meta["user_display"]["emoji"].get_positions(),
            
               account.agg_meta["user_bio"]["length"],
               list(account.agg_meta["user_bio"]["capitals"].ngram.keys()), account.agg_meta["user_bio"]["capitals"].get_numbers(),
               account.agg_meta["user_bio"]["capitals"].get_positions(), list(account.agg_meta["user_bio"]["punctuation"].ngram.keys()), 
               account.agg_meta["user_bio"]["punctuation"].get_numbers(), account.agg_meta["user_bio"]["punctuation"].get_positions(),
               list(account.agg_meta["user_bio"]["emoji"].ngram.keys()), account.agg_meta["user_bio"]["emoji"].get_numbers(), 
               account.agg_meta["user_bio"]["emoji"].get_positions(), list(account.agg_meta["user_bio"]["stopwords"].ngram.keys()), 
               account.agg_meta["user_bio"]["stopwords"].get_numbers(), account.agg_meta["user_bio"]["stopwords"].get_positions(),
               list(account.agg_meta["user_bio"]["tags"].ngram.keys()), account.agg_meta["user_bio"]["tags"].get_numbers(), 
               account.agg_meta["user_bio"]["tags"].get_positions(), list(account.agg_meta["user_bio"]["hashtags"].ngram.keys()), 
               account.agg_meta["user_bio"]["hashtags"].get_numbers(), account.agg_meta["user_bio"]["hashtags"].get_positions(),
               
               account.meta["HAS_PROFILE_PIC"], account.meta["HAS_LINK"], account.meta["HAS_LOCATION"], account.meta["HAS_PINNED"],
               account.meta["followers"], account.meta["following"], account.calc_meta["follow_ratio"], 
               account.meta["num_days"], account.calc_meta["avg_daily"], account.agg_meta["days_times"].get_numbers(), 
               account.calc_meta["per_diem_rate"], account.calc_meta["days_between"], account.calc_meta["times_between"], account.meta["num_total_tweets"],  
               account.meta["num_read"], account.meta["num_tweets_ngram"], account.calc_meta["original_ratio"], 
               account.meta["num_rts"], account.calc_meta["rt_ratio"], account.meta["num_replies"], account.calc_meta["reply_ratio"],
               account.meta["num_langs"], account.calc_meta["langs_ratio"], account.meta["num_mediums"], account.calc_meta["mediums_ratio"],
               account.meta["num_links"], account.calc_meta["link_ratio"], account.meta["num_attachments"], account.calc_meta["attachment_ratio"],
               account.agg_meta["lengths"], account.agg_meta["words"],
               
               list(account.agg_meta["capitals"].ngram.keys()), account.agg_meta["capitals"].get_numbers(), account.agg_meta["capitals"].get_positions(), 
               list(account.agg_meta["stopwords"].ngram.keys()), account.agg_meta["stopwords"].get_numbers(), account.agg_meta["stopwords"].get_positions(),
               list(account.agg_meta["hashtags"].ngram.keys()), account.agg_meta["hashtags"].get_numbers(), account.agg_meta["hashtags"].get_positions(),
               list(account.agg_meta["tags"].ngram.keys()), account.agg_meta["tags"].get_numbers(), account.agg_meta["tags"].get_positions(),
               list(account.agg_meta["punctuation"].ngram.keys()), account.agg_meta["punctuation"].get_numbers(), account.agg_meta["punctuation"].get_positions(),
               list(account.agg_meta["emoji"].ngram.keys()), account.agg_meta["emoji"].get_numbers(), account.agg_meta["emoji"].get_positions()
            ]
        #if the return flag is set to false, output to file
        if rtn == False: 
            with io.open(self.file, "w", newline="", encoding="utf-8") as f:
                write = csv.writer(f)
                write.writerow(self.fields)
                write.writerow(row)
        #else, return packaged data that coincides with the items in self.sd_keys
        else:
            #if the sd_keys flag is false, return all
            if sd_keys == False:
                packaged = []
                for pos, item in enumerate(row):
                    if pos in self.keys.values():
                        packaged.append(item)
            else:
                packaged = []
                for pos, item in enumerate(row):
                    if pos in self.sd_keys.values():
                        packaged.append(item)
            return packaged
    
    def package_dataset(self, dataset, filename=False, multi=False):
        fields = self.sd_keys.keys()
        
        if filename == False:
            filename = self.file
        else:
            filename += ".csv"
        
        with io.open(filename, "w", newline="", encoding="utf-8") as f:
            write = csv.writer(f)
            write.writerow(fields)
            
            if multi == False:
                write.writerow(dataset) 
            else:
                for row in dataset:
                    write.writerow(row)
                
    def package_all(self):
        with io.open(self.file, "w", newline="", encoding="utf-8") as f:
            write = csv.writer(f)
            write.writerow(self.fields)
            for row in self.rows:
                write.writerow(row)
    
    def store(self, line):
        self.rows.append(self.package(line, rtn=True))
    
    def format_stored(self):
        lines = []
        line = []
        for row in self.rows:
            for key in self.sd_keys.keys():
                line.append(row[self.sd_keys[key]])        
            lines.append(line)
            line = []
        return lines
    
    
    #UNPACKAGING METHODS
    def unpackage(self, file=False):
        if file == False:
            file = self.file
        
        with open(file, "r") as f:
           reader = csv.reader(f)
           lines = []
           for pos, line in enumerate(reader):
               if pos > 0:
                   for lst in line:
                       new = lst.replace("[","").replace("]","").split(",")
                       lines.append([float(new[0]), float(new[1])])
           return lines
    
    def unpackage_training(self, file=False):
        if file == False:
            file = self.file
    
        with open(file, "r") as f:
            reader = csv.reader(f)
            lines = []
            for pos, line in enumerate(reader):
                if pos > 0:
                    lines.append(line)
        return lines
    
    
    #JSON METHODS
    def package_json(self, data, filename=False, filetype="json"):
        if filename == False:
            filename = self.file
        else: 
            filename += "." + filetype
        
        with open(filename, 'w') as f:
            json.dump(data, f)
            
    def unpackage_json(self, filename=False, filetype="json"):
        if filename == False:
            filename = self.file
        else: 
            filename += "." + filetype
        
        with open(filename, "r") as f:
            return json.load(f)

    