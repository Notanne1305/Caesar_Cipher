# =============================================================================
# Caesar Cipher Program
# =============================================================================
# Description:
#   This program implements the Caesar Cipher, one of the simplest and most
#   well-known encryption techniques. It works by shifting each letter of the
#   plaintext by a fixed number of positions (the "shift key") in the alphabet.
#
#   Encryption: Each letter is shifted FORWARD by the key amount.
#   Decryption: Each letter is shifted BACKWARD by the same key amount.
#
#   Example (shift = 3):
#     Plaintext:  H  e  l  l  o
#     Ciphertext: K  h  o  o  r
# =============================================================================


# -----------------------------------------------------------------------------
# Core Cipher Function
# -----------------------------------------------------------------------------

def caesar_cipher(text, shift, encrypt=True):
    """
    Shared helper that handles both encryption and decryption.

    Parameters:
        text     (str)  : The input message (plaintext or ciphertext).
        shift    (int)  : The number of positions to shift (0–25).
        encrypt  (bool) : True to encrypt (shift forward), False to decrypt
                          (shift backward). Defaults to True.

    Returns:
        str: The transformed message.

    How it works:
        - direction = +1 for encryption, -1 for decryption.
        - For each alphabetic character:
            1. Find the 0-based position relative to 'a' or 'A'.
            2. Add or subtract the shift amount.
            3. Apply modulo 26 to wrap around the alphabet.
            4. Convert back to the corresponding character.
        - Non-alphabetic characters (digits, spaces, punctuation) pass through
          unchanged.
        - Using (shift % 26) normalises any shift value, including very large
          ones (e.g., 52 → 0, 55 → 3).
    """
    result = ""
    direction = 1 if encrypt else -1

    for char in text:
        if char.isalpha():
            # Preserve case by anchoring to the correct base ASCII value
            base = ord('a') if char.islower() else ord('A')
            # Shift the character and wrap within the 26-letter alphabet
            shifted = (ord(char) - base + direction * (shift % 26)) % 26
            result += chr(shifted + base)
        else:
            # Non-alphabetic characters are left unchanged
            result += char

    return result


# -----------------------------------------------------------------------------
# Public Encryption / Decryption Wrappers
# -----------------------------------------------------------------------------

def caesar_encrypt(plain_text, shift):
    """
    Encrypts a plaintext message using the Caesar Cipher.

    Parameters:
        plain_text (str) : The message to encrypt.
        shift      (int) : The shift key (number of positions to shift forward).

    Returns:
        str: The encrypted (ciphertext) message.
    """
    return caesar_cipher(plain_text, shift, encrypt=True)


def caesar_decrypt(encrypted_text, shift):
    """
    Decrypts a ciphertext message encrypted with the Caesar Cipher.

    Parameters:
        encrypted_text (str) : The message to decrypt.
        shift          (int) : The shift key used during encryption.

    Returns:
        str: The decrypted (plaintext) message.
    """
    return caesar_cipher(encrypted_text, shift, encrypt=False)


# -----------------------------------------------------------------------------
# Input Validation
# -----------------------------------------------------------------------------

def get_valid_shift():
    """
    Prompts the user for a shift key and validates the input.

    Keeps asking until the user enters a valid integer between 0 and 25.

    Returns:
        int: A validated shift key in the range [0, 25].
    """
    while True:
        try:
            shift = int(input("Enter shift key (0-25): "))
            if 0 <= shift <= 25:
                return shift
            else:
                print("Error: Shift key must be between 0 and 25.")
        except ValueError:
            print("Error: Please enter a valid integer.")


# -----------------------------------------------------------------------------
# Menu Display
# -----------------------------------------------------------------------------

def display_menu():
    """Prints the main menu options to the console."""
    print("\nCaesar Cipher Menu:")
    print("1. Encrypt a message")
    print("2. Decrypt a message")
    print("3. Run test cases")
    print("4. Exit")


# -----------------------------------------------------------------------------
# Test Cases
# -----------------------------------------------------------------------------

