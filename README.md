<p align="center">
    <img src="./resources/banner.png">
</p>

A Python CLI tool used for rule-based asset and file renaming - because your mess is our mess, and I don't like messy asset names. Tell us when, and we'll organize the chaos.

When working with assets from various sources, each author tends to have their own naming conventions - and I have mine too. This tool exists to make renaming files consistent, fast, and painless.

With a single command, all files in a folder can be automatically renamed. NOM is shipped as a single standalone executable (built with PyInstaller), meaning you don't need Python installed - just download it and run it.

## Features

- Built using Python.
- Normalizes file names to lower case.
- Provides configurable ruleset:
  - Supports ordering technical map types at the end of file names.
  - Supports number padding for animation frames.
  - Supports normalizing characters used to separate words.

**Preview:**

| Old Name                          | New Name                       |
| --------------------------------- | ------------------------------ |
| frame diffuse METAL .png          | frame_diffuse_metal.png        |
| NoRmAl 1005 Frame 055-metal- .png | 1005_frame_55_metal_normal.png |
| frame 69 - -.png                  | frame_069.png                  |

## Getting Started

### Using NOM

To use the NOM, download the latest release and run it in your favorite terminal.

```bash
-p, --path PATH  Path to directory containing files/assets which you want to rename.

-d, --dry        Dry run - shows what files would be renamed without actually renaming them.
-nl, --no_logo   When set, no logo and tagline will be shown - alternatively, can be disabled in config.

-r, --reset      Resets the configuration file to it's default state.
-c, --config     Open configuration file using the default text editor.
-h, --help       Show help message and exit.
```

**Examples:**

For each command you can use either the short (`-a`) or the long (`--argument`) argument.

```bash
# Run NOM and normalize all files within the `assets` directory.
nom -p <path>/assets

# Run NOM in dry run mode; no files will be modified.
nom -d -p <path>/assets

# Edit NOM configuration file to customize behavior.
nom -c
```

### Developing NOM

To work on NOM, you'll need the following dependencies:

- Python: **>3.14**
- PipEnv: **v2026.0.3**

You should run Python in strict typing mode.

**Project Structure:**

```
root/
├── resources/      Used for GitHub readme.
├── src/            CLI source code.
|   ├── config.py       Handles configuration file.
|   ├── data.py         Data shared across the CLI tool.
|   ├── library.py      Main file normalizing logic.
|   ├── parser.py       Handles building the argument parser.
├── .gitignore      List of files to be ignored by git.
├── LICENSE         License file.
├── nom.py          Main entry file into CLI tool.
├── Pipfile         Dependencies used by the CLI tool.
├── Pipfile.lock    Lockfile for the dependencies.
├── README.md       Project readme file.
```

## Contributing

Contributions are what make the open source community an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this project better, please fork the repo and create a pull request. You can also simply open an issue with the relevant tag. Don't forget to give the project a star! Thank you! ❤️

## Releases

Visit [RELEASES](https://github.com/danielpokladek/nom/releases) to see previous releases, changelog, and the latest release.

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.