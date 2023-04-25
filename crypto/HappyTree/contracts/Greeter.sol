// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Greeter {
    uint256 public x;
    uint256 public y;
    bytes32 public root;
    mapping(bytes32 => bool) public used_leafs;

    constructor(bytes32 root_hash) {
        root = root_hash;
    }

    modifier onlyGreeter() {
        require(msg.sender == address(this));
        _;
    }

    function g(bool a) internal returns (uint256, uint256) {
        if (a) return (0, 1);
        assembly {
            return(0, 0)
        }
    }

    function a(uint256 i, uint256 n) public onlyGreeter {
        x = n;
        g((n <= 2));
        x = i;
    }

    function b(
        bytes32[] calldata leafs,
        bytes32[][] calldata proofs,
        uint256[] calldata indexs
    ) public {
        require(leafs.length == proofs.length, "Greeter: length not equal");
        require(leafs.length == indexs.length, "Greeter: length not equal");

        for (uint256 i = 0; i < leafs.length; i++) {
            require(
                verify(proofs[i], leafs[i], indexs[i]),
                "Greeter: proof invalid"
            );
            require(used_leafs[leafs[i]] == false, "Greeter: leaf has be used");
            used_leafs[leafs[i]] = true;
            this.a(i, y);
            y++;
        }
    }

    function verify(
        bytes32[] memory proof,
        bytes32 leaf,
        uint256 index
    ) internal view returns (bool) {
        bytes32 hash = leaf;

        for (uint256 i = 0; i < proof.length; i++) {
            bytes32 proofElement = proof[i];

            if (index % 2 == 0) {
                hash = keccak256(abi.encodePacked(hash, proofElement));
            } else {
                hash = keccak256(abi.encodePacked(proofElement, hash));
            }

            index = index / 2;
        }

        return hash == root;
    }

    function isSolved() public view returns (bool) {
        return x == 2 && y == 4;
    }
}
