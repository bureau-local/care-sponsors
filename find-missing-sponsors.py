import csv
from datetime import datetime, timedelta
import os

# Check if a sponsor is a local authority or and nhs trust
# @params sponsor: dict
def is_not_council_or_nhs(sponsor):
	if sponsor["Local authority"] == "False" and sponsor["NHS"] == "False":
		return True
	else:
		return False

# All and current list of care sponsors
all_sponsors = "data-out/all-skilled-home-care-sponsors.csv"
current_sponsors = "data-out/current-skilled-home-care-sponsors.csv"

# Open the current sponsors csv
with open(current_sponsors) as infile:
	reader = csv.DictReader(infile)
	header = reader.fieldnames
	current_data = [row for row in reader]

# Get name of homecare agencies in the current data
current_orgs = {sponsor["Organisation Name"] for sponsor in current_data}

# Open the original sponsors csv
with open(all_sponsors) as infile:
	reader = csv.DictReader(infile)
	header = reader.fieldnames
	original_data = [row for row in reader]

# Get the missing sponsors
missing_sponsors = [org for org in original_data if org["Organisation Name"] not in current_orgs]
# Remove Local authority and NHS trusts
missing_sponsors = [org for org in missing_sponsors if is_not_council_or_nhs(org)]

# Get an estimate of how long the sponsor was on the register
# Start by getting the dates of each register
sponsors_registers = [file for file in os.listdir("sponsors-lists/csv") if file.endswith(".csv")]
sponsors_dates = [filename[:10] for filename in sponsors_registers]
sponsors_dates.sort()
# Then loop through sponsors
for sponsor in missing_sponsors:
	first_appeared = sponsor["First appeared"]
	last_appeared = sponsor["Last appeared"]
	# If it's the first file we can't calculate the estimate
	if first_appeared != "2020-07-27":
		# For the max lenght we need the dates before and after
		earliest_possible = sponsors_dates[sponsors_dates.index(first_appeared) - 1]
		latest_possible = sponsors_dates[sponsors_dates.index(last_appeared) + 1]
		# Calculate the delta between the two dates
		earliest_possible = datetime.strptime(earliest_possible, "%Y-%m-%d") + timedelta(days=1)
		latest_possible = datetime.strptime(latest_possible, "%Y-%m-%d") - timedelta(days=1)
		max_estimate = (latest_possible - earliest_possible).days
		# Now we'll get a confidence intervale
		start_delta = (datetime.strptime(first_appeared, "%Y-%m-%d") - earliest_possible).days
		end_delta = (latest_possible - datetime.strptime(last_appeared, "%Y-%m-%d")).days
		# total_confidence_delta = (start_delta + end_delta).days
		# Basically up to 35 days on each side
		if all([start_delta < 35, end_delta < 35]):
			confidence = "Good"
		elif all([start_delta < 70, end_delta < 70]):
			confidence = "Medium"
		else:
			confidence = "Bad"
		# print(start_delta, end_delta, confidence)
	else:
		max_estimate = "-"
		confidence = "-"
	# Assign the values to the sponsor
	sponsor["Estimated days on register (max)"] = max_estimate
	sponsor["Estimate confidence"] = confidence
	# Remove fields we don't care about from the output
	del sponsor["Route"]
	del sponsor["Local authority"]
	del sponsor["NHS"]
	

# Write the missing sponsors to file
header.extend(["Estimated days on register (max)", "Estimate confidence"])
header.remove("Route")
header.remove("Local authority")
header.remove("NHS")
with open("data-out/missing-sponsors.csv", "w") as outfile:
	writer = csv.DictWriter(outfile, fieldnames=header)
	writer.writeheader()
	writer.writerows(missing_sponsors)

print("[*] Task completed!")
