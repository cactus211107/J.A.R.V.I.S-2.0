import requests,os,datetime,json,random,shutil,subprocess
from string import ascii_letters,digits
def join(b,*p):return os.path.join(b,*p)

CHATS_PATH=os.environ['CHATS_FOLDER']


def createJARVISModel(base_model:str=os.environ['BASE_LLM']):
    print('Recreating JARVIS Model')
    try:subprocess.call('ollama rm JARVIS',shell=True)
    except:pass
    with open("system_prompt.json") as f:
        content = json.loads(f.read())
    JARVIS_PERSONALITY=content['personality']
    INFORMATION=content['extra_information']
    system_prompt=f"""[INST]{JARVIS_PERSONALITY}. Extra Information if needed is as follows: {INFORMATION} Good luck![/INST]""".replace('\n',' ')
    # print(system_prompt)
    return requests.post('http://localhost:11434/api/create',json.dumps({
        "name": "JARVIS",
        "modelfile": f"""FROM {base_model}\nSYSTEM {system_prompt}"""
    })).text
def getChat(chatid:str):
    with open(join(CHATS_PATH,chatid,'data.json')) as f:return json.loads(f.read())
def deleteChat(chatid:str):shutil.rmtree(join(CHATS_PATH,chatid))
def deleteAllChats():shutil.rmtree(CHATS_PATH)
def createChat():
    date=datetime.datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
    chat_id=''.join(random.choices(ascii_letters+digits, k=16))
    chat_path=join(CHATS_PATH,chat_id)
    os.makedirs(join(chat_path,'media'))
    os.makedirs(join(chat_path,'history','audio','ai'))
    os.makedirs(join(chat_path,'history','audio','human'))
    with open(join(chat_path,'history','history.md'),'w') as f:
        f.write('# History')
    with open(join(chat_path,'history','function_history.md'),'w') as f:
        f.write('# FN History')
    with open(join(chat_path,'data.json'),'w') as f:
        f.write(json.dumps({
            "created":date,
            "summary":"",
            "messages":[]
            }))
    os.environ['CURRENT_CHAT']=chat_id
    return chat_id
def addMessageToChat(msg:dict,chatid:str):
    with open(join(CHATS_PATH,chatid,'data.json'),'r+') as f:
        content = getChat(chatid)
        content['messages'].append(msg)
        f.write(json.dumps(content))
    with open(join(CHATS_PATH,chatid,'history','history.md'),'a') as f:
        f.write(f"{'User' if msg['role']=='user' else 'JARVIS'}: {msg['content']}")
def callChatAPI(messages:list[dict]):
    body=json.dumps({
        "model":"JARVIS",
        "messages":messages,
        "stream":True
    })
    return requests.post('http://localhost:11434/api/chat',body,stream=True)
def getMostRecentChat():
    folders = [join('chat', d) for d in os.listdir(CHATS_PATH) if os.path.isdir(join('chat', d))]
    if not folders:return None
    return getChat(max(folders, key=os.path.getmtime))
def interact(message:str,chatid:str):
    addMessageToChat({
        "role":"user",
        "content":message,
    },chatid)
    return callChatAPI(getChat(chatid)['messages'])
def initiateChat(chatid:str):
    interact("Welcome to the world, J.A.R.V.I.S!",chatid) # (Just A Rather Very Intelligent System)
    addMessageToChat({
        "role":"assistant",
        "content":"Hello Sir, what can do for you today?"
    },chatid)
    print('JARVIS LLM is running.')