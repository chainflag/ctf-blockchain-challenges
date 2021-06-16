
import conf.base as conf
from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r
from src.utils.utils import update_user_deploy_contracts


def chaitinbank(w3, _abi, _bin, _feicoin, _owner, _flagtokenaddr, _pairaddr, _routeraddr, _acct, _acc_nonce):
    instance = w3.eth.contract(
        abi=_abi,
        bytecode=_bin
    )
    construct_tx = instance.constructor(_feicoin,
                                        _owner,
                                        _flagtokenaddr,
                                        _pairaddr,
                                        _routeraddr,
                                        90).buildTransaction(
        {'chainId': conf.chainId,
         'from': _acct.address,
         'nonce': _acc_nonce[0],  # TODO: nonce 需要全局增加
         'gasPrice': conf.gasPriceOfTokenDeploy,
         'gas': conf.gasLimitOfTokenDeploy
         # 'value': w3.toWei(value, 'ether'),
         })
    try:
        signed_tx = _acct.signTransaction(construct_tx)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        _acc_nonce[0] += 1
    except Exception as err:
        return err, None
    return None, tx_hash.hex()


def deploy(ctx, _feicoin, _owner, _flagtokenaddr, _pairaddr, _routeraddr, _acct, _acc_nonce):
    if 'chaitinbank' not in ctx['deployedcontracts'][_acct.address].keys():
        p.ppln("[-] try to deploy chaitinbank contracts...")
        abi = ctx['compiledcontracts']['chaitinbank']['abi']
        bin = ctx['compiledcontracts']['chaitinbank']['bin']
        w3 = ctx['web3instance']
        err, txhash = chaitinbank(w3, abi, bin, _feicoin, _owner, _flagtokenaddr, _pairaddr, _routeraddr, _acct, _acc_nonce)
        if err:
            p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
            exit(0)
        else:
            return None, txhash
    else:
        txhash = ctx['deployedcontracts'][_acct.address]['chaitinbank']
        return None, txhash


def review(ctx, _acct, _txhash):
    w3 = ctx['web3instance']
    p.ppln("[-] Check for chaitinbank contract successful deployment... ")
    if 'chaitinbank' not in ctx['deployedcontracts'][_acct.address].keys():
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
        except Exception as err:
            p.p(str(err))
            exit(0)
        addr = tx_receipt['contractAddress']
        update_user_deploy_contracts(ctx, _acct.address, 'chaitinbank', addr)
    else:
        addr = ctx['deployedcontracts'][_acct.address]['chaitinbank']

    if not addr:
        p.pln(p.in_fg_color("[!] contract chaitinbank deploy Broken down", r.red5))
    else:
        p.ppln("[+] contract chaitinbank deploy " + p.in_fg_color("success", r.green1))
        p.ppln("[!] chaitinbank contract address is " + p.in_fg_color(addr, r.blue1))

