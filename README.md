# NOM - Normalize Our Mess

A Python based CLI tool used for rule-based asset and file renaming - because your mess, is our mess and I don't like messy asset names; you tell us when, and we organize the mess.

## Features

- Built using Python, with Technical Art in mind.
- Renames files and assets to match the specified ruleset.
- Automatically orders technical map (image) types to be last in the name (diffuse, normal, roughness, etc.)
- For animations, automatically adds padding to the last number in the name - otherwise strips unnecessary zeroes.
- Replaces dashes, spaces, and any other variants of spaces in names with underscores.

## Examples
  
```bash
# Simple cleanup of the name
frame diffuse METAL .png > frame_diffuse_metal.png

# Ordering of words when specified word is detected
NoRmAl Frame 055-metal- .png > frame_55_metal_normal.png

# Animation frame padding is automatically added to names
frame 69 - -.png > frame_069.png
```

## Getting Started

TODO

## Contributing

Contributions are what make the open source community an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

If you have a suggestion that would make this project better, please fork the repo and create a pull request. You can also simply open an issue with the relevant tag. Don't forget to give the project a star! Thank you! ❤️

## Releases

Visit [RELEASES]() to see previous releases, changelog, and the latest release.

## License

Distributed under the MIT License. See [LICENSE](./LICENSE) for more information.