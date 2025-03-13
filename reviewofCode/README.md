# VS Code Code Analyzer Extension

This is a VS Code extension that analyzes selected code by sending it to a local Python server and displays the results in a Markdown preview window.

## Features
- Analyzes selected code for issues.
- Sends the code to a local server for processing.
- Displays the analysis results in a new Markdown preview window.

## Installation
1. Clone this repository or copy the files into your VS Code extension folder.
2. Run `npm install` inside the extension directory to install dependencies.
3. Start your local Python analysis server at `http://localhost:5000/analyze`.
4. Open the extension project in VS Code and press `F5` to launch a new Extension Development Host window.

## Usage
1. Open a code file in VS Code.
2. Select the code snippet you want to analyze.
3. Press `Ctrl+Shift+P` to open the command palette.
4. Search for and run `Finderrors`.
5. The analysis results will appear in a new Markdown preview window.

## Requirements
- Node.js and npm installed.
- Python server running at `http://localhost:5000/analyze`.
- VS Code installed.

## Extension Files
- `extension.js`: Main extension logic.
- `package.json`: VS Code extension metadata and command registration.
- `README.md`: Documentation.

## License
This extension is open-source. Feel free to modify and distribute.

