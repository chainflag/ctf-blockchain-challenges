pragma solidity ^0.5.11;

import "./Montagy.sol";

contract Setup {
    Montagy public montagy;

    constructor(bytes memory _p2) public payable{
        montagy = (new Montagy).value(msg.value)();
        montagy.registerCode(_p2);
        montagy.newPuzzle(_p2);
    }

    function isSolved() public view returns (bool) {
        return address(montagy).balance == 0;
    }
}
