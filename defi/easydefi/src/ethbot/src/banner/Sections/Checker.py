
from conf.base import AES_KEY, HMAC_KEY, sz_col, sz_row
from src.utils.auth import validate_then_decrypt, validate_game_account
from src.checker.flagchecker import check_if_has_topic, getflag
from colorfulpanda.mov.BlinkBlock import main as mov
from colorfulpanda.mov.PanicWhiteRed import main as mov2
from src.banner.text.corpus import PANIC_INFO, SORRY_INFO
import sys


def run(ctx):
	new_token = input("[-]input your new token: ")
	new_token = new_token.strip()
	data = validate_then_decrypt(new_token, AES_KEY, HMAC_KEY)

	if len(data) != 106:
		print("[+]wrong token")
		sys.exit(0)

	data, tx_hash = data[:-32], data[-32:]
	acct = validate_game_account(ctx, data)
	res = check_if_has_topic(ctx, acct) #TODO: checker 具体咋Che还没定
	if res:
		flag = getflag()
		mov(flag, sz_col, sz_row)
	else:
		mov2(PANIC_INFO, SORRY_INFO, sz_col, sz_row)