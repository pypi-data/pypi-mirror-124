# UniqPy

UniqPy is a UNIQUAC-based tool designed for vapor-based quantification of multicomponent systems. Due to UniqPy deals only with vapor phase it is able to quantify only volatile organic compounds (VOCs).

## Dependenicies

Only the `scipy` python library is required.

## Usage

### Model fitting

To apply the model, a number of parameteres should be found. First, the relative Van der Waals volumes and surface areas of molecules should be found. We recommend the MSMS algorithm implemented as an easy-to-use PyMol plugin. The next stage is an optimization of energy parameters which describe all binary intereations in the mixture. The optimization requires experimantal data obtained for both source and vapor phase using different analytical methods or synthetic mixures with a known chemical's composition. Suppose that `x.txt` contains the matrix where each column means the substance, each row means the sample, and values means relative concetrations of the substances for each sample in the source (mainly liquid) phase. The file named `y.txt` contains the same information but about vapor phase relative pressures. The fitting can be performed by command

`uniqpy fit -l x.txt -v y.txt -q Q.txt -r R.txt -p parameters.txt`

`Q.txt` and `R.txt` files contains molecular surface areas and volumes. Samples are availabe in the `test` folder in this repository.


### Vapor data transforming

Vapor-to-liquid transformation can be performed with

`uniqpy transform -v y.txt -q Q.txt -r R.txt -p parameters.txt`



### Rereferences

will be added