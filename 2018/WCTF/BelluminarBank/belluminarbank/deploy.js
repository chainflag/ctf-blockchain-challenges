var Web3 = require('web3');
port = 8000 + parseInt(process.argv[2]);
web3 = new Web3(new Web3.providers.HttpProvider('http://127.0.0.1:' + port.toString() + '/'));

console.log('Starting deploy');

step1();

function step1() {
  // this is participant's account
  web3.personal.importRawKey('b85de9d87f5851a09994ec40438e5e4396b1f36266f4f3566b421aec391a69df', '123qwe', function(e,v){console.log(e, v); step2()});
}

function step2() {
  // this is bank owner's account
  web3.personal.importRawKey('3a2bc75a07948d11105d11a14b030bec316407193391d6274caf29ccc9ebfa71', 'ksdi2h3498uoidsjo2834098u', function(e,v){console.log(e, v); step3()});
}

function step3() {
  web3.personal.unlockAccount('0x571dc32a4A4DA1FD6fF02642537D85Be8984dCB2', 'ksdi2h3498uoidsjo2834098u', 1500, function(e,v){console.log(e, v); step4()});
}

function step4() {
  var _secret = '0x00313373133731337313373133731337';
  var deposit_term = 1622586278;
  var belluminarbankContract = web3.eth.contract([{"constant":true,"inputs":[],"name":"bankBalance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"account","type":"uint256"}],"name":"withdraw","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"account","type":"uint256"},{"name":"_secret","type":"bytes16"}],"name":"confiscate","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"account","type":"uint256"},{"name":"deposit_term","type":"uint256"}],"name":"invest","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"inputs":[{"name":"_secret","type":"bytes16"},{"name":"deposit_term","type":"uint256"}],"payable":true,"stateMutability":"payable","type":"constructor"}]);
  var belluminarbank = belluminarbankContract.new(
     _secret,
     deposit_term,
     {
       from: '0x571dc32a4A4DA1FD6fF02642537D85Be8984dCB2',//web3.eth.accounts[0], 
       data: '0x6080604052604051604080610794833981018060405281019080805190602001909291908051906020019092919050505081600360006101000a8154816fffffffffffffffffffffffffffffffff02191690837001000000000000000000000000000000009004021790555033600260006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555060003411156101735760006060604051908101604052803481526020018381526020013373ffffffffffffffffffffffffffffffffffffffff1681525090806001815401808255809150509060018203906000526020600020906003020160009091929091909150600082015181600001556020820151816001015560408201518160020160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505050505b5050610610806101846000396000f300608060405260043610610062576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff16806328657aa5146100675780632e1a7d4d14610092578063a5c12f79146100bf578063d87aa64314610109575b600080fd5b34801561007357600080fd5b5061007c610133565b6040518082815260200191505060405180910390f35b34801561009e57600080fd5b506100bd60048036038101908080359060200190929190505050610152565b005b3480156100cb57600080fd5b506101076004803603810190808035906020019092919080356fffffffffffffffffffffffffffffffff19169060200190929190505050610265565b005b610131600480360381019080803590602001909291908035906020019092919050505061043f565b005b60003073ffffffffffffffffffffffffffffffffffffffff1631905090565b60008181548110151561016157fe5b906000526020600020906003020160010154421015151561018157600080fd5b60008181548110151561019057fe5b906000526020600020906003020160020160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156101fb57600080fd5b3373ffffffffffffffffffffffffffffffffffffffff166108fc60008381548110151561022457fe5b9060005260206000209060030201600001549081150290604051600060405180830381858888f19350505050158015610261573d6000803e3d6000fd5b5050565b600080600260009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff161415156102c457600080fd5b826fffffffffffffffffffffffffffffffff1916600360009054906101000a9004700100000000000000000000000000000000026fffffffffffffffffffffffffffffffff191614151561031757600080fd5b6301e1338060008581548110151561032b57fe5b90600052602060002090600302016001015401421015151561034c57600080fd5b6000915060015490505b83811115156103e85760008181548110151561036e57fe5b9060005260206000209060030201600001548201915060008181548110151561039357fe5b906000526020600020906003020160008082016000905560018201600090556002820160006101000a81549073ffffffffffffffffffffffffffffffffffffffff021916905550508080600101915050610356565b600184016001819055503373ffffffffffffffffffffffffffffffffffffffff166108fc839081150290604051600060405180830381858888f19350505050158015610438573d6000803e3d6000fd5b5050505050565b60006001548310158015610457575060008054905083105b156104925760008381548110151561046b57fe5b906000526020600020906003020190503481600001600082825401925050819055506105df565b6000808054905011156104dd576301e1338060006001600080549050038154811015156104bb57fe5b9060005260206000209060030201600101540182101515156104dc57600080fd5b5b348160000181905550818160010181905550338160020160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506000819080600181540180825580915050906001820390600052602060002090600302016000909192909190915060008201548160000155600182015481600101556002820160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff168160020160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055505050505b5050505600a165627a7a72305820f5b959ebff97eb743106c14ad377f2c0c24ca39ad65bc3595f91bb661dca2b1f0029', 
       gas: '4700000',
       value: 31337
     }, function (e, contract){
      console.log(e, contract);
      if(typeof contract.address != 'undefined') {
      	console.log('Contract mined! address: ' + contract.address + ' transactionHash: ' + contract.transactionHash);
        web3.personal.lockAccount('0x571dc32a4A4DA1FD6fF02642537D85Be8984dCB2');
        setInterval(function() {
          if(web3.eth.getBalance(contract.address) == 0) {
            console.log('Task solved!!');
            web3.personal.unlockAccount('0x571dc32a4A4DA1FD6fF02642537D85Be8984dCB2', 'ksdi2h3498uoidsjo2834098u', 1500);
            web3.eth.sendTransaction({
              from: '0x571dc32a4A4DA1FD6fF02642537D85Be8984dCB2',
              to: '0x72d45c0dc7EfdAfd00467086B65B2fe078788c44',
              value: 1,
              data: web3.toHex('flag{this is flag}')
            });
            web3.personal.lockAccount('0x571dc32a4A4DA1FD6fF02642537D85Be8984dCB2')
          }
        }, 10000);
      }
   })
}