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

# PRAAKTIKUM 2 - FINITE STATE MACHINE

## Definisi FSM

Di sini kita mendefinisikan komponen-komponen formal sebuah FSM (Finite State Machine). `STATES` adalah himpunan semua state yang dimiliki mesin. `ALPHABET` adalah himpunan simbol yang bisa dibaca mesin, dalam kasus ini hanya '0' dan '1'. `START_STATE` adalah state awal tempat mesin mulai bekerja, yaitu 'S'. `ACCEPT_STAT`E adalah himpunan state yang menyatakan string diterima, yaitu hanya 'B'.

`TRANSITION` adalah kamus dua tingkat yang merepresentasikan fungsi transisi `δ(state, karakter) → state_baru`. Misalnya `TRANSITION['A']['0']` menghasilkan 'C', artinya jika mesin berada di state A lalu membaca karakter 0, mesin pindah ke state C (trap state karena ada substring 00).

## Fungsi `jalankan_fsm`

Fungsi menerima sebuah string lalu mensimulasikan cara kerja mesin FSM karakter per karakter. Prosesnya dimulai dari `START_STATE`, kemudian setiap karakter dibaca satu per satu. Jika karakternya bukan '0' atau '1', fungsi langsung melempar error. Setiap perpindahan state dicatat ke dalam list `jejak` sebagai pasangan `(karakter, state_baru)`.

Setelah semua karakter selesai diproses, dicek apakah state terakhir ada di `ACCEPT_STATE`. Fungsi mengembalikan dua nilai: boolean `diterima` dan list `jejak` yang bisa digunakan untuk menampilkan trace perjalanan mesin.

# Fungsi `tampilkan_hasil`

Fungsi ini bertanggung jawab memformat dan mencetak hasil ke layar. Pertama dicek apakah string kosong. Jika iya langsung ditolak karena bahasa L mensyaratkan panjang minimal 1 karakter `(0+1)⁺`. Jika ada error karakter tidak valid, pesan error ditampilkan dengan aman melalui blok `try/except`.

`teks_jejak` adalah string yang menggambarkan perjalanan mesin seperti `S —0→ A —1→ B`. Ini membantu pengguna memahami kenapa sebuah string diterima atau ditolak. Jika string ditolak, alasan spesifik juga dicetak: apakah karena masuk trap state C (ada substring 00) atau karena state akhir bukan B (karakter terakhir bukan 1).

# Mode Interaktif

Bagian ini membuat program berjalan secara interaktif di terminal. Loop `while True` terus meminta input dari pengguna sampai pengguna mengetik kata kunci keluar. Fungsi `.strip()` dipakai untuk membersihkan spasi di awal/akhir input agar tidak mengganggu pemeriksaan. Setiap string yang dimasukkan langsung diteruskan ke `tampilkan_hasil()` dan hasilnya langsung muncul di bawahnya.
