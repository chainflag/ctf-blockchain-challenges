from src.utils.auth import encrypt_then_mac, create_game_account
from conf.base import AES_KEY, HMAC_KEY, est_gas

def run(ctx):
	# create game account
	acct = create_game_account(ctx)
	print("[+]Your game account:{}".format(acct.address))

	# save account
	with open('db/account.txt', 'a') as f:
		f.write(acct.address)
		f.write('\n')
		f.write(''.join(['%02X' % x for x in acct.key]))
		f.write('\n\n')

	# generate token
	data = acct.address.encode() + acct.key
	token = encrypt_then_mac(data, AES_KEY, HMAC_KEY)
	print("[+]token: {}".format(token))

	print("[+]Deploy will cost {} gas".format(est_gas))
	print("[+]Make sure that you have enough ether to deploy!!!!!!")