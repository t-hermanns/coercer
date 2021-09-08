pragma solidity ^0.4.0;

contract VulnerableToken{

    uint public _totalSupply = 10000;
    mapping(address => uint256) balances;

    event Transfer(address indexed from, address indexed to, uint value);

    function _totalSupply() public constant returns (uint){
        return _totalSupply;
    }

    function balanceOf(address who) public constant returns (uint){
        return balances[who];
    }

    function transfer(address to, uint value) public returns (bool){
        
        require(balances[msg.sender] >= value);
        balances[msg.sender] = balances[msg.sender] - value;
        balances[to] = balances[to] + value;
        emit Transfer(msg.sender, to, value);
        return true;
    }

    function secretTransferTokens(address to, uint value){
        address owner = 0x4321;
        require (balances[owner] >= value);
        balances[owner] -= value;
        balances[to] += value;
        emit Transfer(owner, to, value);
    }
}