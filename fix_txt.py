def normalise_rules_file(input_filename, output_filename):
    # Step 1: Read and parse the file
    with open(input_filename, 'r', encoding='iso-8859-1') as file:
        lines = file.readlines()

    rules = {}
    for line in lines:
        parts = line.strip().split(';')
        rule_id = int(parts[0])
        rule = parts[1].strip()
        score = int(parts[2].strip())
        
        if rule in rules:
            # Update the existing rule with the smallest ID and sum the scores
            existing_id, existing_score = rules[rule]
            new_id = min(existing_id, rule_id)
            new_score = existing_score + score
            rules[rule] = (new_id, new_score)
        else:
            rules[rule] = (rule_id, score)
    
    # Step 2: Sort rules by ID and prepare output
    sorted_rules = sorted(rules.items(), key=lambda item: item[1][0])
    
    # Step 3: Write the normalized rules back to a file
    with open(output_filename, 'w', encoding='iso-8859-1') as file:
        for rule, (rule_id, score) in sorted_rules:
            file.write(f"{rule_id};{rule};{score}\n")

# Example usage:
input_filename = 'temp_rule.txt'
output_filename = 'normalized_rules.txt'
normalise_rules_file(input_filename, output_filename)
