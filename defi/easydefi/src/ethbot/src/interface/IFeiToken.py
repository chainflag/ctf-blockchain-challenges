from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r
from src.utils.utils import update_user_deploy_contracts
from conf.base import chainId

# mint
def mintfeitoken(ctx, _contract, _to_address, _amount, _from, _acc_nonce):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['feitoken']['abi'])
	construct_tx = store_var_contract.functions.mint(_to_address, _amount).buildTransaction(
		{'chainId': chainId,
		'from': _from.address,
		'nonce': _acc_nonce[0],
		'gasPrice': 60000000000,
		'gas': 3000000
		#'value': w3.toWei(value, 'ether'),
		})
	try:
		signed_tx = _from.signTransaction(construct_tx)
		tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
		_acc_nonce[0] += 1
	except Exception as err:
		return err, None
	return None, tx_hash


def mint(ctx, _contract, _to_address, _amount, _acct, _acc_nonce):
	if 'mintfeitoken' not in ctx['deployedcontracts'][_acct.address].keys():
		p.ppln("[-] try to mintfeitoken to deployer...")
		err, txhash = mintfeitoken(ctx, _contract, _to_address, _amount, _acct, _acc_nonce)
		if err:
			p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
			exit(0)
		else:
			update_user_deploy_contracts(ctx, _acct.address, 'mintfeitoken', txhash.hex())
			return None, txhash.hex()
	else:
		txhash = ctx['deployedcontracts'][_acct.address]['mintfeitoken']
		return None, txhash


def mint_review(ctx, _acct, _txhash):
	w3 = ctx['web3instance']
	p.ppln("[-] Check for mintfeitoken successful... ")
	try:
		tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
	except Exception as err:
		p.ppln(str(err))
		exit(0)
	addr = tx_receipt['transactionHash'].hex()

	if not addr:
		p.pln(p.in_fg_color("[!] mintfeitoken Broken down", r.red5))
	else:
		p.ppln("[+] mintfeitoken " + p.in_fg_color("success", r.green1))
		p.ppln("[!] mintfeitoken transaction hash is " + p.in_fg_color(addr, r.blue1))


# approve
def approvefeitoken(ctx, _contract, _to, _amount, _from, _acc_nonce):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['feitoken']['abi'])
	p.ppln(" approve transaction init success")
	construct_tx = store_var_contract.functions.approve(_to, _amount).buildTransaction(
		{'chainId': chainId,
		'from': _from.address,
		'nonce': _acc_nonce[0],
		'gasPrice': 60000000000,
		'gas': 3000000
		#'value': w3.toWei(value, 'ether'),
		})
	p.ppln(" approve transaction build success")
	try:
		signed_tx = _from.signTransaction(construct_tx)
		tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
		_acc_nonce[0] += 1
		p.ppln(" approve transaction send success")
	except Exception as err:
		return err, None
	return None, tx_hash
#==============================================================#

def approve(ctx, _contract, _to, _amount, _acct, _acc_nonce):
	if 'approvefeitoken' not in ctx['deployedcontracts'][_acct.address].keys():
		p.ppln("[-] try to approvefeitoken to deployer...")

		err, txhash = approvefeitoken(ctx, _contract, _to, _amount, _acct, _acc_nonce)
		if err:
			p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
			exit(0)
		else:
			update_user_deploy_contracts(ctx, _acct.address, 'approvefeitoken', txhash.hex())
			return None, txhash.hex()
	else:
		txhash = ctx['deployedcontracts'][_acct.address]['approvefeitoken']
		return None, txhash


def approve_review(ctx, _acct, _txhash):
	w3 = ctx['web3instance']
	p.ppln("[-] Check for approvefeitoken successful... ")
	try:
		tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
	except Exception as err:
		p.ppln(str(err))
		exit(0)
	addr = tx_receipt['transactionHash'].hex()

	if not addr:
		p.pln(p.in_fg_color("[!] approvefeitoken Broken down", r.red5))
	else:
		p.ppln("[+] approvefeitoken " + p.in_fg_color("success", r.green1))
		p.ppln("[!] approvefeitoken transaction hash is " + p.in_fg_color(addr, r.blue1))
