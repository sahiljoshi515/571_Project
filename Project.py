def bwt_transform(text):
    """
    Computes the Burrows-Wheeler Transform (BWT) of a given text.

    The BWT is a reversible transformation of a string that rearranges the symbols
    in a way that creates runs of similar characters, which can be useful for
    compression and other applications.

    :param text: The input string to transform.
    :return: The Burrows-Wheeler Transform of the input string.
    """
    text = text.replace(" ", "")  # Remove spaces before processing
    text = text + "$"  # Append unique end-of-string marker
    rotations = [text[i:] + text[:i] for i in range(len(text))]  # Generate all cyclic rotations
    rotations.sort()  # Lexicographically sort the rotations
    bwt_result = "".join(row[-1] for row in rotations)  # Extract the last column
    return bwt_result

def bwt_inverse(bwt):
    """
    Computes the inverse Burrows-Wheeler Transform (BWT) in O(n) using LF Mapping.

    :param bwt: The Burrows-Wheeler Transform of a string to invert.
    :return: The original string.
    """
    n = len(bwt)
    
    # Create the sorted first column (F)
    first_col = sorted(bwt)
    
    # Compute LF Mapping: map last column indices to first column indices
    # The LF mapping is a bijection between the last column and the first column
    # of the matrix of rotations of the input string. It is used to reconstruct
    # the original string from the Burrows-Wheeler Transform.
    lf_map = []
    count_last, count_first = {}, {}

    for i, char in enumerate(bwt):
        count_last[char] = count_last.get(char, 0) + 1
        count_first[char] = 0  # Initialize count for first column
        lf_map.append((char, count_last[char]))

    # Assign ranks to first column
    # The rank of a character in the first column is the number of occurrences
    # of the character in the first column.
    first_rank = {}
    for i, char in enumerate(first_col):
        count_first[char] += 1
        first_rank[(char, count_first[char])] = i

    # Reconstruct original string using LF mapping
    row = first_rank[('$', 1)]  # Locate the end marker '$'
    original = []
    
    for _ in range(n - 1):  # Stop before '$'
        char, rank = lf_map[row]
        original.append(char)
        row = first_rank[(char, rank)]

    return "".join(original[::-1])  # Reverse to get the original order

def run_length_encode(text):
    """
    Applies Run-Length Encoding (RLE) to compress the text.

    RLE is a simple form of data compression where consecutive identical 
    elements (runs) are stored as a single data value and count. This 
    function compresses a given string by replacing sequences of repeated 
    characters with the character followed by the number of repetitions.

    :param text: The input string to encode.
    :return: The RLE encoded string.
    """
    if not text:
        return ""  # Return an empty string if input is empty

    encoded = []  # List to store the encoded characters
    count = 1  # Initialize count of consecutive characters

    for i in range(1, len(text)):
        if text[i] == text[i - 1]:
            count += 1  # Increment count if current character equals the previous
        else:
            # Append the character and its count if greater than 1
            encoded.append(f"{text[i - 1]}{count}" if count > 1 else text[i - 1])
            count = 1  # Reset count for the next character

    # Append the last character and its count
    encoded.append(f"{text[-1]}{count}" if count > 1 else text[-1])

    return "".join(encoded)  # Join the list into a single string to return


def run_length_decode(encoded):
    """
    Applies Run-Length Decoding (RLE) to decompress the encoded text.

    Run-Length Decoding is the inverse process of Run-Length Encoding. It takes
    a string that has been compressed using RLE and decompresses it back to its
    original form.

    :param encoded: The encoded string to decode.
    :return: The decoded string.
    """
    if not encoded:
        return ""
    
    decoded = []
    i = 0
    
    while i < len(encoded):
        char = encoded[i]  # Current character
        
        # Check if the next characters are digits (count)
        count_str = ""
        while i + 1 < len(encoded) and encoded[i + 1].isdigit():
            count_str += encoded[i + 1]
            i += 1
        
        # Determine the count
        count = int(count_str) if count_str else 1
        
        # Append the character 'count' times
        decoded.append(char * count)
        
        i += 1  # Move to the next character
    
    return "".join(decoded)

def retrieve_row(index, compressed_sequences):
    """
    Retrieve and decompress a specific sequence (row).

    :param index: The index of the sequence to retrieve.
    :param compressed_sequences: The list of compressed BWT sequences.
    :return: The decompressed sequence.
    """
    if index < 0 or index >= len(compressed_sequences):
        raise ValueError("Row index out of range")
    
    compressed_seq = compressed_sequences[index]
    return bwt_inverse(run_length_decode(compressed_seq))


def retrieve_column(position, compressed_sequences):
    """
    Retrieve a specific column (character position across all sequences) using BWT+RLE without full decompression.

    This function takes advantage of the Burrows-Wheeler Transform (BWT) and Run-Length Encoding (RLE) to efficiently
    retrieve a specific column from a list of compressed sequences. It does not require full decompression of the BWT or RLE.

    :param position: The column index to retrieve (0-based).
    :param compressed_sequences: The list of compressed BWT sequences.
    :return: The retrieved column as a string.
    """
    if position < 0:
        raise ValueError("Column position must be non-negative")

    column_chars = []

    for compressed_bwt in compressed_sequences:
        # Step 1: Decode only needed part of BWT (Lazy RLE Expansion)
        bwt = run_length_decode(compressed_bwt)

        if position >= len(bwt):  # Handle shorter sequences
            column_chars.append("-")
            continue

        # Step 2: LF Mapping to reconstruct original character at given column position
        n = len(bwt)
        sorted_bwt = sorted(bwt)

        # Compute C table
        C = {}
        for i, char in enumerate(sorted_bwt):
            if char not in C:
                C[char] = i

        # Compute LF Mapping
        count_last, count_first = {}, {}
        lf_map = []
        for i, char in enumerate(bwt):
            count_last[char] = count_last.get(char, 0) + 1
            count_first[char] = 0  # Initialize first column count
            lf_map.append((char, count_last[char]))

        first_rank = {}
        for i, char in enumerate(sorted_bwt):
            count_first[char] += 1
            first_rank[(char, count_first[char])] = i

        # Start from '$' and follow LF mapping to the required position
        row = first_rank[('$', 1)]  # Locate '$'
        original_char = None

        for _ in range(position):  # Navigate to the required column index
            char, rank = lf_map[row]
            row = first_rank[(char, rank)]

        original_char, _ = lf_map[row]
        column_chars.append(original_char)

    return "".join(column_chars)


# Read input sequence from file
with open("subs_data_2.txt", "r") as file:
    sequences = [line.strip() for line in file if line.strip()]

if not sequences:
    raise ValueError("No valid sequences found in the file")

# Apply BWT and then RLE to each sequence (ignoring spaces)
compressed_sequences = [run_length_encode(bwt_transform(seq)) for seq in sequences]

# Example Usage
column_position = 1  # Retrieve 2nd character from all sequences
retrieved_column = retrieve_row(column_position, compressed_sequences)
print(f"Retrieved Column {column_position}: {retrieved_column}")

# Write the compressed output to compressed.txt
with open("compressed.txt", "w") as file:
    file.writelines(f"{compressed}\n" for compressed in compressed_sequences)

print("BWT + RLE compression completed (ignoring spaces). Check compressed.txt")

decompressed_sequences = [bwt_inverse(run_length_decode(seq)) for seq in compressed_sequences]

# Write the compressed output to decompressed.txt
with open("decompressed.txt", "w") as file:
    file.writelines(f"{decompressed}\n" for decompressed in decompressed_sequences)

print("RLE + BWT decompression completed (ignoring spaces). Check decompressed.txt")
