import json
import os
import argparse


parser = argparse.ArgumentParser(prog='json_export')
parser.add_argument('-f', '--file', help='path to json file. otherwise if you havent used it, '
                                         'the script will be search for json files in the directory '
                                         'where the script is located')
parser.add_argument('--keyword', help='search by keyword')
parser.add_argument('-a','--auth',action='store_true', help='only with password')
args = parser.parse_args()
dir_path = os.path.dirname(os.path.realpath(__file__))

def open_file():
    with open(args.file,'r') as jsonpath:
        obj=json.load(jsonpath)
    return obj

def match(a , b):
    a = a.lower()
    b = b.lower()
    if a in b:
        return True
    return False

def removeduplicate(list):
    seen = []
    i,k = 0,0
    t = len(list["table"])
    for x in list["table"]:
        i+=1
        k+=1
        if x not in seen:
            seen.append(x)
        if k > 5123: 
            os.system('cls' if os.name=='nt' else 'clear')
            print(f"Removing duplicates: {i}/{t}")
            k = 0
    os.system('cls' if os.name=='nt' else 'clear')
    return seen

def to_one_table(objlist):
    mergedlist = objlist[0]
    for i in range(len(objlist)):
        mergedlist["table"].extend(objlist[i]["table"])
        #mergedlist["table"].extend(removeduplicate(objlist[i]["table"]))

    mergedlist["table"] = removeduplicate(mergedlist)
    return mergedlist

def open_all_files():
    objlist = []
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for root, subdirs, files in os.walk(dir_path):
        for file in files:
            if '.json' in file:
                print(file)
                with open(file, 'r') as jsonpath:
                    obj=json.load(jsonpath)
                    objlist.append(obj)
    obj = to_one_table(objlist)
    return obj

def output_with_auth(obj):
    Data = obj["table"]
    for i in range(len(Data)):
        if "type" in Data[i]:
            name = Data[i]["type"]
            ip,port,auth = Data[i]["ip"],Data[i]["port"],None
            if "auth" in Data[i]:
                auth = Data[i]["auth"]
                print(name, ip, port, auth)   


def output_by_keyword(obj, keyword):
    Data = obj["table"]
    for i in range(len(Data)):
        if "type" in Data[i]:
            name = Data[i]["type"]
            if match(keyword, name):
            #if keyword in name:
                ip,port,auth = Data[i]["ip"],Data[i]["port"],None
                if args.auth:
                    if "auth" in Data[i]:
                        auth = Data[i]["auth"]
                        print(name, ip, port, auth)
                else:
                    if "auth" in Data[i]:
                        auth = Data[i]["auth"]                   
                    print(name, ip, port, auth)
   
def main():
    if args.file: obj = open_file()
    else: obj = open_all_files()
    if args.keyword:
        output_by_keyword(obj, args.keyword)
    elif args.auth:
        output_with_auth(obj)
    else: parser.print_help()


    

if __name__ == "__main__":
    main()
