# TOSEC Manager

TOSEC Manager is a powerful command-line interface (CLI) tool designed to efficiently catalog and organize your collection of TOSEC (The Old School Emulation Center) files. Implemented in Python, this tool not only parses TOSEC file naming conventions to extract valuable metadata—such as title, year, publisher, and language—but also organizes these files into structured directories. This organization facilitates easy access and use with emulators, ensuring that your digital collection is both manageable and ready for use.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Installation
1. **Clone the Repository**: Download the repository to your local machine.
   ```bash
   git clone <repository-url>
   cd tosec-manager
   ```

2. **Ensure Python is Installed**: Make sure you have Python installed (version 3.6 or newer).

3. **Install Dependencies**: Install the required packages if needed (e.g., `click`).
   ```bash
   uv sync
   ```

## Usage

TOSEC Manager is a command-line tool that helps in cataloging and organizing your TOSEC file collection for use with emulators. The main script, `tosec.py`, allows you to:

- **Catalog Files**: Organize files into directories based on their initial characters, making it easier to manage large collections.
- **Limit Files per Directory**: Specify a limit on the number of files per directory to ensure optimal organization and accessibility.
- **Create Emulator-Ready Copies**: Copy organized files to a specified location, ready for use with your favorite emulators.

### Command-Line Options

- `--limit`: Specifies the maximum number of files per directory.
- `--copy-to`: Path to the directory where organized files will be copied.
- `path`: Path to the directory containing TOSEC files to be processed.

### Example Usage

```bash
python tosec.py --limit 100 --copy-to /path/to/destination /path/to/source
```

This command will organize the TOSEC files from `/path/to/source`, limit the number of files per directory to 100, and copy them to `/path/to/destination`.

## Contributing

Contributions to TOSEC Manager are welcome. Please ensure that any new code is covered by tests and adheres to the project's coding standards.


