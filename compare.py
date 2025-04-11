import os

# Get the file sizes
genomic_file_size = os.path.getsize("subs_data_2.txt")
encoded_file_size = os.path.getsize("compressed.txt")

# Print the file sizes
print(f"Size of 'subs_data_2.txt': {genomic_file_size} bytes")
print(f"Size of 'compressed.txt': {encoded_file_size} bytes")

# Calculate the difference
size_difference = genomic_file_size - encoded_file_size
compression_ratio = (encoded_file_size / genomic_file_size) * 100

# Print the difference and compression ratio
print(f"Size difference: {size_difference} bytes")
print(f"Compression ratio: {compression_ratio:.2f}%")