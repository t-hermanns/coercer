pragma solidity ^0.4.0;

contract Token{
    uint public _totalSupply = 10000;
    mapping(address => uint) balances;
    mapping(address => mapping (address => uint)) allowed;

    event Transfer(address indexed from, address indexed to, uint value);
    event Approval(address indexed owner, address indexed spender, 
            uint value);
    
    // constructor
    function token() {
            balances[msg.sender] = _totalSupply;
    }
            
    function totalSupply() public view returns (uint){
            return _totalSupply;
    }

    function balanceOf(address owner) public view returns (uint){
            return balances[owner];
    }

    function transfer(address to, uint value) public returns (bool) {
            require(value <= balances[msg.sender]);
            balances[msg.sender] = balances[msg.sender] - value;
            balances[to] = balances[to] + value;
            emit Transfer(msg.sender, to, value);
            return true;
    }

    function approve(address spender, uint value) public returns (bool) {
            allowed[msg.sender][spender] = value;
            emit Approval(msg.sender, spender, value);
            return true;
    }

    function transferFrom(address from, address to, uint value) public 
        returns (bool) {
            require(value <= balances[from]);
            require(value <= allowed[from][msg.sender]);
            balances[from] = balances[from] - value;
            allowed[from][msg.sender] = allowed[from][msg.sender] - value;
            balances[to] = balances[to] + value;
            emit Transfer(from, to, value);
            return true;
    }

    function allowance(address owner, address spender) public view 
        returns (uint) {
            return allowed[owner][spender];
    }
}