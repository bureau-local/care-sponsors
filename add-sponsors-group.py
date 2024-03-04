import csv

# Open the sponsors file
with open("data-out/all-skilled-home-care-sponsors.csv") as infile:
	reader = csv.DictReader(infile)
	header = reader.fieldnames
	sponsors_data = [row for row in reader]

# Apply Council and NHS labels to sponsors
for org in sponsors_data:
	org_name = org["Organisation Name"].lower()

	# Local authority check - exceptions are false positives
	council_flags = ("council", "london borough", "royal borough")
	exceptions = ("arts council", "british council", "church council", "midwifery council", "national council", "reporting council", "research council", "school council", "services council", "toursim council", "town council")
	# Check if any flag and not any exceptions are in the name
	flag_test = [True for flag in council_flags if flag in org_name]
	exceptions_test = [True for val in exceptions if val in org_name]
	if any(flag_test) and not any(exceptions_test): 
		org["Local authority"] = True
	else:
		org["Local authority"] = False

	if "nhs" in org_name:
		org["NHS"] = True
	else:
		org["NHS"] = False

# Write the sponsors data with the new labels
if "Local authority" not in header:
	header.extend(["Local authority", "NHS"])
with open("data-out/all-skilled-home-care-sponsors.csv", "w") as outfile:
	writer = csv.DictWriter(outfile, fieldnames=header)
	writer.writeheader()
	writer.writerows(sponsors_data)

print("[*] Task completed!")

