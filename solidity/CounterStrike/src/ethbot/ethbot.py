#!/usr/bin/python3
import sys
import signal
import hashlib
import os
from Crypto.Util.number import bytes_to_long,long_to_bytes
from util import *
import random
import string
import time
from Crypto.Cipher import AES

# settings
AES_KEY = b'\xc7\\\x8c.50\xa6l\xf1t\r_J\x05\x8b\x98'
HMAC_KEY = b'D\xd5\xc00+<afH3V\xec"0\x9b#\xe7\x11se\xac\x1d^\x08\x14&G\xb2\xd3\xc6\xbbY'

alarmsecs=60
flag="flag{CoUnt3R-$TrIKe_W1N}"
seed = "ddab8023-1a25-4ce7-913b-125818a749a7"
workdir="/root/ethbot"
pow_difficult=21

MENU = '''
We design a pretty easy contract game. Enjoy it!
1. Create a game account
2. Deploy a game contract
3. Request for flag
4. Get source code
Game environment: Ropsten testnet
Option 1, get an account which will be used to deploy the contract;
Before option 2, please transfer some eth to this account (for gas);
Option 2, the robot will use the account to deploy the contract for the problem;
Option 3, use this option to obtain the flag after the event is triggered.
You can finish this challenge in a lot of connections.
'''
TOPIC = 'SendFlag'


class Unbuffered(object):
   def __init__(self, stream):
       self.stream = stream
   def write(self, data):
       self.stream.write(data)
       self.stream.flush()
   def __getattr__(self, attr):
       return getattr(self.stream, attr)
sys.stdout = Unbuffered(sys.stdout)
signal.alarm(alarmsecs)
os.chdir(workdir)


with open('eth.sol','r') as f:
    source1 = f.read()
    SRC_TEXT = source1
    CONT_IF_EasyBomb = compile_from_src(source1)['<stdin>:EasyBomb']
with open('launcher.sol','r') as f:
    source1 = f.read()
    CONT_IF_Launcher = compile_from_src(source1)['<stdin>:Launcher']

#print(CONT_IF_Launcher.keys())
# get contract source and interface


def getflag(seed, teamtoken):
    return 'flag{' + flag + '}'

def generatepow(difficulty):
    prefix = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(8))
    msg="sha256("+prefix+"+?).binary.endswith('"+"0"*difficulty+"')"
    return prefix,msg

def pow(prefix,difficulty,answer):
    hashresult=hashlib.sha256((prefix+answer).encode()).digest()
    bits=bin(int(hashlib.sha256((prefix+answer).encode()).hexdigest(),16))[2:]
    if bits.endswith("0"*difficulty):
        return True
    else:
        return False


print("=================================================================================")
print("[$] Welcome to Counter-Strike! You are cop now! Demolition bomb and get your flag!")
print("=================================================================================")
'''
prefix,msg=generatepow(5)
print("[+]",msg)
answer=input("[-] ?=")

if not pow(prefix,5,answer):
    print("[+]wrong proof")
    sys.exit(0)
print("[+] passed")
'''

print(MENU)

choice = input("[-]input your choice: ")

if choice=='1':
    # create game account
    acct = create_game_account()
    print("[+]Your game account:{}".format(acct.address))

    # save account
    with open('account.txt', 'a') as f:
        f.write(acct.address)
        f.write('\n')
        f.write(''.join(['%02X' % x for x in acct.key]))
        f.write('\n\n')

    # generate token
    data = acct.address.encode() + acct.key
    AES_KEY = AES_KEY
    HMAC_KEY = HMAC_KEY
    token = encrypt_then_mac(data, AES_KEY, HMAC_KEY)
    print("[+]token: {}".format(token))

    #source = SRC_TEXT.replace('RN', str(int.from_bytes(os.urandom(16), 'little')))
    est_gas = get_deploy_est_gas(CONT_IF_Launcher)
    print("[+]Deploy will cost {} gas".format(est_gas))
    print("[+]Make sure that you have enough ether to deploy!!!!!!")

elif choice=='2':
    token = input("[-]input your token: ")
    token=token.strip()
    AES_KEY = AES_KEY
    HMAC_KEY = HMAC_KEY
    data = validate_then_decrypt(token, AES_KEY, HMAC_KEY)
    if len(data) != 74:
        print("[+]wrong token")
        sys.exit(0)
    acct = validate_game_account(data)

    # deploy game contract
    #source = SRC_TEXT.replace('RN', str(int.from_bytes(os.urandom(16), 'little')))
    cont_if = [CONT_IF_Launcher,CONT_IF_EasyBomb]
    err, tx_hash = contract_deploy(acct, cont_if, 10**(-2))

    # check if got error when sending transaction
    if err:
        if err.args[0]['code'] == -32000:
            msg = 'Error: ' + err.args[0]['message'] + '\n'
            print("[+]{}".format(msg))
        sys.exit(0)

    # generate new token
    data = acct.address.encode() + acct.key + tx_hash
    new_token = encrypt_then_mac(data, AES_KEY, HMAC_KEY)
    print("[+]new token: {}".format(new_token))
    print("[+]Your goal is to set power_state into false in the game contract")
    print("[+]Transaction hash: {}".format(tx_hash.hex()))
elif choice=='3':
    new_token = input("[-]input your new token: ")
    new_token=new_token.strip()
    AES_KEY = AES_KEY
    HMAC_KEY = HMAC_KEY
    data = validate_then_decrypt(new_token, AES_KEY, HMAC_KEY)

    if len(data) != 106:
        print("[+]wrong token")
        sys.exit(0)

    data, tx_hash = data[:-32], data[-32:]
    acct = validate_game_account(data)
    addr = get_cont_addr(tx_hash)
    '''
    tx_hash = input("[-]input tx_hash that power_state == false")
    tx_hash = tx_hash.strip()
    '''
    res = check_if_has_topic(addr, tx_hash, CONT_IF_EasyBomb , TOPIC)
    #print(res)
    if res:
        team_token = input("[-]input your team token: ").strip()
        assert len(team_token) == 32 and team_token.startswith('icq')
        flag = getflag(seed,team_token)
        with open("address.txt",'a') as f:
            f.write(tx_hash + ' ' + team_token + ' ' + flag)
            f.write('\n')
        print("[+]flag:"+flag)
    else:
        print("[+]sorry, it seems that you have not solved this~~~~")
elif choice=='4':
    print(SRC_TEXT.replace('RN', '0'))
else:
    print("Invalid option")
    sys.exit(0)
