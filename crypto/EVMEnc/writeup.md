# EVMcrypto

## 源码

```
pragma solidity ^0.5.10;

contract EVMEnc {
    
    uint public result;
    string public key;
    
    uint private delta;
    uint public output;
    
    uint32 public sum;
    uint224 private tmp_sum=0;
    
    uint32 private key0;
    uint224 private t0=0;
    uint32 private key1;
    uint224  private t1=0;
    uint32 private key2;
    uint224 private  t2=0;
    uint32  private key3;
    uint224 private  t3=0;
    
    constructor() public {
        delta = 0xb3c6ef3720;
    }
    
    function Convert(string memory source) public pure returns (uint result) {
        bytes32 tmp;
        assembly {
            tmp := mload(add(source, 32))
        }
        result = uint(tmp) / 0x10000000000000000;
    }
    
    function set_key(string memory tmp) public {
        key = tmp;
    }

    function cal_(uint x) public {
        uint tmp = Convert(key) / 0x10000000000000000;
        result = tmp % x;
    }

    function Encrypt(string memory flag) public {
        uint tmp = Convert(flag);
        uint key_tmp = Convert(key) / 0x10000000000000000;
        assembly {
            let first,second
            sstore(5, and(shr(96, key_tmp), 0xffffffff))
            sstore(6, and(shr(64, key_tmp), 0xffffffff))
            sstore(7, and(shr(32, key_tmp), 0xffffffff))
            sstore(8, and(key_tmp, 0xffffffff))
            
            let step := 1
            for { let i := 1 } lt(i, 4) { i := add(i, 1) } {
                
                first := and(shr(mul(add(sub(24, mul(i, 8)), 4), 8), tmp), 0xffffffff)
                second := and(shr(mul(sub(24, mul(i, 8)), 8), tmp), 0xffffffff)
                
                sstore(4, 0)
                
                for {let j := 0 } lt(j, 32) { j := add(j, 1) } {
                    
                    sstore(4, and(add(and(sload(4), 0xffffffff), shr(5, sload(2))), 0xffffffff))

                    let tmp11 := and(add(and(mul(second, 16), 0xffffffff), and(sload(5), 0xffffffff)), 0xffffffff)
                    let tmp12 := and(add(second, and(sload(4),0xffffffff)), 0xffffffff)
                    let tmp13 := and(add(div(second, 32), and(sload(6),0xffffffff)), 0xffffffff)
                    
                    first := and(add(first, xor(xor(tmp11, tmp12), tmp13)), 0xffffffff)
                    
                    let tmp21 := and(add(and(mul(first, 16), 0xffffffff), and(sload(7),0xffffffff)), 0xffffffff)
                    let tmp22 := and(add(first, and(sload(4),0xffffffff)), 0xffffffff)
                    let tmp23 := and(add(div(first, 32), and(sload(8),0xffffffff)), 0xffffffff)
                    second := and(add(second, xor(xor(tmp21, tmp22), tmp23)), 0xffffffff)

                }
                
                sstore(3, add(sload(3), add(shl(sub(192, mul(step, 32)), first), shl(sub(192, mul(i, 64)), second))))
                step := add(step, 2)
            }

        }
    }
}
```

## exp

* 分析交易可知先是进行了set_key操作，然后进行了Encrypt加密flag的操作，所以主要逻辑是在Encrypt加密函数中
* 题目给了源代码，分析代码，可知key可由中国剩余定理CRT计算

```
# -*- coding:utf-8 -*-
from functools import reduce
from Crypto.Util.number import long_to_bytes,bytes_to_long

def egcd(a, b):
    if 0 == b:
        return 1, 0, a
    x, y, q = egcd(b, a % b)
    x, y = y, (x - a // b * y)
    return x, y, q

def chinese_remainder(pairs):
    mod_list, remainder_list = [p[0] for p in pairs], [p[1] for p in pairs]
    mod_product = reduce(lambda x, y: x * y, mod_list)
    mi_list = [mod_product//x for x in mod_list]
    mi_inverse = [egcd(mi_list[i], mod_list[i])[0] for i in range(len(mi_list))]
    x = 0
    for i in range(len(remainder_list)):
        x += mi_list[i] * mi_inverse[i] * remainder_list[i]
        x %= mod_product
    return x

if __name__=='__main__':
    
    result = chinese_remainder([(231412341286754812414297, 208645382789328542577309), (126381254785148123414597, 29341064342757093333104), (438712649816519864511367, 227103917449451505785192)])

    print long_to_bytes(result)
```

* 分析可得Encrypt其实是tea加密，可通过如下脚本计算

```
#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
from ctypes import *

def encipher(v, k):
    y = c_uint32(v[0])
    z = c_uint32(v[1])
    sum = c_uint32(0)
    delta = 0x9e3779b9
    n = 32
    w = [0,0]

    while(n>0):
        sum.value += delta
        y.value += ( z.value << 4 ) + k[0] ^ z.value + sum.value ^ ( z.value >> 5 ) + k[1]
        z.value += ( y.value << 4 ) + k[2] ^ y.value + sum.value ^ ( y.value >> 5 ) + k[3]
        n -= 1

    w[0] = y.value
    w[1] = z.value
    return w

def decipher(v, k):
    y = c_uint32(v[0])
    z = c_uint32(v[1])
    sum = c_uint32(0xc6ef3720)
    delta = 0x9e3779b9
    n = 32
    w = [0,0]

    while(n>0):
        z.value -= ( y.value << 4 ) + k[2] ^ y.value + sum.value ^ ( y.value >> 5 ) + k[3]
        y.value -= ( z.value << 4 ) + k[0] ^ z.value + sum.value ^ ( z.value >> 5 ) + k[1]
        sum.value -= delta
        n -= 1

    w[0] = y.value
    w[1] = z.value
    return w

if __name__ == "__main__":
    key = [0x6b65795f, 0x74686973, 0x5f69735f, 0x6b65795f]

    # 1970527074032043059410457910532573615730510348629701619382 = 0xfa5714574e8de96cc4ff6dcbae35a7c1ae0792b77b5b31ba
    enc = [0x505d4339, 0x47f27742, 0xf60b06f3, 0x50f25834, 0x50a1f722, 0x1380eeb6]
    flag = ''
    for i in range(3):
        x = decipher(enc[i*2:i*2+2], key)
        for i in x:
            tmp = hex(i)[2:-1]
            for i in range(0,len(tmp),2):
                flag += chr(int(tmp[i:i+2], 16))
    print flag
    # flag{ETH_TEA_ENC_to_ok!}
```
