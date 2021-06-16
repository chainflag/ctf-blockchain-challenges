from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r
from src.utils.utils import update_user_deploy_contracts

# mint
def allpairschaitinfactory(ctx, _contract, _from):
	w3 = ctx['web3instance']
	store_var_contract = w3.eth.contract(address=_contract, abi=ctx['compiledcontracts']['chaitinfactory']['abi'])
	try:
		pair_addr = store_var_contract.functions.allPairs(0).call()
	except Exception as err:
		return err, None
	return None, pair_addr


def allpairs(ctx, _contract, _acct):
	if 'allpairschaitinfactory' not in ctx['deployedcontracts'][_acct.address].keys():
		p.ppln("[-] try to allpairschaitinfactory...")
		err, pair_addr = allpairschaitinfactory(ctx, _contract, _acct)
		if err:
			p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
			exit(0)
		else:
			update_user_deploy_contracts(ctx, _acct.address, 'allpairschaitinfactory', pair_addr)
			p.ppln("[+] allpairschaitinfactory " + p.in_fg_color("success", r.green1))
			p.ppln("[!] chaitinToken-feiToken pair address is: " + p.in_fg_color(pair_addr, r.blue1))
			return None, pair_addr
	else:
		pair_addr = ctx['deployedcontracts'][_acct.address]['allpairschaitinfactory']
		p.ppln("[!] chaitinToken-feiToken pair address is: " + p.in_fg_color(pair_addr, r.blue1))
		return None, pair_addr


