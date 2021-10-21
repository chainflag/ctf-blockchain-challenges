pragma solidity ^0.5.10;

import "./EasyBomb.sol";
import "./Launcher.sol";

contract Setup {
    EasyBomb public easyBomb;

    constructor(bytes32 _password) public {
        easyBomb = new EasyBomb(address(new Launcher()), _password);
    }

    function isSolved() public view returns (bool) {
        return easyBomb.power_state() == false;
    }
}
