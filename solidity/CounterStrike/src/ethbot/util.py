from web3 import Web3, WebsocketProvider
from web3.middleware import geth_poa_middleware
from solcx import compile_source,compile_files
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import hashlib
import hmac
import os

# connect to node
#INFURA_PROJ_ID = os.environ['INFURA_PROJ_ID']
w3 = Web3(Web3.HTTPProvider("https://ropsten.infura.io/v3/af5a1d6c6ae04585b340adc84718a3c4"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

# aes and hmac
def encrypt_then_mac(data, aes_key, hmac_key):
	cipher = AES.new(aes_key, AES.MODE_CBC)
	# print(type(pad(data, AES.block_size)))
	msg = cipher.iv + cipher.encrypt(pad(data, AES.block_size))
	sig = hmac.new(hmac_key, msg, hashlib.sha256).digest()
	token = b64encode(msg + sig).decode()
	return token

def validate_then_decrypt(token, aes_key, hmac_key):
	s = b64decode(token)
	msg, sig = s[:-32], s[-32:]
	assert sig == hmac.new(hmac_key, msg, hashlib.sha256).digest()
	iv, ct = msg[:16], msg[16:]
	cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
	data = unpad(cipher.decrypt(ct), AES.block_size)
	return data

# solc
def compile_from_src(source):
	compiled_sol = compile_source(source)
	return compiled_sol


# web3
def get_deploy_est_gas(cont_if):
	instance = w3.eth.contract(
		abi=cont_if['abi'],
		bytecode=cont_if['bin']
	)
	return instance.constructor().estimateGas()

def get_cont_addr(tx_hash):
	tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
	assert tx_receipt != None
	return tx_receipt['contractAddress']

def contract_deploy(acct, cont_if, value):
	instance = w3.eth.contract(
		abi=cont_if[0]['abi'],
		bytecode=cont_if[0]['bin']
	)
	addr = ""
	construct_tx = instance.constructor().buildTransaction(
		{'chainId': 3,
		'from': acct.address,
		'nonce': w3.eth.getTransactionCount(acct.address),
		'gasPrice': w3.eth.gasPrice*10
		#'value': w3.toWei(value, 'ether'),
		})
	try:
		signed_tx = acct.signTransaction(construct_tx)
		tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
	except Exception as err:
		return err, None
	tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
	addr = tx_receipt['contractAddress']
	
	instance = w3.eth.contract(
		abi=cont_if[1]['abi'],
		bytecode=cont_if[1]['bin']
	)
	'''
	w3.geth.personal.unlock_account(acct.address,"aHardPassword")
	tx_hash = instance.constructor(addr,"0x000000000000666c61677b646f6e4c65745572447265616d4265447265616d7d").transact({'from':acct.address})
	return tx_hash
	'''
	
	construct_tx = instance.constructor(addr,bytes.fromhex("000000000000666c61677b646f6e4c65745572447265616d4265447265616d7d")).buildTransaction(
		{'chainId': 3,
		'from': acct.address,
		'nonce': w3.eth.getTransactionCount(acct.address),
		'gasPrice': w3.eth.gasPrice*10
		#'value': w3.toWei(value, 'ether'),
		})
	addr = addr.replace('0x','')
	construct_tx['data'] = "0x608060405260008060006101000a81548160ff0219169083151502179055506001600260006101000a81548160ff02191690831515021790555034801561004557600080fd5b5060405161047d38038061047d8339818101604052604081101561006857600080fd5b81019080805190602001909291908051906020019092919050505081600060016101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055508060018190555050506103a1806100dc6000396000f3fe608060405234801561001057600080fd5b50600436106100415760003560e01c80632719a334146100465780635844aeb8146100685780635c2ed85414610096575b600080fd5b61004e6100b4565b604051808215151515815260200191505060405180910390f35b6100946004803603602081101561007e57600080fd5b81019080803590602001909291905050506100c7565b005b61009e6102fb565b6040518082815260200191505060405180910390f35b600260009054906101000a900460ff1681565b6001546100d26102fb565b146100dc57600080fd5b3273ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff16141561011557600080fd5b6000333b90506000811461012857600080fd5b600060019054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600260016101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff160217905550600260019054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff166329dcb0cf6040518163ffffffff1660e01b815260040160206040518083038186803b1580156101f357600080fd5b505afa158015610207573d6000803e3d6000fd5b505050506040513d602081101561021d57600080fd5b8101908080519060200190929190505050431061023957600080fd5b60016000806101000a81548160ff0219169083151502179055503373ffffffffffffffffffffffffffffffffffffffff16ff5b6020831061028f578051825260208201915060208101905060208303925061026c565b6001836020036101000a038019825116818451168082178552505050505050905001915050600060405180830381855af49150503d80600081146102ef576040519150601f19603f3d011682016040523d82523d6000602084013e6102f4565b606091505b5050505050565b600060606000368080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f82011690508083019250505050505050905060008151141561035d576000801b915050610369565b60246020018101519150505b9056fea265627a7a723158205c2723cfd7ec5fe8630177ed681731a8717cf0176ca1d650aa35b3dd70339d6564736f6c63430005100032000000000000000000000000" + addr + "000000000000666c61677b646f6e4c65745572447265616d4265447265616d7d"
	
	try:
		signed_tx = acct.signTransaction(construct_tx)
		tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
	except Exception as err:
		return err, None
	return None,tx_hash



def check_if_has_topic(addr, tx_hash, cont_if, topic):
	ret = w3.eth.getStorageAt(addr,2)
	return ret == b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'

# game account
def create_game_account():
	acct = w3.eth.account.create("aHardPassword")
	return acct

def validate_game_account(data):
	addr, priv_key = data[:-32], data[-32:]
	acct = w3.eth.account.from_key(priv_key)
	assert acct.address.encode() == addr
	return acct
