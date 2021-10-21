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