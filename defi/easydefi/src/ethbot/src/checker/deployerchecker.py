
from conf.base import MINSTARTBALANCE
from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r
from src.utils.utils import update_user_deploy_contracts


def transfercheck(ctx, _acct, _txhash):
    w3 = ctx['web3instance']
    if 'transfercheck' not in ctx['deployedcontracts'][_acct.address].keys():
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=120)
        except:
            return False
        _from = tx_receipt['from']
        _to = tx_receipt['to']

        if _to != _acct.address:
            return False

        try:
            balance = w3.eth.getBalance(_acct.address)
        except:
            return False

        if balance < MINSTARTBALANCE:
            p.pln(p.in_fg_color("contructor Balance Not Enough, Please Send More ETH...", r.red4))

        update_user_deploy_contracts(ctx, _acct.address, 'transfercheck', _from)
        return True
    else:
        return True
