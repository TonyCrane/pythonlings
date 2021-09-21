# Pythonlings

Welcome to Pythonlings, an automated Python tutorial program (inspired by [Rustlings](https://github.com/rust-lang/rustlings) and [Haskellings](https://github.com/MondayMorningHaskell/haskellings)).

## WIP
This program is still working in progress. Now it just has a stupid framework, and lack of exercises.
Here is a TODO-list: (welcome everyone to contribute by opening pull requests :)
- [ ] exercises 
    - [ ] variables
    - [ ] lists
    - [ ] conditions
    - [ ] dicts
    - [ ] loops
    - [ ] functions
    - [ ] classes
    - ...(?)
- [ ] improve the structure of this program
- [ ] improve `test` function and use global variables for countings instead of using coroutines
- [ ] add more functions to `pythonlings list` command
- [ ] ...
- (This project is so poorly written that there are endless things that need to be improved \_(:з」∠)\_)

## Install
1. Clone this repository
    ```sh 
    $ git clone https://github.com/TonyCrane/pythonlings.git 
    $ cd pythonlings
    ```
2. Install pythonlings through pip 
    ```sh 
    $ pip install -e .
    ```
3. Run pythonlings!
    ```sh 
    $ pythonlings 
    ```

## Run Exercises 
```text
usage: pythonlings [-h] [-v] [command [command ...]]

Pythonlings is a collection of small exercises to get you used to writing and reading Python code

positional arguments:
  command        the commend you want to execute

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  show the executable version

commands:
  verify            Verifies all exercises according to the recommended order
  watch             Reruns `verify` when files were edited
  run {exercise}    Runs a single exercise
  hint {exercise}   Returns a hint for the given exercise
  list              Lists the exercises available in Rustlings
```
(I'm just too lazy to write it. I'll make it up later (gugugu) \_(:з」∠)\_)

