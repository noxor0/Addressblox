# AddressBlox

A dockerized simple address book implementation for all your address book needs. Need to find someone in your sizable address book? AddressBlox will search your address, and find any entry by name, address, or even age! With mulitple ways to use the program, Addressblox is sure to find its way into your life!

AddressBlox offers an interactive mode that allows you to search multiple different people in succession! Additionally, AddressBlox comes with an easy to use script that allows you to do single quick and dirty searches.

## Setup
A quick setup for AdressBlox is a simple make target that will `build`, `run`, and then start the `interact`ive AddressBlox prompt.
```
make all
```
*Note: If docker is not properly setup on your machine, you may have to docker as root to get full functionality.*

## Usage
`make all` will automatically set you up with an interactive prompt to search for address entries. If container is running and you would like to restart the interactive prompt, use `make interact`.

If a single look up is required running `./singlelookup.sh` provides the same functionality in an alternative package.
`./singlelookup.sh -h` for all the available commands.

Addressblox comes with a variety of easy to use commands to give you full control over the program. `make help` will provide alternative commands.

A simple address book implementation for all your address book needs.

## Sprint Board
Can be found [here](https://docs.google.com/spreadsheets/d/1yak-cNcikx1f9nvNYInIvDK-7EJftMJWaT8gevyBo4k/edit?usp=sharing)
