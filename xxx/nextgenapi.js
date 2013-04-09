airstrip show emberjs
-> all details and available versions

airstrip require emberjs
-> add emberjs stable to the project airfile

airstrip require emberjs -v stable
-> add emberjs version stable to the project airfile

airstrip require emberjs -v trunk
-> add emberjs version trunk to the project airfile

airstrip require emberjs -v 1.7
-> add emberjs version 1.7 to the project airfile


airstrip edit emberjs -v mine
-> edit emberjs airstrip installer for version "mine"

airstrip require emberjs -v mine
-> add emberjs version mine to the project airfile

airstrip remove emberjs
airstrip remove emberjs -v 1.7
airstrip remove emberjs -v all
-> remove project dependency to emberjs (stable), 1.7, or all previously requested versions

airstrip list
-> list all requested dependencies

airstrip build
-> build all requested dependencies

airstrip build emberjs
-> build just emberjs, if it was requested
airstrip build emberjs -v 1.7
-> build just emberjs version 1.7 if it was requested

airstrip rebuild
-> force rebuild of requested dependencies



airstrip install emberjs
-> alias: airstrip require emberjs && airstrip build emberjs


airstrip system
-> list system dependencies needed to build the required formulas

airstrip system install
-> try to install system dependencies needed to build the required formulas


airstrip use
-> list configuration, and possible flags

airstrip use flag value
-> set a config flag to value


Current configuration flags:
- directory: destination path
- minify: true/false wether to minify files or not
- minifier: closure
- pattern: default to $type/$name/$version - can also use $longversion
- jshint: true/false run jshint on every dependency - will FAIL the build if jshint doesnt pass




Dependencies are managed inside the project airfile:
require:
  $name:
    $version
    $version
    $version
config:
  directory: $directory
  minify: true
  minifier: 



airstrip install emberjs (= require + build)





