

from conf.base import AES_KEY, HMAC_KEY
from src.utils.auth import validate_then_decrypt, validate_game_account, encrypt_then_mac, is_account_exist
import src.deployer.main as deployer
import sys
from src.utils.prettyprint.Red import Printer
import src.utils.prettyprint.Red as r
from src.checker.deployerchecker import transfercheck



def run(ctx):
	token = input("[-]input your token: ")
	token = token.strip()
	data = validate_then_decrypt(token, AES_KEY, HMAC_KEY)
	if len(data) != 74:
		print(Printer.in_fg_color("[+]wrong token", r.red4))
		sys.exit(0)
	acct = validate_game_account(ctx, data)

	if not is_account_exist(ctx, acct.address):
		print(Printer.in_fg_color("[+]wrong token", r.red4))
		sys.exit(0)

	transfer_txhash = input("[-]input your transaction hash of transfer enough ETH to deployer: ")
	if not transfercheck(ctx, acct, transfer_txhash):
		print(Printer.in_fg_color("[+]wrong transaction hash", r.red4))
		sys.exit(0)

	tx_hash = deployer.run(ctx, acct)

	# generate new token
	data = acct.address.encode() + acct.key + tx_hash
	new_token = encrypt_then_mac(data, AES_KEY, HMAC_KEY)
	Printer.ppln(Printer.in_fg_color("[+]new token: {}".format(new_token), r.white1))
	Printer.ppln("[+]Your goal is to convert 1wei Chaitin into 80 Flag")