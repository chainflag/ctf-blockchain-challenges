
import conf.base as conf
from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r
from src.utils.utils import update_user_deploy_contracts


def flagtoken(w3, _abi, _bin, _acct, _acc_nonce):
    instance = w3.eth.contract(
        abi=_abi,
        bytecode=_bin
    )
    construct_tx = instance.constructor().buildTransaction(
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


def deploy(ctx, _acct, _acc_nonce):
    if 'flagtoken' not in ctx['deployedcontracts'][_acct.address].keys():
        p.ppln("[-] try to deploy flagtoken contracts...")
        abi = ctx['compiledcontracts']['flagtoken']['abi']
        bin = ctx['compiledcontracts']['flagtoken']['bin']
        w3 = ctx['web3instance']
        err, txhash = flagtoken(w3, abi, bin, _acct, _acc_nonce)
        if err:
            p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
            exit(0)
        else:
            return None, txhash
    else:
        txhash = ctx['deployedcontracts'][_acct.address]['flagtoken']
        return None, txhash


def review(ctx, _acct, _txhash):
    w3 = ctx['web3instance']
    p.ppln("[-] Check for flagtoken contract successful deployment... ")
    if 'flagtoken' not in ctx['deployedcontracts'][_acct.address].keys():
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
        except Exception as err:
            p.p(str(err))
            exit(0)
        addr = tx_receipt['contractAddress']
        update_user_deploy_contracts(ctx, _acct.address, 'flagtoken', addr)
    else:
        addr = ctx['deployedcontracts'][_acct.address]['flagtoken']

    if not addr:
        p.pln(p.in_fg_color("[!] contract flagtoken deploy Broken down", r.red5))
    else:
        p.ppln("[+] contract flagtoken deploy " + p.in_fg_color("success", r.green1))
        p.ppln("[!] flagtoken contract address is " + p.in_fg_color(addr, r.blue1))

