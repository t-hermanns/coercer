pragma solidity ^0.4.0;

interface IERC20 {
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function transfer(address recipient, uint256 amount) external returns (bool);
    function allowance(address owner, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transferFrom(address sender, address recipient, uint256 amount) external returns (bool);
    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);
}

contract InteractingContract{

    function sendTransfer(address to, uint256 value) public {
        IERC20 token = IERC20(0x4000000000000000000000000000000000000001);
        token.transferFrom(0x4321, to, value);
    }

}