from Classes.grabber import Grabber
import csv

grabber = Grabber()

ids = ""
users = []
num = 0
limit = 0
with open("midterm_2.txt", "r") as f:
    reader = csv.reader(f)
    lines = []
    for line in reader:
        if num < 40000:
            if limit < 100:
                ids += str(line[0]) + ","
                num += 1
                limit += 1
            else:
                users.append(ids[:-1])
                ids = ""
                limit = 0
        else: break

data = []
for row in users:
    check = grabber.grab_check(row)
    print(check)
    data += check["data"]

with open("test_bot_list.tsv", "w") as f:
    for user in data:
        f.write(user["username"] + "\t" + user["id"] + "\n")
    f.close()
