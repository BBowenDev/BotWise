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
To run the script, run the following, where `XXXX` is your Twitter Bearer Authentication Token. If you do not have a token, one can be found [here](https://developer.twitter.com/). 
```
python BotWise.py XXXX
```


### ** Training a New Model**

This script uses a previous set of training and testing data utilizing the files `model_base.json` and `test_max.json`. To create a new model, utilize the `preseter.py` script, which pulls training data from `train_list.tsv` and testing data from `test_real_list.tsv`, taken from the [Yang et al. (2020)](https://arxiv.org/abs/1911.09179) midterm-2018 dataset, with each list consisting of 3,729 human accounts. 

The declarations of `Trainer` and `Tester` objects in the `preseter.py` script can modify the usage of the dataset. By default, 700 accounts are used to train, which returns `model_base.json`, the set of standard deviations and average, and 100 accounts are used to test, which returns `test_max.json`, the maximum allowable values.
