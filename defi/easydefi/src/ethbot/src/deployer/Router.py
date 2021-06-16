
import conf.base as conf
from src.utils.prettyprint.Red import Printer as p
import src.utils.prettyprint.Red as r
from src.utils.utils import update_user_deploy_contracts


def chaitinrouter(w3, _abi, _bin, _acct, _acc_nonce, _factoryaddr, _weth_addr, _chaitin_token_addr):
    instance = w3.eth.contract(
        abi=_abi,
        bytecode=_bin
    )
    construct_tx = instance.constructor(_factoryaddr, _weth_addr, _chaitin_token_addr).buildTransaction(
        {'chainId': conf.chainId,
         'from': _acct.address,
         'nonce': _acc_nonce[0],  # TODO: nonce 需要全局增加
         'gasPrice': conf.gasPriceOfRouterDeploy,
         'gas': conf.gasLimitOfRouterDeploy
         # 'value': w3.toWei(value, 'ether'),
         })
    try:
        signed_tx = _acct.signTransaction(construct_tx)
        tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
        _acc_nonce[0] += 1
    except Exception as err:
        return err, None
    return None, tx_hash.hex()


def deploy(ctx, _acct, _acc_nonce, _factoryaddr, _weth_addr, _chaitin_token_addr):
    if 'chaitinrouter' not in ctx['deployedcontracts'][_acct.address].keys():
        p.ppln("[-] try to deploy chaitinrouter contracts...")
        abi = ctx['compiledcontracts']['chaitinrouter']['abi']
        bin = ctx['compiledcontracts']['chaitinrouter']['bin']
        w3 = ctx['web3instance']
        err, txhash = chaitinrouter(w3, abi, bin, _acct, _acc_nonce, _factoryaddr, _weth_addr, _chaitin_token_addr)
        if err:
            p.ppln(p.in_fg_color(("[!] " + str(err)), r.red5))
            exit(0)
        else:
            return None, txhash
    else:
        txhash = ctx['deployedcontracts'][_acct.address]['chaitinrouter']
        return None, txhash


def review(ctx, _acct, _txhash):
    w3 = ctx['web3instance']
    p.ppln("[-] Check for chaitinrouter contract successful deployment... ")
    if 'chaitinrouter' not in ctx['deployedcontracts'][_acct.address].keys():
        try:
            tx_receipt = w3.eth.waitForTransactionReceipt(_txhash, timeout=720)
        except Exception as err:
            p.p(str(err))
            exit(0)
        addr = tx_receipt['contractAddress']
        update_user_deploy_contracts(ctx, _acct.address, 'chaitinrouter', addr)
    else:
        addr = ctx['deployedcontracts'][_acct.address]['chaitinrouter']

    if not addr:
        p.pln(p.in_fg_color("[!] contract chaitinrouter deploy Broken down", r.red5))
    else:
        p.ppln("[+] contract chaitinrouter deploy " + p.in_fg_color("success", r.green1))
        p.ppln("[!] chaitinrouter contract address is " + p.in_fg_color(addr, r.blue1))

