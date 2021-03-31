import math

class Comparator ():
    def __init__(self, model=None, test_max=None, strd_range=1):
        self.model = model
        self.test_max = test_max
        self.strd_range = strd_range
        
    #the list of comparisons between the training model and the new account
    #none by default (object can be used just for deviation calculations)
    model = {}
        
    #the number of acceptable standard deviations from the mean
    #the smaller the range, the stricter the focus of the calculation
    strd_range = 1
    
    def set_model(self, new_model):
        self.model = new_model
    
    def set_range(self, new_range):
        self.strd_range = new_range
    
    #calculate standard deviations for new account, compare all points in self.model{} with all account points
    def compare(self, account, zv=False, output=False):
        z_vals = [] 
        for pos, acct in enumerate(account):
            if len(acct) == 0:
                avg = 0.0
            else:
                avg = sum(acct) / len(acct)
            
            r = self.strd_range
            sd = self.model[pos][1] 
            a = self.model[pos][0]
            
            #if sd > 0   Z = abs(avg-a) / sd > r 
            if not self.model[pos][1] == 0:
                z = abs(avg-a) / sd
                if z > r: 
                    zScore = z
                else:
                    zScore = 0
                    
            #if sd <= 0   Z = abs(avg-a) > r 
            else:
                z = abs(avg-a)
                if z > r:
                    zScore = z 
                else: 
                    zScore = 0
            z_vals.append(zScore)
        
        if zv == True:
            return z_vals
        
        else:
            b_vals = sum(z_vals) / len(z_vals)
            
            passed = 0
            if b_vals > self.test_max[str(r)]:
                passed = 1
            
            if output == True:
                print("B VALUES:", "%.3f" % b_vals, "::", "%.3f" % self.test_max[str(r)])
                print("--> PASSAGE AT", r, "=", "PASSED" if passed == 0 else "FAILED")
            return passed
            
    #calculate the standard deviation for the set
    def standard_dev(self, nums):
        if len(nums) == 0:
            return [0.0, 0.0]
        elif len(nums) == 1:
            return [float(nums[0]), 0.0]
        else:
            avg = float(sum(nums) / float(len(nums)))
            sqrs = [float((x-avg)**2) for x in nums]
            dev = math.sqrt(sum(sqrs)/len(sqrs))
            return [avg, dev]