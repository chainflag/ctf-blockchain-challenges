from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r
from src.utils.utils import update_user_deploy_contracts
from conf.base import chainId

# mint
def mintflagtoken(ctx, _contract, _to_address, _amount, _from, _acc_nonce):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['flagtoken']['abi'])
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
	if 'mintflagtoken' not in ctx['deployedcontracts'][_acct.address].keys():
		p.ppln("[-] try to mintflagtoken to deployer...")
		err, txhash = mintflagtoken(ctx, _contract, _to_address, _amount, _acct, _acc_nonce)
		if err:
			p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
			exit(0)
		else:
			update_user_deploy_contracts(ctx, _acct.address, 'mintflagtoken', txhash.hex())
			return None, txhash.hex()
	else:
		txhash = ctx['deployedcontracts'][_acct.address]['mintflagtoken']
		return None, txhash


def mint_review(ctx, _acct, _txhash):
	w3 = ctx['web3instance']
	p.ppln("[-] Check for mintflagtoken successful... ")
	try:
		tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
	except Exception as err:
		p.ppln(str(err))
		exit(0)
	addr = tx_receipt['transactionHash'].hex()

	if not addr:
		p.pln(p.in_fg_color("[!] mintflagtoken Broken down", r.red5))
	else:
		p.ppln("[+] mintflagtoken " + p.in_fg_color("success", r.green1))
		p.ppln("[!] mintflagtoken transaction hash is " + p.in_fg_color(addr, r.blue1))


# approve
def approveflagtoken(ctx, _contract, _to, _amount, _from, _acc_nonce):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['flagtoken']['abi'])
	p.ppln(" approve transaction init success")
	construct_tx = store_var_contract.functions.approve(_to, _amount).buildTransaction(
		{'chainId': 3,
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
	if 'approveflagtoken' not in ctx['deployedcontracts'][_acct.address].keys():
		p.ppln("[-] try to approveflagtoken to deployer...")

		err, txhash = approveflagtoken(ctx, _contract, _to, _amount, _acct, _acc_nonce)
		if err:
			p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
			exit(0)
		else:
			update_user_deploy_contracts(ctx, _acct.address, 'approveflagtoken', txhash.hex())
			return None, txhash.hex()
	else:
		txhash = ctx['deployedcontracts'][_acct.address]['approveflagtoken']
		return None, txhash


def approve_review(ctx, _acct, _txhash):
	w3 = ctx['web3instance']
	p.ppln("[-] Check for approveflagtoken successful... ")
	try:
		tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
	except Exception as err:
		p.ppln(str(err))
		exit(0)
	addr = tx_receipt['transactionHash'].hex()

	if not addr:
		p.pln(p.in_fg_color("[!] approveflagtoken Broken down", r.red5))
	else:
		p.ppln("[+] approveflagtoken " + p.in_fg_color("success", r.green1))
		p.ppln("[!] approveflagtoken transaction hash is " + p.in_fg_color(addr, r.blue1))
