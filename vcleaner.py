import sys


HELP_TEXT: str = """Usage:
\tpython script.py show <input_file>
\tpython script.py clean <input_file> [output_file]
Example:
\tpython script.py clean dirty.txt clean.txt
\tpython script.py show dirty.txt
"""


def count_words(text: str) -> int:
    words = text.split()
    return len(words)


def clean_text_file(input_file: str, output_file: str) -> None:
    """
    Reads a text file, removes hidden/non-ASCII characters,
    and saves clean ASCII text to output file.
    """
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        original_length = len(content)
        original_words = count_words(content)

        print(f"\nOriginal length: {original_length} characters")
        print(f"Number of Words: {original_words}")

        cleaned = ""
        hidden_count = 0
        for char in content:
            ascii_val = ord(char)
            if (32 <= ascii_val <= 126) or ascii_val in [9, 10, 13]:
                cleaned += char
            else:
                hidden_count += 1

        cleaned_length = len(cleaned)
        cleaned_words = count_words(cleaned)
        hidden_removed = hidden_count

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cleaned)

        print(f"Cleaned Length: {cleaned_length} characters")
        print(f"Invisible characters removed: {hidden_removed}")
        print(f"Words count: {cleaned_words}")
        print(f"Clean version of file saved to: {output_file}\n")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")
    except Exception as e:
        print(f"Error: {e}")


def show_hidden_chars(input_file: str) -> None:
    """
    Shows what hidden characters are in the file (for debugging)
    """
    try:
        with open(input_file, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        original_length = len(content)
        original_words = count_words(content)

        hidden_chars = {}
        total_hidden = 0

        for char in content:
            ascii_val = ord(char)
            if not ((32 <= ascii_val <= 126) or ascii_val in [9, 10, 13]):
                if char not in hidden_chars:
                    hidden_chars[char] = 0
                hidden_chars[char] += 1
                total_hidden += 1

        print()
        if hidden_chars:
            print("Invisible characters found:")
            for char, count in sorted(
                hidden_chars.items(), key=lambda x: x[1], reverse=True
            ):
                print(f"  Find (ASCII {ord(char)}): {count} characters")
            print(f" Total Invisible Characters: {total_hidden} characters")
        else:
            print("No hidden characters found! Your file is clean")

        print(f"  Original Length: {original_length}")
        print(f"  Number of Words: {original_words}\n")

    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found!")


def main() -> int:
    if len(sys.argv) < 2:
        print(HELP_TEXT)
        return 1

    match sys.argv[1]:
        case "clean":
            if len(sys.argv) < 3:
                print("Error: Specify input file")
            else:
                input_file = sys.argv[2]
                output_file = (
                    sys.argv[3] if len(sys.argv) > 3 else "cleaned_" + input_file
                )
                clean_text_file(input_file, output_file)
        
        case "show":
            if len(sys.argv) < 3:
                print("Error: Specify input file")
            else:
                show_hidden_chars(sys.argv[2])

        case _:
            print("Unknown command. Use 'clean' or 'show'")
            return 1
    
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
