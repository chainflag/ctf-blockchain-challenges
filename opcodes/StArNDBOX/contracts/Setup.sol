pragma solidity ^0.5.11;

import "./StArNDBOX.sol";

contract Setup {
    address payable public instance;

    constructor() public payable {
        StArNDBOX stArNDBOX = new StArNDBOX();
        instance = address(uint160(address(stArNDBOX)));
        instance.transfer(msg.value);
    }

    function isSolved() public view returns (bool) {
        return instance.balance == 0;
    }
}
