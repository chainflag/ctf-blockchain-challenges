from src.utils.prettyprint.Red import Printer, Formator
_p = Printer()
_f = Formator()
deploy_panic_imp_info = "人们不能预见、不可避免、不能克服的自然、社会现象客观情况。社会及自然现象包括但不限于天灾人祸如地震、战争、市政工程建设、其它政府政策或矿工不给你打包交易"

MENU = '''
We design a pretty easy contract game. Enjoy it!
1. Create a game account
2. Deploy a game contract
3. Request for flag
Game environment: ropsten testnet
Option 1, get an account which will be used to deploy the contract;
Before option 2, please transfer some eth to this account (for gas);
Option 2, the robot will use the account to deploy the contract for the problem;
Option 3, use this option to obtain the flag after the event is triggered.
You can finish this challenge in a lot of connections.
'''


WELCOME = _f.in_column_center(_p.in_fg_color('.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.\r', 40))+\
_f.in_column_center(_p.in_fg_color('.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.\n', 40))+\
_f.in_column_center(_p.in_fg_color('( Welcome to EasyDefi!                          )\n', 41))+\
_f.in_column_center(_p.in_fg_color(' )we will give you 1 wei Chaitin token,         (\n', 42))+\
_f.in_column_center(_p.in_fg_color('( And you need to exchange it for 80 FlagTokens )\n', 43))+\
_f.in_column_center(_p.in_fg_color('"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"\n', 44))


SRC_TEXT = '''
https://github.com/PandaTea/NightCity-backup
'''

DEPLOY_SUCCESS_CELEBRATION = "\n\n\n\n\n\n\n\n" + _f.in_column_center(_p.in_fg_color('.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.\r', 40))+\
                             _f.in_column_center(_p.in_fg_color(' .+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.\n', 39))+\
_f.in_column_center(_p.in_fg_color('( ALL CONTRACTS Deployed SUCCESSFUL           )\n',75))+\
_f.in_column_center(_p.in_fg_color(' )Congratulations!!!, You are so lucky!      (\n',111))+\
_f.in_column_center(_p.in_fg_color('( The blessings of the miners are with you!!! )\n',147))+\
_f.in_column_center(_p.in_fg_color(' "+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"+.+"\n',183)) + "\n\n\n\n"

PANIC_INFO = '''
Uploading distributions to https://upload.pypi.org/legacy/
Enter your username: ^CTraceback (most recent call last):
  File "/usr/local/bin/绝密-夜之城地下金融交易网络内幕", line 8, in <module>
    sys.exit(main())
  File "/usr/local/lib/python3.8/site-packages/绝密-夜之城地下金融交易网络内幕/__main__.py", line 28, in main
    result = cli.dispatch(sys.argv[1:])
  File "/usr/local/lib/python3.8/site-packages/绝密-夜之城地下金融交易网络内幕/cli.py", line 82, in dispatch
    return main(args.args)
  File "/usr/local/lib/python3.8/site-packages/绝密-夜之城地下金融交易网络内幕/commands/upload.py", line 151, in main
    return upload(upload_settings, parsed_args.dists)
  File "/usr/local/lib/python3.8/site-packages/绝密-夜之城地下金融交易网络内幕/commands/upload.py", line 89, in upload
    repository = upload_settings.create_repository()
  File "/usr/local/lib/python3.8/site-packages/绝密-夜之城地下金融交易网络内幕/settings.py", line 321, in create_repository
    self.username,
  File "/usr/local/lib/python3.8/site-packages/绝密-夜之城地下金融交易网络内幕/settings.py", line 141, in username
    return cast(Optional[str], self.auth.username)
  File "/usr/local/lib/python3.8/site-packages/绝密-夜之城地下金融交易网络内幕/auth.py", line 35, in username
    return utils.get_userpass_value(
  File "/usr/local/lib/python3.8/site-packages/绝密-夜之城地下金融交易网络内幕/utils.py", line 241, in get_userpass_value
    return prompt_strategy()
  File "/usr/local/lib/python3.8/site-packages/绝密-夜之城地下金融交易网络内幕/auth.py", line 76, in username_from_keyring_or_prompt
    return self.get_username_from_keyring() or self.prompt("username", input)
  File "/usr/local/lib/python3.8/site-packages/绝密-夜之城地下金融交易网络内幕/auth.py", line 84, in prompt
    return how(f"Enter your {what}: ")
'''

SORRY_INFO = '''
Sorry, you do not have access to this confidential content
对不起，你无权访问此机密内容
'''