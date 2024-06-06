import regex,re

def getSentences(text:str,onlyReturnFull:bool=True):
    # try:
        s=regex.split(r'(?<!(Mr|Ms|Mrs|St|Dr|Gov|[0-9]|\n[A-z]|\.|!|\?))(\.|\?|!) ',text)
        sentences=[]
        for x in range(0,len(s)-2,3):
            sentences.append((s[x]+s[x+2]).replace('**',''))
        sentences.append(s[-1])
        if onlyReturnFull:
            if sentences[-1][-1] not in ['.','?','!']:
                sentences=sentences[:-1]
        return sentences
    # except Exception as e:
    #     print(e)
    #     return []
def getNoises(text:str)->list[str]:
     return re.split(r'(\*.*\*|chipi chipi chapa chapa dubi dubi daba daba ________ boom boom boom boom)',text)


if __name__=='__main__':
    print(getNoises('no'))