# Dissect documentation

This project houses the Sphinx documentation for the Dissect project.

## Build and instructions

Start by checking out the submodules if you haven't done so already:

```bash
git submodule update --init --recursive
```

If you want to update all submodules add `--remote` to the previous command.

Create a new virtual environment, install the dependencies and build the Sphinx project.

```bash
pip install -r requirements.txt
cd docs && make html
```

If you run into build issues, clean the Sphinx output directory and AutoAPI output:

```bash
cd docs && make clean
```

When writing documentation you can use the convenience command below. This rebuilds 
the Sphinx project when source files change and automatically reloads your browser.

Please note that in order for the `make watch` command to work, you will have to 
run `make html` first at least once.

```bash
cd docs && make watch
```

## Contributing

The Dissect project encourages any contribution to the codebase. To make your contribution fit into the project, please
refer to [the style guide](https://docs.dissect.tools/en/latest/contributing/style-guide.html).

## Copyright and license

Dissect is released as open source by Fox-IT (<https://www.fox-it.com>) part of NCC Group Plc
(<https://www.nccgroup.com>).

Developed by the Dissect Team (<dissect@fox-it.com>) and made available at <https://github.com/fox-it/dissect>.

License terms: AGPL3 (<https://www.gnu.org/licenses/agpl-3.0.html>). For more information, see the LICENSE file.
