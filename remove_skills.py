import re

def remove_annotations_from_titles(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as infile:
        lines = infile.readlines()

    with open(output_file, 'w', encoding='utf-8') as outfile:
        for line in lines:
            # Use regex to remove backticks and annotations within them
            clean_line = re.sub(r'`[^`]*`', '', line)
            outfile.write(clean_line)

# Example usage:
input_file = 'cplan.md'  # Replace with your input file name
output_file = 'cplan.md'  # Replace with your desired output file name
remove_annotations_from_titles(input_file, output_file)