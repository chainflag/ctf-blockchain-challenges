from conf.base import flag, TOPIC, ONEHUNDRED
from src.utils.auth import get_acc_nonce
from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r

def getflag():
	return flag


def balanceofflagtoken(ctx, _contract, _to_address, _from, _acc_nonce):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['chaitintoken']['abi'])

	try:
		balance = store_var_contract.functions.balanceOf(_to_address).call()
	except Exception as err:
		return err, None
	return None, balance


def check_if_has_topic(ctx, _acct):
	acc_nonce = get_acc_nonce(ctx, _acct)
	flagtoken_addr = ctx['deployedcontracts'][_acct.address]['flagtoken']
	gamer_account = ctx['deployedcontracts'][_acct.address]['transfercheck']
	err, balance = balanceofflagtoken(ctx, flagtoken_addr, gamer_account, _acct, acc_nonce)

	if err:
		p.pln(p.in_fg_color(str(err), r.red4))

	if ( TOPIC < balance or TOPIC == balance ) and balance < ONEHUNDRED:
		return True
	else:
		return False
