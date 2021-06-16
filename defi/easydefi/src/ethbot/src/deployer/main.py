from src.utils.auth import get_acc_nonce
from src.utils.prettyprint.Red import Printer, Processor, Formator
from src.utils.compiler import comp
from conf.base import ONEHUNDRED
from src.banner.text.corpus import DEPLOY_SUCCESS_CELEBRATION
import src.utils.prettyprint.Red as r

from src.deployer import ChaitinToken, FeiToken, FlagToken, WETH9, Factory, Router, ChaitinBank
from src.interface import IChaitinToken, IChaitinRouter, IChaitinFactory, IFeiToken, IFlagToken


def finish_deploy(ctx, _acct):
	if 'mintforuser' in ctx['deployedcontracts'][_acct.address].keys():
		mintforuser_txhash = ctx['deployedcontracts'][_acct.address]['mintforuser']
		Printer.ppln(DEPLOY_SUCCESS_CELEBRATION)
		return bytes.fromhex(mintforuser_txhash.split("0x")[1])
	else:
		exit(0)


def run(ctx, _acct):
	p = Printer()
	processor = Processor(150)
	formator = Formator()

	p.ppln(formator.in_all_left("[-] loading deploy cache..."))

	ctx = comp(ctx)
	processor.update(3)

	acc_nonce = get_acc_nonce(ctx, _acct)
	processor.update(2)


	# 1 stage contracts deploy
	err, chaitintoken_deploy_txhash = ChaitinToken.deploy(ctx, _acct, acc_nonce)
	processor.update(5)

	err, feitoken_deploy_txhash = FeiToken.deploy(ctx, _acct, acc_nonce)
	processor.update(5)

	err, flagtoken_deploy_txhash = FlagToken.deploy(ctx, _acct, acc_nonce)
	processor.update(5)

	err, weth9_deploy_txhash = WETH9.deploy(ctx, _acct, acc_nonce)
	processor.update(5)

	err, factory_deploy_txhash = Factory.deploy(ctx, _acct, acc_nonce)
	processor.update(5)


	ChaitinToken.review(ctx, _acct, chaitintoken_deploy_txhash)
	processor.update(5)

	FeiToken.review(ctx, _acct, feitoken_deploy_txhash)
	processor.update(5)

	FlagToken.review(ctx, _acct, flagtoken_deploy_txhash)
	processor.update(5)

	WETH9.review(ctx, _acct, weth9_deploy_txhash)
	processor.update(5)

	Factory.review(ctx, _acct, factory_deploy_txhash)
	processor.update(5)

	# 2 stage contracts deploy
	factory_addr = ctx['deployedcontracts'][_acct.address]['chaitinfactory']
	weth9_addr = ctx['deployedcontracts'][_acct.address]['weth9']
	chaitintoken_addr = ctx['deployedcontracts'][_acct.address]['chaitintoken']

	err, router_deploy_txhash = Router.deploy(ctx, _acct, acc_nonce, factory_addr, weth9_addr, chaitintoken_addr)
	processor.update(5)

	Router.review(ctx, _acct, router_deploy_txhash)
	processor.update(5)


	# 3 stage mint approve and add liquidity
	chaitinrouter_addr = ctx['deployedcontracts'][_acct.address]['chaitinrouter']

	err, chaitintoken_mint_txhash = IChaitinToken.mint(ctx, chaitintoken_addr, _acct.address, ONEHUNDRED, _acct, acc_nonce)
	processor.update(5)

	err, chaitintoken_approve_txhash = IChaitinToken.approve(ctx, chaitintoken_addr, chaitinrouter_addr, ONEHUNDRED, _acct, acc_nonce)
	processor.update(5)

	IChaitinToken.mint_review(ctx, _acct, chaitintoken_mint_txhash)
	processor.update(5)

	IChaitinToken.approve_review(ctx, _acct, chaitintoken_approve_txhash)
	processor.update(5)

	feitoken_addr = ctx['deployedcontracts'][_acct.address]['feitoken']
	err, feitoken_mint_txhash = IFeiToken.mint(ctx, feitoken_addr, _acct.address, ONEHUNDRED, _acct,
	                                                   acc_nonce)
	processor.update(5)

	err, feitoken_approve_txhash = IFeiToken.approve(ctx, feitoken_addr, chaitinrouter_addr, ONEHUNDRED, _acct,
	                                                         acc_nonce)
	processor.update(5)

	IFeiToken.mint_review(ctx, _acct, feitoken_mint_txhash)
	processor.update(5)

	IFeiToken.approve_review(ctx, _acct, feitoken_approve_txhash)
	processor.update(5)


	err, chaitinrouter_addliquidity_txhash = IChaitinRouter.addliquidity(ctx,
	                                                                     chaitinrouter_addr,
	                                                                     chaitintoken_addr,
	                                                                     feitoken_addr,
	                                                                     ONEHUNDRED,
	                                                                     ONEHUNDRED,
	                                                                     _acct.address,
	                                                                     _acct,
	                                                                     acc_nonce)
	processor.update(5)

	IChaitinRouter.addliquidity_review(ctx, _acct, chaitinrouter_addliquidity_txhash)
	processor.update(5)

	# 4 stage get pair and deploy bank
	flagtoken_addr = ctx['deployedcontracts'][_acct.address]['flagtoken']

	err, pair_addr = IChaitinFactory.allpairs(ctx, factory_addr, _acct)
	processor.update(5)

	err, bank_deploy_txhash = ChaitinBank.deploy(ctx,
	                                      feitoken_addr,
	                                      _acct.address,
	                                      flagtoken_addr,
	                                      pair_addr,
	                                      chaitinrouter_addr,
	                                      _acct,
	                                      acc_nonce)
	processor.update(5)

	ChaitinBank.review(ctx, _acct, bank_deploy_txhash)
	processor.update(5)

	# 5 stage Mint Flag to ChaitinBank
	chaitinbank_addr = ctx['deployedcontracts'][_acct.address]['chaitinbank']

	err, flagtoken_mint_txhash = IFlagToken.mint(ctx, flagtoken_addr, chaitinbank_addr, ONEHUNDRED, _acct, acc_nonce)
	processor.update(5)

	IFlagToken.mint_review(ctx, _acct, flagtoken_mint_txhash)
	processor.update(5)

	# 6 stage get Gamer address and Mint ChaitinToken to him
	gamer_address = ctx['deployedcontracts'][_acct.address]['transfercheck']
	err, gamer_mint_txhash = IChaitinToken.mintforuser(ctx, chaitintoken_addr, gamer_address, 1, _acct,
	                                                   acc_nonce)
	processor.update(5)

	IChaitinToken.mintforuser_review(ctx, _acct, gamer_mint_txhash)
	processor.update(5)








	# finish deployer
	return finish_deploy(ctx, _acct)



