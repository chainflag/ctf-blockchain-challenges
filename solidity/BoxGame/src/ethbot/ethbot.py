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
AES_KEY = "1d45c47a3819decc5f5e1bb6c6d3b66e"
HMAC_KEY = "4263d309bddb3c5509095f496cbcc5f7121a80c1bfab8aee534b70166c912a9e"

alarmsecs=60
flag="flag{0h_Fantansitic_Congratulation_t0_U_to_master_bytec0de}"
# seed = "ccbc8023-1b25-5ce8-913c-125890a749a7"
workdir="/root/ethbot"
pow_difficult=21

MENU = '''
We design a pretty easy contract game. Enjoy it!
1. Create a game account
2. Deploy a game contract
3. Request for flag
4. Get source code
Game environment: ropsten testnet

Option 1, get an account which will be used to deploy the contract;
Before option 2, please transfer some eth to this account (for gas);
Option 2, the robot will use the account to deploy the contract for the problem;
Option 3, use this option to obtain the flag after emit ForFlag(address addr) event.
Option 4, use this option to get source code.
You can finish this challenge in a lot of connections.
'''
TOPIC = 'ForFlag'


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

# get contract source and interface
with open('./eth.sol', 'r') as f:
    SRC_TEXT = f.read()
CONT_IF = compile_from_src(SRC_TEXT.replace('RN', '0'))

def getflag(seed, teamtoken):
    token=teamtoken
    real_flag=hashlib.md5((seed+'&'+hashlib.sha1(token[::-1].encode()).hexdigest()[:10]).encode()).hexdigest()
    return 'flag{' + real_flag + '}'

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


# prefix,msg=generatepow(20)
# print("[+]",msg)
# answer=input("[-] ?=")

# if not pow(prefix,20,answer):
#     print("[+]wrong proof")
#     sys.exit(0)
# print("[+] passed")



print(MENU)

choice=input("[-]input your choice: ")

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
    AES_KEY = str.encode(AES_KEY)
    HMAC_KEY = str.encode(HMAC_KEY)
    token = encrypt_then_mac(data, AES_KEY, HMAC_KEY)
    print("[+]token: {}".format(token))

    # source = SRC_TEXT.replace('RN', str(int.from_bytes(os.urandom(16), 'little')))
    # cont_if = compile_from_src(source)
    # est_gas = get_deploy_est_gas(cont_if)
    # print("[+]Deploy will cost {} gas".format(est_gas))
    print("[+]Make sure that you have enough ether to deploy!!!!!!")

elif choice=='2':
    token = input("[-]input your token: ")
    token=token.strip()
    AES_KEY = str.encode(AES_KEY)
    HMAC_KEY = str.encode(HMAC_KEY)
    data = validate_then_decrypt(token, AES_KEY, HMAC_KEY)
    if len(data) != 74:
        print("[+]wrong token")
        sys.exit(0)
    acct = validate_game_account(data)

    # deploy game contract
    source = SRC_TEXT.replace('RN', str(int.from_bytes(os.urandom(16), 'little')))
    cont_if = compile_from_src(source)
    err, tx_hash = contract_deploy(acct, cont_if, 0)

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
    print("[+]Your goal is to emit ForFlag(address addr) event in the game contract")
    print("[+]Transaction hash: {}".format(tx_hash.hex()))
elif choice=='3':
    new_token = input("[-]input your new token: ")
    new_token=new_token.strip()
    AES_KEY = str.encode(AES_KEY)
    HMAC_KEY = str.encode(HMAC_KEY)
    data = validate_then_decrypt(new_token, AES_KEY, HMAC_KEY)

    if len(data) != 106:
        print("[+]wrong token")
        sys.exit(0)

    data, tx_hash = data[:-32], data[-32:]
    acct = validate_game_account(data)
    addr = get_cont_addr(tx_hash)

    tx_hash = input("[-]input tx_hash that emitted {} event: ".format(TOPIC))
    tx_hash = tx_hash.strip()
    res = check_if_has_topic(addr, tx_hash, CONT_IF, TOPIC)
    if res:
        with open("address.txt",'a') as f:
            f.write(tx_hash)
            f.write('\n')
        print("[+]flag:"+flag)
    else:
        print("[+]sorry, it seems that you have not solved this~~~~")
elif choice=='4':
    print(SRC_TEXT.replace('RN', '0'))
else:
    print("Invalid option")
    sys.exit(0)
