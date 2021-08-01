
import requests
import json
import re
import os
import time

## why are these orange?
INPUT_FILE=""
OUTPUT_FOLDER = ""
WPF=10
API_KEY=""
API_ID=""

def init(config="settings.json"):
    f = open(config, "r")
    as_json = json.loads(f.read())
    global API_ID 
    API_ID = get_json_attr(as_json, 'apiid')
    global API_KEY
    API_KEY = get_json_attr(as_json, 'apikey')
    global WPF
    WPF = get_json_attr(as_json,'words_per_file')
    global INPUT_FILE
    INPUT_FILE = get_json_attr(as_json, 'input_file')
    global OUTPUT_FOLDER
    OUTPUT_FOLDER = get_json_attr(as_json, 'output_folder')

    f.close()

def get_json_attr(json, attr, mand=True):
    try:
        return json[attr]
    except KeyError:
        if (mand):
            print("ERROR: Expected JSON attribute \"{}\", but no such attribute was provided".format(attr))
            print("Aborting . . . ")
            exit()
        else:
            print("Nonmandatory attribute {} not found".format(attr))


def req_word(word):
    ## the global references are actually wholly unnecessary
    global API_ID
    global API_KEY
    language = "en-gb"
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word.lower()
    r = requests.get(url, headers={"app_id": API_ID, "app_key": API_KEY})
    return r

def get_def(resjson):
    try:
        def_arr = resjson['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['definitions']
        return def_arr
    except:
        return []

def get_syn(resjson):
    try:
        syn_arr = resjson['results'][0]['lexicalEntries'][0]['entries'][0]['senses'][0]['synonyms']
        syn_arr2 = [y['text'] for y in syn_arr]
        return syn_arr2
    except:
        return []

## precondition that res is status code 200
def form_def(word, res):
    if (res.status_code != 200):
        print("Failed to retrieve the word \"{}\"".format(word))
        return None
    as_json = json.loads(res.text)
    d = get_def(as_json)
    s = get_syn(as_json)
    if (len(d) > 2):
        d = [d[0], d[1]]
    if (len(s) > 2):
        s = [s[0], s[1]]
    fin_txt = "(" + ", ".join(s) + ") " + ";".join(d)
    return fin_txt

def get_word_list(fname):
    try:
        f = open(fname, "r")
        t = f.read()
        ## replace all linebreaks and commas surrounded by whitespace with a 
        t = (re.sub("\s+[,\\n ]+\s+","\n", t)).strip()
        f.close()
        return t.split("\n")

    except FileNotFoundError:
        print("Failed to retrieve input file \"{}\"".format(fname))
        print("Aborting . . . ")
        exit()




def run():
    init()
    word_list = get_word_list(INPUT_FILE)
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
    words = 0
    fileno = 0
    fileref = open(OUTPUT_FOLDER+"/output"+str(fileno)+".tsv", "w")
    for word in word_list:
        time.sleep(1)
        res = req_word(word)
        defin = form_def(word, res)
        line = word + "\t" + str(defin) + "\n"
        fileref.write(line)
        print("Completed writing the word {}".format(word))
        words+=1
        if (words%WPF==0):
            print("Completed writing in file number {}".format(fileno))
            fileno+=1
            fileref.close()
            fileref = open(OUTPUT_FOLDER+"/output"+str(fileno)+".tsv", "w")
    print("Completed writing {} words".format(words))
            

run()