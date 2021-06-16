from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r
from src.utils.utils import update_user_deploy_contracts
from conf.base import gasLimitOfAddLiquidity, gasPriceOfAddLiquidity, ONEDAY
import time

# mint
def addliquiditychaitinrouter(ctx, _contract, _to_address, _tokenA, _tokenB, _amountA, _amountB, _from, _acc_nonce):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['chaitinrouter']['abi'])
	construct_tx = store_var_contract.functions.addLiquidity(_tokenA,
	                                                         _tokenB,
	                                                         _amountA,
	                                                         _amountB,
	                                                         1,
	                                                         1,
	                                                         _to_address,
	                                                         int(time.time() + ONEDAY)).buildTransaction(
		{'chainId': 3,
		'from': _from.address,
		'nonce': _acc_nonce[0],
		'gasPrice': gasPriceOfAddLiquidity,
		'gas': gasLimitOfAddLiquidity
		})
	try:
		signed_tx = _from.signTransaction(construct_tx)
		tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
		_acc_nonce[0] += 1
	except Exception as err:
		return err, None
	return None, tx_hash


def addliquidity(ctx, _contract, _tokenA, _tokenB, _amountA, _amountB, _to_address, _acct, _acc_nonce):
	if 'addliquiditychaitinrouter' not in ctx['deployedcontracts'][_acct.address].keys():
		p.ppln("[-] try to addliquiditychaitinrouter to deployer...")
		err, txhash = addliquiditychaitinrouter(ctx,
		                                        _contract,
		                                        _to_address,
		                                        _tokenA,
		                                        _tokenB,
		                                        _amountA,
		                                        _amountB,
		                                        _acct,
		                                        _acc_nonce)
		if err:
			p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
			exit(0)
		else:
			update_user_deploy_contracts(ctx, _acct.address, 'addliquiditychaitinrouter', txhash.hex())
			return None, txhash.hex()
	else:
		txhash = ctx['deployedcontracts'][_acct.address]['addliquiditychaitinrouter']
		return None, txhash


def addliquidity_review(ctx, _acct, _txhash):
	w3 = ctx['web3instance']
	p.ppln("[-] Check for addliquiditychaitinrouter successful... ")
	try:
		tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
	except Exception as err:
		p.ppln(str(err))
		exit(0)
	addr = tx_receipt['transactionHash'].hex()

	if not addr:
		p.pln(p.in_fg_color("[!] addliquiditychaitinrouter Broken down", r.red5))
	else:
		p.ppln("[+] addliquiditychaitinrouter " + p.in_fg_color("success", r.green1))
		p.ppln("[!] addliquiditychaitinrouter transaction hash is " + p.in_fg_color(addr, r.blue1))

