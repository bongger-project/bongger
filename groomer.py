#!/usr/bin/python
# simple cleanup script, 2012-12-25 <greg@xiph.org>
import sys
import operator
from decimal import *
from jsonrpc import ServiceProxy

if len(sys.argv)<3:
    
  print ('Usage %s http://user:password@127.0.0.1:8332/ [fee]'%(sys.argv[0]))
  print ('This script generates a transaction to cleanup your wallet.')
  print ('  It looks for the single addresses which have the most small confirmed payments made to them and merges')
  print ('   all those payments, along with those for any addresses which are all tiny payments, to a single txout.')
  print ('  It must connect to bitcoin to inspect your wallet and to get fresh addresses to pay your coin to.')
  print ('  This script doesn\'t sign or send the transaction, it only generates the raw txn for you.')
else:
  try:
    b = ServiceProxy(sys.argv[1])
    b.getinfo()
  except: 
    print ("Couldn't connect to bitcoin")
    exit(1)
  min_fee=Decimal(sys.argv[2])

  #Add up the number of small txouts and amounts assigned to each address.
  coins=b.listunspent(1,99999999)
  scripts={}
  for coin in coins:
    script=coin['scriptPubKey']
    if script not in scripts:
      scripts[script]=(0,Decimal(0),0)
    if (coin['amount']<Decimal(25) and coin['amount']>=Decimal(0.01) and coin['confirmations']>100):
      scripts[script]=(scripts[script][0]+1,scripts[script][1]+coin['amount'],scripts[script][0]+1)
    else:
      scripts[script]=(scripts[script][0],scripts[script][1]+coin['amount'],scripts[script][0]+1)

  #which script has the largest number of well confirmed small but not dust outputs?
  most_overused = max(scripts.iteritems(), key=operator.itemgetter(1))[0]

  #If the best we can do doesn't reduce the number of txouts or just moves dust, give up.  
  if(scripts[most_overused][2]<3 or scripts[most_overused][1]<Decimal(0.01)):
    print ("Wallet already clean.")
    exit(0)
    
  usescripts=set([most_overused])

  #Also merge in scripts that are all dust, since they can't be spent without merging with something.
  for script in scripts.keys():
    if scripts[script][1]<Decimal(0.00010000):
      usescripts.add(script)
  
  amt=Decimal(0)
  txouts=[]
  for coin in coins:
    if coin['scriptPubKey'] in usescripts:
      amt+=coin['amount']
      txout={}
      txout['txid']=coin['txid']
      txout['vout']=coin['vout']
      txouts.append(txout)
  print ('Creating tx from %d inputs of total value %s:'%(len(txouts),amt))
  for script in usescripts:
    print ('  Script %s has %d txins and %s BTC value.'%(script,scripts[script][2],str(scripts[script][1])))

  out={}
  na=amt-min_fee
  #One new output per 100 BTC of value to avoid consolidating too much value in too few addresses. 
  # But don't add an extra output if it would have less than 10 BTC.
  while na>0:
    amount=min(Decimal(100),na)
    if ((na-amount)<10):
      amount=na
    addr=b.getnewaddress('consolidate')
    #omg wtf, this is awful. the python-bitcoin crap makes the argument be a float
    if (Decimal(str(float(amount)))>0):
      if addr not in out:
        out[addr]=float(0)
      out[addr]+=float(amount)
    na-=Decimal(str(float(amount)))
  print ('Paying %s BTC (%s fee) to:'%(sum([Decimal(str(out[k])) for k in out.keys()]),amt-sum([Decimal(str(out[k])) for k in out.keys()])))
  for o in out.keys():
    print ('  %s %s'%(o,out[o]))
  
  txn=b.createrawtransaction(txouts,out)
  print ('\nRaw transaction, sign with signrawtransaction then send with sendrawtransaction:')
  print ('If, after signing, transaction is too large (e.g. >20,000 character) you may need to provide a fee or it will be rejected by bitcoin.\n')
  print (txn)

#This could sign and send the transaction, but better to let the user do it.
#  txn=b.signrawtransaction(txn)
#  print (txn)
#  print ('Bytes: %d Fee: %s'%(len(txn['hex'])/2,amt-sum([Decimal(str(out[x])) for x in out.keys()])))
