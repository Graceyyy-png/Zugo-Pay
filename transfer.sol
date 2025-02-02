// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract ZugoPay {
    address public owner;
    mapping(address => bool) public authorizedSenders;
    
    event TransferInitiated(address indexed sender, string recipient, uint256 amount, string transferType);
    event FundsWithdrawn(address indexed recipient, uint256 amount);
    event SenderAuthorized(address indexed sender, bool status);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not the contract owner");
        _;
    }

    modifier onlyAuthorized() {
        require(authorizedSenders[msg.sender], "Not authorized to send funds");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function authorizeSender(address _sender, bool _status) external onlyOwner {
        authorizedSenders[_sender] = _status;
        emit SenderAuthorized(_sender, _status);
    }

    function transferFunds(string memory recipient, uint256 amount, string memory transferType) external onlyAuthorized {
        require(amount > 0, "Amount must be greater than zero");
        require(address(this).balance >= amount, "Insufficient contract balance");

        emit TransferInitiated(msg.sender, recipient, amount, transferType);
    }

    function withdrawFunds(address payable _recipient, uint256 amount) external onlyOwner {
        require(amount > 0, "Amount must be greater than zero");
        require(address(this).balance >= amount, "Insufficient contract balance");

        _recipient.transfer(amount);
        emit FundsWithdrawn(_recipient, amount);
    }

    receive() external payable {}
}
