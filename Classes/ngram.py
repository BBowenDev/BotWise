class nGram ():
    def __init__(self):
        self.ngram = {}
    def __len__(self):
        return len(self.ngram)
    def __str__(self):
        return str(self.ngram)
         
    """
    ngram = {
        "word": {"number": 0, "position": []}}  
    """

    #append new word to ngram
    def append(self, word, position=-1):
    #is word in ngram?
        if word in self.ngram.keys():
           self.ngram[word]["number"] = self.ngram[word]["number"] + 1
           
           if not position == -1:
               self.ngram[word]["position"].append(position)

    #if not, create entry
        else:
            self.ngram[word] = {"number": 1, "position": [position]}
    
    #append all words in new ngram to ngram
    def append_all(self, new):
        if not new.ngram == {}:  
            for word in new.ngram:
                if word in self.ngram.keys():
                    self.ngram[word]["number"] = self.ngram[word]["number"] + new.ngram[word]["number"]
                    if not new.ngram[word]["position"] == []:
                        self.ngram[word]["position"] += new.ngram[word]["position"]
                else:
                    self.ngram[word] = {"number": new.ngram[word]["number"], "position": new.ngram[word]["position"]}
    
    def get_numbers(self):
        nums = [self.ngram[word]["number"] for word in self.ngram]
        
        if nums == []:
            return [0]
        return nums
        
    def get_positions(self):
        pos = []
        for word in self.ngram:
            pos = pos + self.ngram[word]["position"]
        return pos
    
    def get_sorted_nums(self):
        return sorted(self.get_numbers())
            
    def get_sorted_positions(self):
        return sorted(self.get_positions())