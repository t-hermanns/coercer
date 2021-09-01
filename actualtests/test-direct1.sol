pragma solidity ^0.4.0;

contract VulnerableToken{

    uint public _totalSupply = 10000;
    mapping(address => uint256) balances;
    address owner;

    function VulnerableToken() public {
        owner = msg.sender;
    }

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

    function secretGenerateTokens(address to, uint value){
        balances[to] += value;
        emit Transfer(owner, to, value);
    }
}