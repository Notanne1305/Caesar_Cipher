# Caesar Cipher

A simple Python implementation of the Caesar Cipher — one of the oldest encryption techniques — that lets you encrypt and decrypt messages using a shift key.

## How It Works

Each letter in your message is shifted forward (encryption) or backward (decryption) by a fixed number of positions in the alphabet. Non-alphabetic characters (numbers, punctuation, spaces) are left unchanged.

**Example with shift = 3:**
```
Plaintext:  Hello, World!
Ciphertext: Khoor, Zruog!
```

## Usage

Run the program:
```bash
python Caesar_Cipher.py
```

You'll be presented with a menu:
```
1. Encrypt a message
2. Decrypt a message
3. Run test cases
4. Exit
```

Enter your message and a shift key between **0 and 25** when prompted.

## Features

- Encrypts and decrypts any text message
- Preserves letter case (upper/lowercase)
- Handles large shift values via modulo 26 normalisation
- Includes automated test cases covering edge cases and round-trips
