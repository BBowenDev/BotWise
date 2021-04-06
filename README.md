# BotWise
**A Model to Capture and Recognize Bot Activity on Twitter**

### **Introduction**
BotWise is a model to analyze human activity and characteristics on Twitter and compare that to novel data of unknown origin. An account may either be marked as "likely a bot" or "not likely a bot." The model also errs on the side of caution, only flagging an account at 95% certainty or above. 

### **Prerequisites**
- Python >= 3.8
- [git](https://git-scm.com/download/win)
- [Twitter Bearer Authentication Token](https://developer.twitter.com/)

### **Installation**
Clone the repository and `cd` into it.

```
git clone https://github.com/BraedenLB/BotWise.git
cd BotWise
```

### **Setup**
The repository should be ready for use after cloning, as it contains a pre-trained model in `base_model.json` and `base_max.json`. To use the script, run the `BotWise.py` script.
```
python BotWise.py X
```
- `X`- your Twitter Bearer Authentication Token. If you do not have a token, you can apply for one [here](https://developer.twitter.com/). 

The script will print input for a Twitter account to be analyzed. If the Auth Token is correct, the script will return relevant data and a verdict on the account's veracity.
```
**********************************
BotWise
**********************************
Enter account: @
```


### **Training a New Model**
The repository uses a pre-trained model for decision-making. The `preseter.py` script creates a new model for BotWise to use. To create a new model, run the script in the command line.
```
python preseter.py A B C
```
- `A`- the number of accounts to build the training model 
- `B`- the number of accounts to build the maxing model 
- `C`- your Twitter Bearer Authentication Token

Limited options for model creation are accessible from the command line, but the declaration of `Trainer` and `Tester` objects in the script allow for more customization. 

The model will pull account data from the `list_train.tsv`, `list_max.tsv`, and `list_train.tsv`. Training a new model will result in 9 new files: 
- `base_model.json`- a _critical_ JSON file containing model average and standard deviation
- `base_max.json`- a _critical_ JSON file containing model max values
- `data_train.json`- a JSON file containing API training data for re-testing later
- `data_max.json`- a JSON file containing API maxing data for re-testing later
- `data_test.json`- a JSON file containing API testing data for re-testing later
- `output_test.csv`- a CSV file containing raw formatted output for training data
- `output_max.csv`- a CSV file containing raw formatted output for maxing data
- `output_test.csv`- a CSV file containing raw formatted output for testing data
- `std_dev_base.csv`- a CSV file containing average and standard deviation values for training data
