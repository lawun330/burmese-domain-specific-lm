import argparse
import re
import string

# innermost (...) with no nested parens
_INNERMOST_PAREN = re.compile(r"\([^()]*\)")
# POS / tree label at start of parenthesis content (e.g. NOUN, verb, noun-adp)
_TAG_PREFIX = re.compile(r"^([A-Za-z][-A-Za-z0-9]*)\s+(.*)$", re.DOTALL)
_TAG_ONLY = re.compile(r"^([A-Za-z][-A-Za-z0-9]*)$")


def strip_word_tags_ALT(line: str) -> str:
    """unwrap (TAG token ...) groups; leave normal english words untouched."""
    while True:
        match = _INNERMOST_PAREN.search(line)
        if not match:
            break
        inner = match.group(0)[1:-1].strip()
        tag_body = _TAG_PREFIX.match(inner)
        if tag_body:
            replacement = tag_body.group(2).strip()
        elif _TAG_ONLY.match(inner):
            replacement = ""
        else:
            replacement = inner
        line = line[: match.start()] + replacement + line[match.end() :]
    return line


def remove_punctuation(input_path, output_path):
    # Define English punctuation from the string module
    english_punct = string.punctuation
    
    # Define Burmese specific punctuation
    burmese_punct = "၊။“”‘’"
    
    # Combine them into one set of characters to remove
    all_to_remove = english_punct + burmese_punct
    
    # Create a translation table for fast processing
    # This maps every character in 'all_to_remove' to None
    table = str.maketrans('', '', all_to_remove)

    try:
        with open(input_path, 'r', encoding='utf-8') as infile:
            with open(output_path, 'w', encoding='utf-8') as outfile:
                for line in infile:
                    # Strip word tags
                    clean_line = strip_word_tags_ALT(line)
                    # Apply the translation table to each line
                    clean_line = clean_line.translate(table)
                    outfile.write(clean_line)
        
        print(f"Success! Cleaned text saved to: {output_path}")
        
    except FileNotFoundError:
        print(f"Error: The file '{input_path}' was not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Remove English/Burmese punctuation and word tags from a text file."
    )
    
    # Setting up --input/-i and --output/-o
    parser.add_argument('-i', '--input', required=True, help="Path to the source text file.")
    parser.add_argument('-o', '--output', required=True, help="Path where the cleaned file will be saved.")

    args = parser.parse_args()

    remove_punctuation(args.input, args.output)
