import csv
import os

# Group sponsors from multiple lists
# Include the date it first and last appears on the sponsors lists

# Check if org sponsors skilled worker
# @params org_data: dict
def is_skilled_worker_sponsor(org_data):
	visa_route = org_data["Route"].lower()
	if "skilled" in visa_route or "tier 2 general" in visa_route:
		return True

# Get all sponsors files
sponsors_files = [file for file in os.listdir("sponsors-lists/csv") if file.endswith(".csv")]
# Sort the file in reverse order alpha/chrono-logically
# That way the type/route info will be from the most recent file
sponsors_files.sort(reverse=True)

# Create a blank dict to group all sponsors
all_sponsors = dict()

# Loop through files
for i, filename in enumerate(sponsors_files):
	# Get the file date from the filename
	file_date = filename[:10]
	# Open the file
	filepath = "sponsors-lists/csv/" + filename
	with open(filepath) as infile:
		reader = csv.DictReader(infile)
		header = reader.fieldnames
		# Keep only skilled sponsor
		skilled_sponsor = [row for row in reader if is_skilled_worker_sponsor(row)]
	# Loop through the skilled sponsors in the file
	for sponsor in skilled_sponsor:
		organisation_name = sponsor["Organisation Name"]
		# If the sponsor is not yet in the dict
		# - Add the file date as the first/last appeared date
		# - And add the sponsor to the dict
		if organisation_name not in all_sponsors:
			sponsor["First appeared"] = file_date
			sponsor["Last appeared"] = file_date
			all_sponsors[organisation_name] = sponsor
		# If the sponsor is already in the dict
		# - Update the first appeared date
		elif organisation_name in all_sponsors:
			all_sponsors[organisation_name]["First appeared"] = file_date
	# Print a process update
	print("[*] Processed sponsors from {}/{} files".format((i + 1), len(sponsors_files)))

# Remove the dict keys/Convert the dict to list of dict
all_sponsors = [val for key, val in all_sponsors.items()]
# Add new datafield names to the header
header.extend(["First appeared", "Last appeared"])
# Write list of all-sponsors to file
with open("data-out/all-skilled-sponsors.csv", "w") as outfile:
	writer = csv.DictWriter(outfile, fieldnames=header)
	writer.writeheader()
	writer.writerows(all_sponsors)

print("[*] Task completed!")
