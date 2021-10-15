pragma solidity ^0.5.10;

contract Launcher{
    uint256 public deadline;
    function setdeadline(uint256 _deadline) public {
        deadline = _deadline;
    }

    constructor() public {
        deadline = block.number + 100;
    }
}