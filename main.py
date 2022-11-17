import os
import re
import yaml
import sys
import getopt


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


def argumentsParsing(argv):
    try:
        opts, args = getopt.getopt(argv, 'hc:', 'config')
    except getopt.GetoptError:
        print('main.py -c <configfile>')
        sys.exit(2)
    
    parameters = []

    if opts:
        parameters = opts
    elif args:
        parameters = args
    else:
        print('main.py -c <configfile>')
        sys.exit(2)
    
    return parameters 


def yamlParsing(fileName):
    try:
        file = open(fileName, 'r')
    except FileNotFoundError:
        print("Arquivo não existe")
        sys.exit(2)
    
    yamlFile = yaml.safe_load(file)
    return yamlFile['paths'], yamlFile["file_names"]


def main():
    args = argumentsParsing(sys.argv[1:])
    paths, names = yamlParsing(args[-1])

    newRulesFile = open(paths['new_rules'] + names['new_rules'])

    rulesDirectory = paths['rules']
    ruleUpdate = open(rulesDirectory + names["rule_update"], 'a+')

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

    os.remove(paths['new_rules'] + names['new_rules'])


if __name__ == "__main__":
    main()
