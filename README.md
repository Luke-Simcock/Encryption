## Encryption
Code for encrypting and decrypting data very securely.
note: some mentions of encryption may reefer to hashing but for simplicity hashing will be under the blanket of encrypting

## Functions
Test for proving code works is encrypt.py
data read from Storage.txt

## Design
It is intended to secure data (example used here is passwords)
It is intended to be simple enough to utilised by less knowledgeable programmers
It is intended to provide a range of encryption 
It is intended to utilise a safe amount of the devices resources to balance speed and encryption strength 
It is intended to work on both low power hardware and high level enterprise hardware.
It uses scrypt to encrypt data and allows the user to enter a custom amount of resources (RAM) to be used for the password
The more resources that are used on the encryption will require any password attempt to use the same amount of resources.
This means that if you have a very powerful device with a lot of resources available you could use a large amount of them to essentially block any attackers with less resources

## Testing
You can test this program yourself if you run the program, ideally on higher end hardware (+16GB RAM)
Run a test encryption and watch your resources used increase for the duration of the encryption
If you select a value over 25% of your available RAM there will be a warning showing your available RAM and ask the user if they want to continue anyway
This safeguard of 25% will provide a safe barrier for inexperienced users while letting users who need the best possible encryption have the custom amount they need.
If the program is about to crash it will automatically quit on its own safely before it fails catastrophically.

## Additional info
Encryption currently only effects password. could be added to username for additional security. 
A second layer of encryption may be added to lines of the txt file for additional security if a majority of data on lines are sensitive and a blanket encryption will be more simple.
It is recommended to use 25% of your available RAM for each encryption (this is what Auto will select)

## Download
# (Add links for scripts to automatically install all files and dependencies)
Linux: 
Mac: 
Windows: 

Automatic: 
