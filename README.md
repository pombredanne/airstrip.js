AirStrip.js
=============

About
-------------

This project is meant to ease dealing with third-party javascript dependencies in ambitious client-side web projects.

Conceptually, Airstrip has similarities with Twitter's Bower.

Problem
-------------

Modern javascript projects usually depend on numerous third-party libraries and frameworks 
(say: requirejs, handlebars, i18n, emberjs, jasmine).

Picking these, building, minifying, tracking versions, possibly patching or forking them, maintaining dependencies, then integrating into a project can quickly become borringly repetitive and tedious.

Solution
-------------

The idea here is to help do that, by providing tools to quickly assemble dependencies from numerous, widely used libraries, build them uniformly, list various versions, then "dispatching" the results in a build directory to be then used by said projects - and obviously tools that help you do that for your own libraries.


Installation
-------------




API
-------------

Once the airstrip binary has been installed, you should cd to you project root source folder and may use the following commands.


Command:
```airstrip search emberjs```

Result:
```emberjs
```


Command:
```airstrip show emberjs```

Result:
```emberjs
```
-> all details and available versions


Command:
```airstrip require emberjs```

Result:
Create or update the project "airfile", in order to add emberjs in stable version to the build dependency list.


Command:
```airstrip require emberjs/stable```
```airstrip require emberjs/trunk```
```airstrip require emberjs/1.0```

Result:
Same as above, but explicitely require a specific version. "Stable" and "trunk" versions keywords always exist for any library, and are mapped to specific versions by the airfile descriptor maintainer.
Two different versions of the same library can be required.
Note that requiring a project that depends on other projects will require them as well, in the recommended version.
It's your responsability to keep that tidy.


Command:
```airstrip remove emberjs```
```airstrip remove emberjs/version```

Result:
Will remove the library from the project dependencies list, if present (possibly in the specified /version).


Command:
```airstrip edit newlibrary```

Result:
Will create and open in your chosen editor a new airfile descriptor for a library named "newlibrary" (that airfile descriptor being avalaible only in the current project/directory).
The placeholders for versions "stable" and "trunk" will be added (and will need to be documented), and any other version may be added as well.
If the keyword "system" is added (`airstrip system edit newlibrary`), the airfile descriptor will be created system-wide instead, hence made available globally for the airstrip command.





```airstrip list```
-> list all requested dependencies

```airstrip build```
-> build or rebuild all requested dependencies

```airstrip build somelibrary```
-> build or rebuild a specific library that has been requested


```airstrip install emberjs```
-> alias for `airstrip require emberjs && airstrip build emberjs`


<!-- airstrip build emberjs
-> build just emberjs, if it was requested
airstrip build emberjs -v 1.7
-> build just emberjs version 1.7 if it was requested
 -->
<!-- airstrip rebuild
-> force rebuild of requested dependencies
 -->



Command:
```airstrip use```

Output:
- flag1: currentValue1
    flag1 explanation
    long explanation
    long long explanation
- flag2: currentValue2 (default: differentValue2)
    flag2 explanation
- flag3: currentValue3 (default: differentValue3)
    flag3 explanation
    long explanation




-> list current configuration, default, and possibly overriden values

```airstrip use flag=value```
-> set a config flag to value


Current configuration flags:
- directory: destination path
- minify: true/false wether to minify files or not
- minifier: closure
- pattern: default to $type/$name/$version - can also use $longversion
- jshint: true/false run jshint on every dependency - will FAIL the build if jshint doesnt pass


<!-- airstrip system
-> list system dependencies needed to build the required formulas

airstrip system install
-> try to install system dependencies needed to build the required formulas
 -->







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





