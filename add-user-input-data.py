import csv

# Open the user inputed data
with open("data-in/sponsors-cases-with-manual-input.csv") as infile:
	reader = csv.DictReader(infile)
	user_input_header = reader.fieldnames
	user_input_data = {row["Decision id"]: row for row in reader}

# Open the sponsors cases data
with open("data-out/sponsors-cases.csv") as infile:
	reader = csv.DictReader(infile)
	header = reader.fieldnames
	sponsors_cases = [row for row in reader]

# Loop through cases and add the user inputed data
for case in sponsors_cases:
	decision_id = case["Decision id"].strip()
	if decision_id in user_input_data:
		user_input_for_case = user_input_data[decision_id]
	else:
		user_input_for_case = dict()
	for datafield in user_input_header:
		if datafield not in case:
			if datafield in user_input_for_case:
				case[datafield] = user_input_for_case[datafield]
			else:
				case[datafield] = ""

# Add the new datafield to the header
for datafield in user_input_header:
	if datafield not in header:
		header.append(datafield)
# Re-write the data with user input
with open("data-out/sponsors-cases-with-manual-input.csv", "w") as outfile:
	writer = csv.DictWriter(outfile, fieldnames=header)
	writer.writeheader()
	writer.writerows(sponsors_cases)
