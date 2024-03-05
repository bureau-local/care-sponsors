import csv
from datetime import datetime

# Convert strings to datetime objects
# @params date_str: strings
def convert_to_date(date_str):
    date_formats = ["%Y-%m-%d", "%Y-%m-%d %H:%M", "%a, %d %b %Y"]
    for fmt in date_formats:
        try:
            return datetime.strptime(date_str, fmt)
        except ValueError:
            pass
    raise ValueError("[!] Error, no valid date format found")

# Open the decisions data
print("[*] Opening the decisons data")
with open("data-in/decisions-data.csv") as infile:
	reader = csv.DictReader(infile)
	decisions_header = reader.fieldnames
	decisions_data = [row for row in reader]
# Open the documents data
print("[*] Opening the documents data")
with open("data-in/documents-data.csv") as infile:
	reader = csv.DictReader(infile)
	documents_data = [row for row in reader]
# Get the doc ids for outcome types to remove
to_remove = ["Dismissal", "Strike out", "Withdrawal"]
cases_to_remove = {doc["Decision id"] for doc in documents_data if doc["Outcome"] in to_remove}
# Remove the relevant decisions
decisions_data = [case for case in decisions_data if case["Decision id"] not in cases_to_remove]

# Open the care sponsors data
print("[*] Opening the sponsors data")
with open("data-out/all-skilled-home-care-sponsors.csv") as infile:
	reader = csv.DictReader(infile)
	header = reader.fieldnames
	sponsors_data = [row for row in reader]
# Get the number of sponsors
sponsors_count = len(sponsors_data)
org_with_cases_found = 0

# Blank list to store cases data
all_sponsors_cases = list()
# Loop through care sponsors
print("[*] Checking sponsors against employement tribunal data")
for i, sponsor in enumerate(sponsors_data):
	org_name = sponsor["Organisation Name"]
	# Get the id of employement tribunal decisions involving this org
	org_tribunal_cases = [x for x in decisions_data if x["Defendant"] == org_name]
	org_tribunal_cases_ids = [x["Decision id"] for x in org_tribunal_cases]
	cases_str = " / ".join(org_tribunal_cases_ids)
	# Get the count and id of the tribunal decisions
	decisions_count = len(org_tribunal_cases)
	if decisions_count > 0:
		org_with_cases_found += 1
	# Add the new data to the sponsor data
	sponsor["Employement Tribunal decisions count"] = decisions_count
	sponsor["Employement Tribunal decisions ids"] = cases_str

	# Check if the decision was after the org appeared as a sponsor
	first_appear = datetime.strptime(sponsor["First appeared"], "%Y-%m-%d")
	for case in org_tribunal_cases:
		decision_date = datetime.strptime(case["Decision date"], "%Y-%m-%d")
		if first_appear < decision_date:
			case["Decision after sponsor first appeared date"] = True
		else:
			case["Decision after sponsor first appeared date"] = False
	
	# Add the org cases to the output list
	all_sponsors_cases.extend(org_tribunal_cases)

	# Print process update
	index = i + 1
	if index % 500 == 0:
		update_msg = "[*] Checked {}/{} sponsors against employement tribunal data"
		print(update_msg.format(index, sponsors_count))
	# Conditional break used when testing
	# if i > 99:
		# break

print("[*] We've found employement tribunal decisions for {} orgs".format(org_with_cases_found))
# Re-write the sponsors data with the new datafields added
new_datafields = ["Employement Tribunal decisions count", "Employement Tribunal decisions ids"]
if new_datafields[0] not in header:
	header.extend(new_datafields)
with open("data-out/all-skilled-home-care-sponsors.csv", "w") as outfile:
	writer = csv.DictWriter(outfile, fieldnames=header)
	writer.writeheader()
	writer.writerows(sponsors_data)

# Write the cases
decisions_header.append("Decision after sponsor first appeared date")
with open("data-out/sponsors-cases.csv", "w") as outfile:
	writer = csv.DictWriter(outfile, fieldnames=decisions_header)
	writer.writeheader()
	writer.writerows(all_sponsors_cases)

print("[*] Task completed!")

