import csv
from datetime import datetime
import os

# Check if a sponsor was on the register on a specific date
# @params sponsor: dict
# @params date: datetime obj
def is_registered_at_the_time(sponsor, date):
	first_appeared = datetime.strptime(sponsor["First appeared"], "%Y-%m-%d")
	last_appeared = datetime.strptime(sponsor["Last appeared"], "%Y-%m-%d")
	if first_appeared <= date <= last_appeared:
		return True
	else:
		return False
	
# Check if a sponsor is a local authority or and nhs trust
# @params sponsor: dict
def is_not_council_or_nhs(sponsor):
	if sponsor["Local authority"] == "False" and sponsor["NHS"] == "False":
		return True
	else:
		return False

# Open the sponsors data
with open("data-out/all-skilled-home-care-sponsors.csv") as infile:
	reader = csv.DictReader(infile)
	header = reader.fieldnames
	care_sponsors = [row for row in reader]

# Get the dates sponsors register and list chronologicaly
sponsors_csv = [file for file in os.listdir("sponsors-lists/csv") if file.endswith(".csv")]
csv_dates = [file[:10] for file in sponsors_csv]
csv_dates.sort()
csv_datetime_dates = [datetime.strptime(x, "%Y-%m-%d") for x in csv_dates]

# Blank dict to store the output data
output_data = dict()

# Get the count of registered sponsors on each date
for date_str in csv_dates:
	# Convert the date to a datetime object
	date = datetime.strptime(date_str, "%Y-%m-%d")
	# Get the list of sponsors registered on that date
	registered_sponsors = [org for org in care_sponsors if is_registered_at_the_time(org, date)]
	# Remove local authority and nhs trusts
	registered_sponsors = [org for org in registered_sponsors if is_not_council_or_nhs(org)]
	# Get the count of regisreted sponsors
	registered_sponsors_count = len(registered_sponsors)
	
	# Look for a date a year earlier
	timedeltas = [(x - date).days for x in csv_datetime_dates]
	year_ago_test = [True if (-350 >= x >= -380) else False for x in timedeltas]
	if any(year_ago_test):
		year_ago_index = year_ago_test.index(True)
		year_ago = csv_dates[year_ago_index]
		year_ago_count = output_data[year_ago]["Registered care sponsors"]
		in_year_change = registered_sponsors_count - year_ago_count
		avg_monthly_change = in_year_change / 12
	else:
		year_ago = "-"
		in_year_change = "-" 
		avg_monthly_change = "-"
	
	# Format the output data and add tot he output list
	output_row = {
		"Year": date_str[:4],
		"Date": date_str,
		"Registered care sponsors": registered_sponsors_count,
		"Approximate in-year change": in_year_change,
		"Avg. in-year monthly change": avg_monthly_change,
		"Date used for yearly comparison": year_ago
	}
	output_data[date_str] = output_row

# Write the data to the output file
outhead = [
	"Year", "Date", "Registered care sponsors", "Approximate in-year change",
	"Avg. in-year monthly change", "Date used for yearly comparison"
]
output_data = [val for key, val in output_data.items()]
with open("data-out/registered-care-sponsors-count.csv", "w") as outfile:
	writer = csv.DictWriter(outfile, fieldnames=outhead)
	writer.writeheader()
	writer.writerows(output_data)

print("Task completed :))")
