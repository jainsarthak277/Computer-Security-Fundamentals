pragma solidity ^0.5.0;

/*
    This contract makes use of revert/require statements to handle erronous user inputs like calling play, reveal, withdraw out of order
    or calling play with a lower wage than player 1. Therefore, such erronous function call does not get committed and the MyEtherWallet
    will throw an error. MyEtherWallet does not show what the error is for some reason, just the message "gas required exceeds allowance 
    or always failing transaction"
    
    Passing anything else other than "rock", "paper", "scissors" to the encode_commitment function will return 0x0 which is an error
*/
contract rps_test {
    
    address owner;
    uint256 iterator;
    uint256 j;
    
    struct player_details {
        address player_addr;
        bytes32 commitment;
        uint256 wage;
        uint8 isReveal;
        uint8 moneyWithdrawn;
    }
    
    player_details player1;
    player_details player2;
    
    string public player1_choice;
    string public player2_choice;
    
    uint256 public player1_total_earnings;
    uint256 public player2_total_earnings;
    
    constructor () public{
        owner = msg.sender;
    }
    
    function encode_commitment(string memory choice, string memory rand)
        public pure returns (bytes32) {
            if(keccak256(abi.encodePacked(choice)) == keccak256(abi.encodePacked("rock")) || keccak256(abi.encodePacked(choice)) == keccak256(abi.encodePacked("paper")) || keccak256(abi.encodePacked(choice)) == keccak256(abi.encodePacked("scissors"))) {
                return sha256(bytes(string(abi.encodePacked(choice, rand))));    
            }
            else {
                return 0x0;
                //revert("Wrong choice entered");
            }
    }
    
    function play(bytes32 commitment) public payable { 
        uint256 wager = msg.value;
        
        if(iterator == 0){
            player1.player_addr = msg.sender;
            player1.wage = msg.value;
            iterator += 1;
            player1.commitment = commitment;
        }
        else if(iterator == 1 && msg.sender != player1.player_addr){
            if(player1.wage < wager) {
                msg.sender.transfer(wager - player1.wage);
                iterator += 1;
                player2.commitment = commitment;
                player2.player_addr = msg.sender;
                player2.wage = player1.wage;
            }
            else if(player1.wage == msg.value) {
                iterator += 1;
                player2.commitment = commitment;
                player2.player_addr = msg.sender;
                player2.wage = player1.wage;
            }
            else {
                msg.sender.transfer(wager);
                revert("Wage less than player 1");
            }
        }
        else {
            msg.sender.transfer(wager);
            revert("2 players already playing");
            
        }
    }
    
    function calculate_earnings() internal {
        
        if(keccak256(abi.encodePacked(player1_choice)) == keccak256(abi.encodePacked("rock")) && keccak256(abi.encodePacked(player2_choice)) == keccak256(abi.encodePacked("paper"))) {
            player2_total_earnings = player2.wage + player1.wage;
            player1_total_earnings = 0;
        }
        else if(keccak256(abi.encodePacked(player1_choice)) == keccak256(abi.encodePacked("rock")) && keccak256(abi.encodePacked(player2_choice)) == keccak256(abi.encodePacked("rock"))) {
            player2_total_earnings = player2.wage;
            player1_total_earnings = player1.wage;
        }
        else if(keccak256(abi.encodePacked(player1_choice)) == keccak256(abi.encodePacked("rock")) && keccak256(abi.encodePacked(player2_choice)) == keccak256(abi.encodePacked("scissors"))) {
            player2_total_earnings = 0;
            player1_total_earnings = player1.wage + player2.wage;
        }
        else if(keccak256(abi.encodePacked(player1_choice)) == keccak256(abi.encodePacked("paper")) && keccak256(abi.encodePacked(player2_choice)) == keccak256(abi.encodePacked("paper"))) {
            player2_total_earnings = player2.wage;
            player1_total_earnings = player1.wage;
        }
        else if(keccak256(abi.encodePacked(player1_choice)) == keccak256(abi.encodePacked("paper")) && keccak256(abi.encodePacked(player2_choice)) == keccak256(abi.encodePacked("rock"))) {
            player2_total_earnings = 0;
            player1_total_earnings = player1.wage + player2.wage;
        }
        else if(keccak256(abi.encodePacked(player1_choice)) == keccak256(abi.encodePacked("paper")) && keccak256(abi.encodePacked(player2_choice)) == keccak256(abi.encodePacked("scissors"))) {
            player2_total_earnings = player2.wage + player1.wage;
            player1_total_earnings = 0;
        }
        else if(keccak256(abi.encodePacked(player1_choice)) == keccak256(abi.encodePacked("scissors")) && keccak256(abi.encodePacked(player2_choice)) == keccak256(abi.encodePacked("rock"))) {
            player2_total_earnings = player1.wage + player2.wage;
            player1_total_earnings = 0;
        }
        else if(keccak256(abi.encodePacked(player1_choice)) == keccak256(abi.encodePacked("scissors")) && keccak256(abi.encodePacked(player2_choice)) == keccak256(abi.encodePacked("scissors"))) {
            player2_total_earnings = player2.wage;
            player1_total_earnings = player1.wage;
        }
        else if(keccak256(abi.encodePacked(player1_choice)) == keccak256(abi.encodePacked("scissors")) && keccak256(abi.encodePacked(player2_choice)) == keccak256(abi.encodePacked("paper"))) {
            player2_total_earnings = 0;
            player1_total_earnings = player1.wage + player2.wage;
        }
    }
    
    function reveal(string memory choice, string memory rand) public {
        
        if(iterator == 2) {
            bytes32 commitment = sha256(bytes(string(abi.encodePacked(choice, rand))));
            
            if(msg.sender == player1.player_addr && player1.isReveal == 0) {
                
                if(commitment == player1.commitment) {
                    player1_choice = choice;
                    j += 1;
                    player1.isReveal = 1;
                }
                else {
                    require (
                        commitment == player1.commitment,
                        "Wrong choice/string inputted"
                    );
                }
            }
            
            else if(msg.sender == player2.player_addr && player2.isReveal == 0) {
            
                if(commitment == player2.commitment) {
                    player2_choice = choice;
                    j += 1;
                    player2.isReveal = 1;
                }
                else {
                    require (
                        commitment == player2.commitment,
                        "Wrong choice/string inputted"
                    );
                }
            }
            else {
                revert("Non existent player");
            }
        
            if(j == 2) {
                calculate_earnings();
                j = 0;
            }
        }
        else {
            require (
                iterator == 2,
                "Both players not ready yet"
            );
        }
    }
    
    function withdraw() public { 
        uint256 amt;
        
        if(player1.isReveal == 1 && player2.isReveal == 1) {
            if(player1.player_addr == msg.sender && player1.moneyWithdrawn == 0) {
                player1.moneyWithdrawn = 1;
                amt = player1_total_earnings; 
                player1_total_earnings = 0; //This prevents recursive attacks
                msg.sender.transfer(amt);
            }
            else if(player2.player_addr == msg.sender && player2.moneyWithdrawn == 0) {
                player2.moneyWithdrawn = 1;
                amt = player2_total_earnings; 
                player2_total_earnings = 0; //This prevents recursive attacks
                msg.sender.transfer(amt);
            }
            else {
                revert("Non-existent player");
            }
            
            /* Condition when both players have withdrawn money - reset system */
            if(player2.moneyWithdrawn == 1 && player1.moneyWithdrawn == 1) {
                iterator = 0;
                player1.moneyWithdrawn = 0;
                player2.moneyWithdrawn = 0;
                player1.isReveal = 0;
                player2.isReveal = 0;
                player2.wage = 0;
                player1.wage = 0;
                player1_choice = "";
                player2_choice = "";
                //player2_total_earnings = 0;
                //player1_total_earnings = 0;
            }
        }
        else {
            require (
                player1.isReveal == 1 && player2.isReveal == 1,
                "Incorrect stage"
            );
        }
    }
    
    function get_rich() public {
        if(msg.sender == owner) {
            msg.sender.send(address(this).balance);    
        }
    }
}