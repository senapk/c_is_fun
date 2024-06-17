import re

def process_line(line):
    # Regex para encontrar '- [ ] <tag>'
    pattern = r'- \[ \] <!--.*?-->'
    # Substituir a correspondência encontrada por '- [ ]'
    return re.sub(pattern, '- [ ] ', line)

def process_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    with open(output_file, 'w', encoding='utf-8') as file:
        for line in lines:
            processed_line = process_line(line)
            file.write(processed_line)

if __name__ == "__main__":
    input_file = 'cplan.md'  # Nome do arquivo de entrada
    output_file = 'cplan.md'  # Nome do arquivo de saída
    process_file(input_file, output_file)
