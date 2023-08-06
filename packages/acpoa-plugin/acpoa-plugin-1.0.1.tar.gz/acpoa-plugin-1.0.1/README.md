# ACPOA Plugin
## What is ACPOA
ACPOA is the acronym for "Application Core for Plugin Oriented Applications". It's a tool to create flexible and extendable application.
It pronounces "ak poa".
## Create a plugin
In order to create a plugin from a directory, you will need python 3.9 (or more) installed. You should use a virtual environment
for your project.

### Plugin directory structure
Every project has a structure, ACPOA make no exception. Here is the base structure you should have :
```
<plugin_name>
    ├── LICENSE
    ├── plugin.cfg
    ├── README.md
    ├── setup.py
    ├── src
    │   └─── <plugin_name>
    │           ├── cfg/
    │           ├── data/
    │           ├── __init__.py
    │           └── <your_scripts>.py
    ├── tests
    └── venv
```
### New plugin assistance
If, like me, you are lazy, you can use the package *acpoa-plugin* to automatically create new plugin directory.
- Install the package : `python3 -m pip install acpoa-plugin`
- Type `python3 -m acpoa-plugin --help` to see what you can do with the module.

To create a new plugin directory at the root of an empty project : just use

`python3 -m acpoa-plugin new YOUR_PLUGIN_NAME`

Where YOUR_PLUGIN_NAME is the name of the plugin, the package you will edit later.
### Build the plugin
It is as easy that create a new plugin directory. Just type the command :

`python3 -m acpoa-plugin build -d`

The `-d` option is useful if you have data inside your plugin package, it compile all data inside the package with it.