def run_test_cases():
    """
    Runs a series of automated test cases and reports PASS/FAIL results.

    Test coverage:
        1. Basic encryption
        2. Basic decryption
        3. Large shift value  (normalisation via modulo 26)
        4. Mixed characters   (digits, punctuation, spaces preserved)
        5. Wrap-around        (letters near end of alphabet wrap correctly)
        6. Full round-trip    (encrypt then decrypt returns original text)
    """
    print("\n" + "=" * 50)
    print("Running Test Cases")
    print("=" * 50)

    passed = 0
    failed = 0

    def assert_equal(label, actual, expected):
        """Helper to compare actual vs expected and report result."""
        nonlocal passed, failed
        if actual == expected:
            print(f"  [PASS] {label}")
            passed += 1
        else:
            print(f"  [FAIL] {label}")
            print(f"         Expected : {expected!r}")
            print(f"         Got      : {actual!r}")
            failed += 1

    # ------------------------------------------------------------------
    # Test Case 1: Basic Encryption
    # ------------------------------------------------------------------
    print("\nTest Case 1 — Basic Encryption (shift = 3)")
    assert_equal(
        "Encrypt 'Hello, World!'",
        caesar_encrypt("Hello, World!", 3),
        "Khoor, Zruog!"
    )

    # ------------------------------------------------------------------
    # Test Case 2: Basic Decryption
    # ------------------------------------------------------------------
    print("\nTest Case 2 — Basic Decryption (shift = 3)")
    assert_equal(
        "Decrypt 'Khoor, Zruog!'",
        caesar_decrypt("Khoor, Zruog!", 3),
        "Hello, World!"
    )

    # ------------------------------------------------------------------
    # Test Case 3: Edge Cases
    # ------------------------------------------------------------------
    print("\nTest Case 3 — Edge Cases")

    # 3a. Large shift value: 52 % 26 == 0 → output should equal input
    assert_equal(
        "Large shift (52 ≡ 0 mod 26) — 'ABC xyz' unchanged",
        caesar_encrypt("ABC xyz", 52),
        "ABC xyz"
    )

    # 3b. Mixed characters: digits, punctuation, and spaces pass through
    mixed = "Test123!@# With Numbers & Symbols"
    assert_equal(
        "Mixed characters round-trip (shift = 5)",
        caesar_decrypt(caesar_encrypt(mixed, 5), 5),
        mixed
    )

    # 3c. Wrap-around: letters near the end of the alphabet wrap correctly
    assert_equal(
        "Wrap-around — 'XYZ' shift 5 → 'CDE'",
        caesar_encrypt("XYZ", 5),
        "CDE"
    )

    # 3d. Full round-trip with a sentence
    original = "The Quick Brown Fox Jumps Over The Lazy Dog"
    assert_equal(
        "Full round-trip (shift = 13)",
        caesar_decrypt(caesar_encrypt(original, 13), 13),
        original
    )

    # ------------------------------------------------------------------
    # Summary
    # ------------------------------------------------------------------
    print("\n" + "-" * 50)
    print(f"Results: {passed} passed, {failed} failed.")
    print("=" * 50)


# -----------------------------------------------------------------------------
# Main Program Loop
# -----------------------------------------------------------------------------

def main():
    """
    Entry point. Displays the menu and handles user input in a loop until
    the user chooses to exit.
    """
    print("Welcome to the Caesar Cipher Program!")

    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()

        if choice == '1':
            # --- Encryption mode ---
            plaintext = input("Enter the message to encrypt: ")
            shift = get_valid_shift()
            encrypted_message = caesar_encrypt(plaintext, shift)
            print(f"Encrypted message: {encrypted_message}")

        elif choice == '2':
            # --- Decryption mode ---
            ciphertext = input("Enter the message to decrypt: ")
            shift = get_valid_shift()
            decrypted_message = caesar_decrypt(ciphertext, shift)
            print(f"Decrypted message: {decrypted_message}")

        elif choice == '3':
            # --- Run automated tests ---
            run_test_cases()

        elif choice == '4':
            # --- Exit ---
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


# -----------------------------------------------------------------------------
# Program Entry Point
# -----------------------------------------------------------------------------

if __name__ == "__main__":
    main()