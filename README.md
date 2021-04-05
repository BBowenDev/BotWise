# BotWise
**A Model to Capture and Recognize Bot Activity on Twitter**

### **Introduction**
BotWise is a model to analyze human activity and characteristics on Twitter and compare that to novel data of unknown origin. An account may either be marked as "likely a bot" or "not likely a bot." The model also errs on the side of caution, only flagging an account at 95% certainty or above. 

### **Prerequisites**
- Python 3.8 or greater
- git

### **Installation**
Clone the repository and `cd` into it.

```
git clone https://github.com/BraedenLB/BotWise.git
cd BotWise
```

### **Setup**
To run the script, run the following, where `XXXX` is your Twitter Bearer Authentication Token. If you do not have a token, you can apply for one [here](https://developer.twitter.com/). 
```
python BotWise.py XXXX
```


### ** Training a New Model**

