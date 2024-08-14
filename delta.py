import email
import re

def process_eml_files(file1, file2, identifier):
    def extract_values(filename, target_id):
        with open(filename, 'r') as file:
            eml_content = file.read()
        
        msg = email.message_from_string(eml_content)
        body = msg.get_payload()

        # Find the table in the body
        table_match = re.search(r'\|.*\|.*\|.*\|', body, re.DOTALL)
        if table_match:
            table = table_match.group(0)
            rows = table.split('\n')
            headers = [header.strip() for header in rows[0].split('|') if header.strip()]
            
            for row in rows[2:]:  # Skip header and separator rows
                cells = [cell.strip() for cell in row.split('|') if cell.strip()]
                if cells:
                    row_dict = dict(zip(headers, cells))
                    if row_dict.get('**ID**') == target_id:
                        return {
                            'Traced this month': int(row_dict.get('**Traced this month**', 0)),
                            'Logs traced this month': int(row_dict.get('**Logs traced this month**', 0))
                        }
        
        return None

    # Extract values from both files
    values1 = extract_values(file1, identifier)
    values2 = extract_values(file2, identifier)

    if values1 is None or values2 is None:
        print(f"Error: Identifier {identifier} not found in one or both files.")
        return

    # Print results for each file
    print(f"File: {file1}")
    for column, value in values1.items():
        print(f"Column: {column}, Value: {value}")

    print(f"\nFile: {file2}")
    for column, value in values2.items():
        print(f"Column: {column}, Value: {value}")

    # Calculate and print delta
    print(f"\nDelta (File2 - File1) for identifier {identifier}:")
    for column in values1.keys():
        delta = values2[column] - values1[column]
        print(f"Column: {column}, Delta: {delta}")

# Example usage:
# process_eml_files('file1.eml', 'file2.eml', 'ABC123')