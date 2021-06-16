import json
from solcx import compile_source
from src.utils.utils import dumps_env


# solc
def compile_from_src(source):
	compiled_sol = compile_source(source, output_values=["abi", "bin"], solc_version="0.6.6", optimize=True)
	return compiled_sol


# solc
def compile_from_src_op(source):
	compiled_sol = compile_source(source, output_values=["abi", "bin"], solc_version="0.6.6", optimize=True)
	return compiled_sol


# solc
def compile_from_src_v5(source):
	compiled_sol = compile_source(source, output_values=["abi", "bin"], solc_version="0.5.16")
	return compiled_sol


# web3
def get_deploy_est_gas(ctx, cont_if):
	w3 = ctx['web3instance']
	instance = w3.eth.contract(
		abi=cont_if['abi'],
		bytecode=cont_if['bin']
	)
	return instance.constructor().estimateGas()


def prepare_contract_source_without_cache():
	confs = {}

	with open("contracts/ERC20.sol", 'r+') as fi:
		source1 = fi.read()
		conf_all = compile_from_src(source1)
		confs['chaitintoken'] = conf_all['<stdin>:ChaitinToken']
		confs['feitoken'] = conf_all['<stdin>:FeiToken']
		confs['flagtoken'] = conf_all['<stdin>:FlagToken']

	with open("contracts/WETH9.sol", 'r+') as fi:
		source1 = fi.read()
		conf_all = compile_from_src(source1)
		confs['weth9'] = conf_all['<stdin>:WETH9']

	with open("contracts/ChaitinFactory.json",
			  'r') as f:  # TODO:// update ChaitinFactory into a primary params Precious
		js = json.loads(f.read())
		confs['chaitinfactory'] = {}
		confs['chaitinfactory']['abi'] = js['abi']
		confs['chaitinfactory']['bin'] = js['bytecode']


	with open("contracts/ChaitinRouter.sol", 'r+') as fi:
		source1 = fi.read()
		conf_all = compile_from_src_op(source1)
		confs['chaitinrouter'] = conf_all['<stdin>:ChaitinRouter']

	with open("contracts/ChaitinBank.sol", 'r+') as fi:
		source1 = fi.read()
		conf_all = compile_from_src(source1)
		confs['chaitinbank'] = conf_all['<stdin>:ChaitinBank']
	return confs


def comp(ctx):
	if not ctx['compiledcontracts']:
		compiler_result = prepare_contract_source_without_cache()
		ctx['compiledcontracts'] = compiler_result
		dumps_env(ctx)
		return ctx
	else:
		return ctx
