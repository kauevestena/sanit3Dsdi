import os, requests, hashlib


def joinToHome(input_path):
    """
    join a relative path to the home path
    """
    return os.path.join(os.environ['HOME'],input_path.strip('/'))

def create_dir_ifnot_exists(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def createDirs(dirList):
    for dirPath in dirList:
        create_dir_ifnot_exists(dirPath)

def list_dump(input_list,outpath,mode='w+'):
    with open(outpath,mode) as list_writer:
        for item in input_list:
            list_writer.write(str(item)+'\n')

def get_hash_from_text_in_url(url):
    textstring = requests.get(url).text
    return hash_string(textstring)


def hash_string(inputstr):
    hasher = hashlib.sha256()
    hasher.update(inputstr.encode())
    return hasher.hexdigest()

def select_entries_with_string(inputlist,inputstring):
    return [entry for entry in inputlist if inputstring in entry]
