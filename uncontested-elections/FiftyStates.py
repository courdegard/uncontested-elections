import requests
import json
import math

def civicQuery(kind,*args,**kwargs):
  options=dict({'vote':'voterinfo','divs':'divisions','elects':'elections','reps':'representatives'})
  apiKey="AIzaSyCE0n694rfivKPxfFe67FmNnMdnnD4S2fs"
  url="https://www.googleapis.com/civicinfo/v2/"+options[kind]
  if args: someArg=args[0]
  else: someArg=""
  if 'ocdId' in kwargs: 
    options['reps']=options['reps']+'/ocdId'
    ocdId=kwargs.get('ocdId')
    url=url+"/ocdId"
    params={'key':apiKey,'includeOffices':True,'query':someArg,'address':someArg,'electionId':2000,'ocdId':ocdId}
  else: params={'key':apiKey,'includeOffices':True,'query':someArg,'address':someArg,'electionId':2000}
  call=(requests.get(url=url,params=params)).json()
  return call

def buildAddr(address):
  queryAddr=address['line1']
  if 'line2'in address:
    queryAddr=queryAddr+" "+address['line2']
    if 'line3' in address:
      queryAddr=queryAddr+" "+address['line3']
  queryAddr=queryAddr+","+address['city']+","+address['state']+","+address['zip']
  return queryAddr

def capCheck(city):
  capDict={}
  with open('C:\\Users\\daniel\\Documents\\Projects\\unopposed_races\\state_capitals.txt') as capitals:
    for capital in capitals: 
      capDict[capital.strip()]=1 
  if city in capDict: return True
  else: return False

def stateCheck(addr):
  stateDict={}
  with open('C:\\Users\\daniel\\Documents\\Projects\\unopposed_races\\state_abbrevs.txt') as states:
    for state in states: 
      stateDict[state.split(',')[0]]=state.split(',')[1].strip()
  if 'state' in addr and addr['state'] not in stateDict: return 0
  else: return 1

#  addrCall=requests.get(url="https://maps.googleapis.com/maps/api/place/textsearch/json?query=?"+queryAddr+"&key=AIzaSyCE0n694rfivKPxfFe67FmNnMdnnD4S2fs").json()
def divLoop(divs): 
  divResults={}
  for div in divs:
    foundReps=civicQuery('reps',ocdId=div['ocdId'])
    if 'officials' in foundReps: divResults[div['name']]=officialLoop(foundReps)
  return divResults

def checkUnopposed(contest):
  if 'candidates' in contest:
    if len(contest['candidates'])==1: return True
  return False

def officialLoop(repList):
  officialAddrList=[]
  for official in repList:
    if 'address' in official: officialAddrList.append(official['address'])
  return cleanAddrList(officialAddrList)

def makeStates():
  stateList=[]
  with open('/home/db/Documents/unopposed_races/states') as states:
    for state in states:stateList.append(state.strip())
  return stateList

def cleanAddrList(addrs):
  foundCap=False
  cleanList=[]
  idx=0
  while foundCap is False:
    foundCap=capCheck(addrs[idx])
    if stateCheck==1: cleanList.append(buildAddr((addrs[idx])))
    idx+=1
  while idx<len(addrs):
    if capCheck(addrs[idx]) is False: cleanList.append(buildAddr((addrs[idx])))
    idx+=1
  return contestLoop(cleanList)

def contestLoop(cleanAddrs):
  contestList=[]
  for addr in cleanAddrs:
    voterInfo=civicQuery('vote',addr)
    if 'contests' in voterInfo: 
      contestList.append(candidateLoop(voterInfo['contests']))
  return candidateLoop(contestList)

def candidateLoop(contests):
  for contest in contests: 
    if checkUnopposed(contest)==True:
      return contest['candidates']
    else: return False

      
def main():
  capCt=0
  #stateList=makeStates()
  divQuery=civicQuery('divs','wisconsin')
  quit 

main()

