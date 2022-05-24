<div align="center">

# vgonisanz's User Input Automatization

</div>

## Usage

TBD

## Development

To start developing this project, clone this repo and do:

```
make env-create
```

This will create a virtual environment with all the needed dependencies (using [tox](https://tox.readthedocs.io/en/latest/)). You can activate this environment with:

```
$ source ./.tox/uia/bin/activate
```

Then, you can run `make help`.
Learn more about the different tasks you can perform on this project using [make](https://www.gnu.org/software/make/).

### Upgrade dependencies

From scratch, use the following command to generate `requirements{-dev}.txt` files:

```
make env-compile
```

## Contributing

Please see the [Contributing Guidelines](./CONTRIBUTING.md) section for more details on how you can contribute to this project.

## License

[GNU General Public License v3](./LICENSE)
