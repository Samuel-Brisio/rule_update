import os
import re
from datetime import datetime

def diffHasIDField(str1, str2):
    words1 = re.split(';', str1)
    words2 = re.split(';', str2)

    if len(words1) != len(words2):
        return False
    
    set1 = set(words1)
    set2 = set(words2)

    diff = set1.difference(set2)

    # se for maior que 1, as regras diferem em algum outro campo alem do id
    if len(diff) > 1:
        return False

    # se não possui diferença
    if len(diff) == 0:
        return True

    # obs diff tem tamanho unitario
    for e in diff:
        diff = e

    isIDField = re.findall("[\s]*[s][i][d][\s]*[:][\d]+", diff)

    if len(isIDField) == 0:
        return False

    return True 

    


newRulesFile = open('files/new_rules.rules')

rulesDirectory = "example_file/rules/"
ruleUpdate = open(rulesDirectory + "ruleUpdate_" + str(datetime.now()), 'w')

# iterate over files in
# that directory

for newRule in newRulesFile:
    hasNewRule = False

    for filename in os.listdir(rulesDirectory):
        f = os.path.join(rulesDirectory, filename)
        
        # checking if it is a file
        if not os.path.isfile(f):
            continue
        
        File = open(f)


        for row in File:
            isNotRule = re.search("#", row)
            
            if isNotRule or len(row) == 0 or row == '\n':
                continue

            hasNewRule = diffHasIDField(newRule, row)

            if hasNewRule:
                break
        if hasNewRule:
            break
    
    if not hasNewRule:
        ruleUpdate.write(newRule)

            


