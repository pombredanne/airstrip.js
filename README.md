AirStrip.js
=============

This project is meant to ease dealing with and tracking third-party javascript dependencies in large projects.


Background
-------------

Modern js projects usually depend on numerous third-party libraries and frameworks 
(say: requirejs, handlebars, i18n, emberjs, jasmine).

Tracking versions of these, possibly patching or forking them, maintaining deps lists, then integrating 
into the project can quickly become tedious.

The idea here is to help manage that, and list such dependencies (and versions) in YAML, build them uniformly,
"dispatching" the results in a build directory to be then used by said projects.


Technology
-------------

We use puke (https://github.com/webitup/puke), a (inhouse) versatile python build system.

Dependencies are listed in YAML.

And ah, all this is likely not working on windows (though we know it does on OSX and reasonable Linuxes).

How to use
-------------

- clone: `git clone https://github.com/jsBoot/airstrip.js`
- install puke: `pip install puke`
- build it as-is: `cd aistrip.js; puke all`

Check the "build" directory.

Doesn't work?
-------------

You probably miss a build dependency required by one or the other third-party projects.
Puke usually give you a hint about what's going wrong.

Do you have ruby installed, along with rvm and bundle? If not, grab rvm and gem install bundle.
Do you have nodejs and npm? If not, install them (aptitude install node, or brew install node, or
whichever method suits you).

Not interested in the provided dependencies and their build requirements? Just wipe-out the Collection
node (see down below) and specify what you're interested in.


Configuration
-------------

Edit puke-yak.yaml:
- create a new node "user-USER-box-BOX:", where USER is your unix nickname, and BOX the result of the `uname` command.
This node will be used to "specialize" your configuration (the generic configuration being stored in the "yak:" node)
- add (at least) a node for "DEPLOY_ROOT": this is where the result of the build will be put (and likely from where
your web server will serve said resources)
- when done editing, puke again (`puke all`)

Build result
-------------

In your DEPLOY_ROOT directory you will find:
- a number of "static" resources, copied from the src directory - these are mondane, edit or remove them at will
- a lib directory, with category subdirectories, containing said built dependencies: frameworks (emberjs, jquery), 
loaders (requirejs, labjs), plugins, tooling, shims, etc
- an airstrip.yaml file, containing a list of everything that has been built - this is the manifest to be used
in other projects or build systems using this

Every dependency has been built or fetched, in versions specified in the yaml file, renamed, and minified
(we use google closure to minify both css and js files, ECMA5 - not strict).

Listing and managing simple dependencies
-------------

Edit the puke-yak.yaml file again.

Get the Yak.COLLECTION node.

A typical entry looks like ("stacktrace.js" here):

```
stacktrace:
    "License": "PublicDomain"
    "Destination": "shims-plus"
    "Source":
        stacktrace-0.3.js: "https://github.com/downloads/eriwen/javascript-stacktrace/stacktrace-0.3.js"
        stacktrace-jsboot.js: "https://raw.github.com/webitup/javascript-stacktrace/master/stacktrace.js"
        stacktrace-trunk.js: "https://raw.github.com/eriwen/javascript-stacktrace/master/stacktrace.js"
```

The root node ("stacktrace") is purely casual.

You should always specify the license of the project, obviously.

The "Destination" node is a category directory (will live under the lib/ output folder).

The "Source" node list "versions" that you want to track for this library. Each version is a key
value pair, where the key is the final name you desire, and the value the url where to find the source.

In the case of stacktrace, we track three versions (a stable release, a forked release, and the upstream trunk).


Zipped dependencies
-------------

Some libraries come released in zip files.

Using these just requires:
- to have a "WHATEVER.zip: http://sourceurl" entry in your "Source" node
- to specify what to get from the zip in a "Build" node.

For example, LABJS:

```
lab:
    "License": "MIT"
    "Destination": "loaders"
    "Source":
        lab-2.0.3.zip: "http://labjs.com/releases/LABjs-2.0.3.zip"
        lab-jsboot.js: "https://raw.github.com/getify/LABjs/master/LAB.src.js"
        lab-trunk.js: "https://raw.github.com/getify/LABjs/master/LAB.src.js"
    "Build":
        type: 'zip'
        dir: 'LABjs-2.0.3'
        production:
            lab-2.0.3.js: 'LAB.src.js'
```

Here we track three versions: two direct "source form factor", and one zip (the lab-2.0.3.zip entry 
in the "Source" node).
In order to extract a specific file from the zip, we define a "Build" section, type "zip", we name
the "dir" resulting from the zip extraction, and a "production" node that specifies (using the same
key value syntax as the "Source" node) which files (from the extracted dir) to get and rename.


Git repositories and actual builds
-------------

In order to clone a git repository, just add a "git: sourceurl" entry in your "Source" node.

If there is a build step in order to produce the actual result, you specify that using the "Build" node.

For example, Emberjs is built that way:

```
ember:
    "License": "MIT"
    "Destination": "frameworks"
    "Source":
        ember.prod-0.9.6.js: "https://github.com/downloads/emberjs/ember.js/ember-0.9.6.min.js"
        ember.debug-0.9.6.js: "https://github.com/downloads/emberjs/ember.js/ember-0.9.6.js"
        ember.prod-1.0.pre.js: "https://github.com/downloads/emberjs/ember.js/ember-1.0.pre.min.js"
        ember.debug-1.0.pre.js: "https://github.com/downloads/emberjs/ember.js/ember-1.0.pre.js"
        git: "git://github.com/emberjs/ember.js.git"
    "Build":
        type: "rake"
        dir: "ember.js"
        production:
            ember.debug-trunk.js: "dist/ember.js"
            ember.prod-trunk.js: "dist/ember.prod.js"
```

... specifies a git entry in the Source list. Then requires build type "rake". Then copy two files
from the dir.

Understanding build and build types
-------------

For now, the following build types are "supported":
- rake
- thor
- make

You can pass random additional arguments to the command if you want, adding an "extra" node in the "Build" node.

Specifying any other build type (like "zip") will actually trigger no build operation, but is a way to let
you specify a "working" directory and copy files operations (using the "production" node) from a random dir ("dir").

There also exist the experimental "sh" build type. By specifying "extra" you can perform *any* build operations that way.


License
-------------


MIT license.
Note, though, that the result of the build it produces contains numerous softwares with various licenses,
and that by using them means you should agree with their individual licenses, not with the MIT license of this system itself. 