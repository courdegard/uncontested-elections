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
 # print("buildAddr called")
  queryAddr=address['line1']
  if 'line2'in address:
    queryAddr=queryAddr+" "+address['line2']
    if 'line3' in address:
      queryAddr=queryAddr+" "+address['line3']
  queryAddr=queryAddr+","+address['city']+","+address['state']+","+address['zip']
  return queryAddr

def capCheck(city):
  capDict={}
  with open(r'C:\Users\daniel\Documents\Projects\uncontested-elections\state_capitals.txt') as capitals:
    for capital in capitals: 
      capDict[capital.strip()]=1 
  print(type(city))
  if city in capDict: return True
  else: return False

def stateCheck(addr):
  stateDict={}
  with open(r'C:\Users\daniel\Documents\Projects\uncontested-elections\state_abbrevs.txt') as states:
    for state in states: 
      stateDict[state.split(',')[0]]=state.split(',')[1].strip()
  if 'state' in addr: 
    print(addr['state'])
    return 1
  # and addr['state']!='WI' or addr['state']!='Wisconsin': 
  else:  
    print("No state")
    return 0

#  addrCall=requests.get(url="https://maps.googleapis.com/maps/api/place/textsearch/json?query=?"+queryAddr+"&key=AIzaSyCE0n694rfivKPxfFe67FmNnMdnnD4S2fs").json()

# divs: a list of divisions from divQuery in main
# returns divResults: dictionary of division names (keys)
# and data on uncontested elections for addresses in those divisions (values)

def divLoop(divs): 
  print("DIV LIST")
  print(divs[0])
  divResults={}
  for div in divs:
    foundReps=civicQuery('reps',ocdId=div['ocdId'])
    if 'officials' in foundReps: 
      divResults[div['name']]=officialLoop(foundReps['officials'])
  return divResults

def checkUncontested(contest):
  if 'candidates' in contest:
    if len(contest['candidates'])==1: return True
  return False
# params: 
# repList: a list of representatives in a political division
# returns a cleaned list of addresses for the representatives in a political division 
# (cleanAddrList(officialAddrList))
def officialLoop(repList):
  officialAddrList=[]
  print("OFFICIALS LIST")
  print(repList[0])
  for official in repList:
    if 'address' in official: officialAddrList.append(official['address'])
  return cleanAddrList(officialAddrList)

def makeStates():
  stateList=[]
  with open('/home/db/Documents/uncontested_elections/states') as states:
    for state in states:stateList.append(state.strip())
  return stateList

# Params: addrs: a list of lists of dictionaries
# Returns a list of dictionaries pluckedAddrs
def pluckAddrs(addrs):
  pluckedAddrs=[]
  for addr in addrs:
    for dAddr in addr:
      pluckedAddrs.append(dAddr)
  return pluckedAddrs

# params:
# addrs: a list of lists of dictionaries containing addresses for representatives in political division
# returns list of dictionaries with data on uncontested elections 
def cleanAddrList(addrs):
  print("DIRTY ADDR LIST")
  foundCap=False
  cleanList=[]
  idx=0
  pluckedAddrs=pluckAddrs(addrs)
  num=len(pluckedAddrs)
  print(num)
  while foundCap is False and idx<len(pluckedAddrs):
    print(pluckedAddrs[idx])
    if stateCheck(pluckedAddrs[idx])==1: 
      print(idx)
      foundCap=capCheck(pluckedAddrs[idx]['city'])
      cleanList.append(buildAddr((pluckedAddrs[idx])))
    idx+=1
  while idx<len(pluckedAddrs):
    print(idx)
    if capCheck(pluckedAddrs[idx]['city']) is False: cleanList.append(buildAddr((pluckedAddrs[idx])))
    idx+=1
  return contestLoop(cleanList)

def contestLoop(cleanAddrs):
  print("CLEAN ADDR LIST")
  if cleanAddrs==[]: return False
  print(cleanAddrs[0])
  contestList=[]
  for addr in cleanAddrs:
    voterInfo=civicQuery('vote',addr)
    if 'contests' in voterInfo: 
      contestList.append(candidateLoop(voterInfo['contests']))
  return contestList

def candidateLoop(contests):
  print("CONTEST LIST")
  print(contests[0])
  for contest in contests: 
    if checkUncontested(contest)==True:
      return contest['candidates']
    else: return 'None'
      
def main():
  divQuery=civicQuery('divs','wisconsin')
  divUncontested=divLoop(divQuery['results'])
  for key in divUncontested: print(divUncontested[key])
  quit 

main()

