### Hexlet tests and linter status:
[![Actions Status](https://github.com/Unshock/python-project-lvl2/workflows/hexlet-check/badge.svg)](https://github.com/Unshock/python-project-lvl2/actions)
[![Python CI](https://github.com/Unshock/python-project-lvl2/actions/workflows/tests-and-linter-check.yml/badge.svg)](https://github.com/Unshock/python-project-lvl2/actions/workflows/tests-and-linter-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/dc7cb1754db6a42ae472/maintainability)](https://codeclimate.com/github/Unshock/python-project-lvl2/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/dc7cb1754db6a42ae472/test_coverage)](https://codeclimate.com/github/Unshock/python-project-lvl2/test_coverage)

## Difference generator study project for Hexlet.io 
### Description:
##### The project consists of a utility that visualizes the difference between two JSON or YAML files

##### There are three options that could be applied for the difference generator:

| Option   | Description                                                                                  |
|----------|----------------------------------------------------------------------------------------------|
| stylish  | Default option that shows difference in JSON-like style without commas and quotes            |
| json     | Option that shows difference in JSON style                                                   |
| plain    | Option that shows difference in plain style showing keys that were added, deleted or updated |

### Difference generator install
The project exists only on ***github*** and for usage could be installed using ***pip*** command:

    python3 -m pip install --user git+https://github.com/Unshock/python-project-lvl2.git

### Difference generator run
Run of the program is carried out by the command below:

    gendiff file_1 file_2
Options could be applied by the commands below: 
    
    gendiff file_1 file_2 --format stylish

    gendiff file_1 file_2 --format json

    gendiff file_1 file_2 --format plain

#### Asciinema demonstrations of install, get visualization and import of the module
[![asciicast](https://asciinema.org/a/2PgFE4iL2xzLrZznVYVMy86TY.svg)](https://asciinema.org/a/2PgFE4iL2xzLrZznVYVMy86TY)
[![asciicast](https://asciinema.org/a/5IrGK1rRG8G58eGOtWr9U4wqi.svg)](https://asciinema.org/a/5IrGK1rRG8G58eGOtWr9U4wqi)
[![asciicast](https://asciinema.org/a/fAMFPHHzbLOcmgaWwPfOb9wor.svg)](https://asciinema.org/a/fAMFPHHzbLOcmgaWwPfOb9wor)