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
To run the script, run the following, where `A` is your Twitter Bearer Authentication Token. If you do not have a token, you can apply for one [here](https://developer.twitter.com/). 
```
python BotWise.py A
```


### **Training a New Model**
The repository uses a pre-trained model for decision-making. The `preseter.py` script creates a new model for BotWise to use. To create a new model, run the script in the command line.
```
python preseter.py A B C
```
- `A` is the number of accounts to build the model from
- `B` is the number of accounts to build the max 
- `C` is your Twitter Bearer Authentication Token. If you do not have a token, you can apply for one [here](https://developer.twitter.com/). 

Limited options for model creation are accessible from the command line, but the declaration of `Trainer` and `Tester` objects in the script allow for more customization.
