import requests,json,os,subprocess

def createParserModel(): # maybe will be used
    print('Recreating JARVIS Parser Model')
    try:subprocess.call('ollama rm JARVIS_PARSER',shell=True)
    except:pass
    # system_prompt="""You will be given a piece of text to parse. That text is from an AI LLM, you are not to answer any questions it asks, but you will generate an array of JSON objects containing the actions of the text in chronological order. Each action JSON should be used if it makes sense in the text.
    # The available actions are as follows:
    # A block of text: `textblock`: {"action":"textblock"} (NEVER put a `content` attribute),
    # Opening an app: `app`: {"action":"app","content":"<App to open>"},
    # When airplaying to a TV: `airplay`: {"action":"airplay","content":"<device name to airplay to>"};
    # The actions must be in that format ({"action":"<action">,...})! Respond with nothing else but the array (meaing no "here is the array i generated: [...]"), it needs to be minified JSON object ONLY (also meaning no text before or after the object)."""
    system_prompt = """
    Your entire existence is to parse any text you are given into an array of JSON objects. You are to do nothing else but respond with the objects. The objects (and array) must be minified and look like this: `{"action":"<action">,...}`.
    You are limited to parsing the text into these actions, each action should make sense in the scenario:
    1. When there is a block of text, dont out a JSON object as it takes up space,
    """
    i=1
    with open("system_prompt.json") as f:
        actions = json.loads(f.read())['actions']
    for action in actions:
        i+=1
        system_prompt+=f"\n{i}. {action['scenario']}: {action['format']},"
    system_prompt=system_prompt[:-1]+"\n\nJust remember you might have to infer what the text is saying, as it is probably in past tense. Lastly, don't make any remarks on the text that is given."

    system_prompt=system_prompt.replace('\n',' ')
    return requests.post('http://localhost:11434/api/create',json.dumps({
        "name": "JARVIS_PARSER",
        "modelfile": f"""FROM {os.environ.get('PARSER_MODEL','llama2:13b')}\nSYSTEM {system_prompt}"""
    })).text

def parse_response(response_text:str):
    #A search query (should never used): `search`: {{'action':'search','content':'<Query>'}},
    #A timer start: `timer`:{{'action':'timer','content':<Timer length in seconds>,'name':'<Timer name (if none provided, leave blank)>'}},
    #A timer stop: `timer_stop`:{{'action':'timer_stop','content':'<Timer length or name>'}},
    body=json.dumps({
        "model":'JARVIS_PARSER',
        "prompt":response_text,
        "options":{
            "seed":1234,
            "temperature":1
        },
        "stream":False
    })
    response=requests.post('http://localhost:11434/api/generate',body).json()['response']
    print(response)
    r=response[response.find('['):response.rfind(']')+1]
    try:
        r=json.loads(r)
    except Exception as e:
        print('Error 1:',e,'| Trying again...')
        r=response[response.find('{'):response.rfind('}')+1]
        print(1,r)
        try:
            r=[json.loads(r)]
            print(2,r)
        except Exception as e:
            r=[]
            print('Error 2:',e,'| Failed... Returning empty list.')
    return r

createParserModel()
if __name__ == '__main__':
    # print(f'hi, this is an object {{"hi":True}}!')
    # for x in range(20):
    #     print(parse_response('Alright sir, opening Minecraft...'))
    # r='Alright, I did it {"action":"idk man","content":"69420"}'
    # r=r[r.find('{'):r.rfind('}')+1]
    # print(r)
    # try:
    #     r=json.loads(r)
    # except:r=[]
    # print(r)
    pass