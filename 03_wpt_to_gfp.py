import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file, 'r') as f:
    # Read lines from the input file
    lines = f.readlines()

converted_lines = []
for line in lines:
    parts = line.strip().split(',')
    # Remove dots, 'd', and 'm' characters from the coordinates and concatenate latitude and longitude
    coordinates = parts[2].replace('.', '').replace('d', '').replace('m', '') + parts[3].replace('.', '').replace('d', '').replace('m', '')
    # Append the formatted coordinates to the converted lines
    converted_lines.append(f'{coordinates}')

# Concatenate the converted lines with the :F: delimiter
output_content = 'FPN/RI:F:' + ':F:'.join(converted_lines)

with open(output_file, 'w') as f:
    f.write(output_content)
