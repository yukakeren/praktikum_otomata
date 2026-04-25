# Token Classifier

A Python-based analyzer with a GUI interface for tokenizing and classifying source code. This tool identifies and categorizes tokens from Python, C/C++, and Java.

## Installation

1. Clone or download the project
2. Navigate to the project directory:
   ```bash
   cd praktikum_otomata
   ```

## Usage

Run the application with:

```bash
python3 analyzer.py
```

## Overview

The Lexical Analyzer breaks down source code into tokens and classifies them into categories such as:
- Reserve Words (Python, C, Java keywords)
- Symbols and Punctuation
- Variables
- Mathematical Expressions
- Numbers (integers and floats)
- String Literals
- Comments

## Project Structure

```
praktikum_otomata/
├── analyzer.py         # Main entry point
├── gui.py              # GUI components and application window
├── lexer.py            # Tokenizer and lexical analysis logic
├── tokens.py           # Token definitions and constants
```

### File Descriptions

**tokens.py**
- Defines the Token dataclass
- Contains reserved words and mathematical functions lists
- Defines all token categories and color schemes for GUI display

**lexer.py**
- Contains the Lexer class for tokenization
- Implements regex-based token pattern matching
- Provides token categorization logic
- Handles multi-line tokens and line/column tracking

**gui.py**
- Implements the LexerApp class (main application window)
- Provides dark-themed UI with ttk widgets
- Handles user input and file operations
- Displays tokenization results in a table with filtering capability
- Includes export to JSON functionality

**analyzer.py**
- Entry point for the application
- Launches the GUI application

## Supported Reserve Words

### Python Keywords
- Control flow: if, elif, else, for, while, break, continue, pass
- Functions: def, return, lambda, yield
- Classes: class, super, self
- Exceptions: try, except, finally, raise
- Imports: import, from, as
- Others: and, or, not, in, is, None, True, False

### C/C++/Java Keywords
- Types: int, float, double, char, bool, void, string
- Access modifiers: public, private, protected, static
- OOP: class, interface, enum, extends, implements
- Others: new, this, const, var, auto

## Supported Math Functions

sin, cos, tan, log, log2, log10, sqrt, abs, pow, exp, ceil, floor, round, max, min, sum, pi, e, factorial, gcd, lcm, hypot, asin, acos, atan, atan2
