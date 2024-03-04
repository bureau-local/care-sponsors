# Care Sponsors

This project builds from the existing work on the [employment tribunal scraper](https://github.com/bureau-local/employement-tribunal)

### The Data
The care sponsors data produced as part of this project can be found in [these googlesheets](https://docs.google.com/spreadsheets/d/1iPB56kDgxa9FGxA6Y_-g-AsE2tlOPGFyk4-O6SCF67Q/edit#gid=626523347)

### Prep
Download the sponsors lists from this [google drive folder](https://drive.google.com/drive/u/0/folders/189R89zfI2xOL-KNqN3Szor8ZUkWtmQl0), and place them in a folder named `sponsors-lists/csv` in the version of this project folder on your machine. 

### Run Order
To fully update the care sponsors data found in the data section above you to run the scripts in the following order

Starting with the employement tribunal scripts
1. `get-all-decisions.py`, to make sure we have data on all currently published employment tribunal decisions
2. `clean-defendants.py`, to clean defendant names, for instance when there's multiple defendants or to consolidate when various spellings are used for the same company name 
3. `evaluate-defendant-groups.py`, which evaluates if the defendant is a local authority, NHS body, care organisation etc...
4. `add-defendant-goups.py`, to apply the defendants groups to the decisions data
5. `json-to-csv.py`, Convert the json data to csv

You can then copy `decisions-data.csv` from the employment tribunal project to the `data-in` folder for this project. If it's been a while since the last sponsors list was added to the `sponsors-lists/csv` folder, download the latest version on the [register of licensed sponsors page](https://www.gov.uk/government/publications/register-of-licensed-sponsors-workers). You can then proceed with...

6. `prep-sponsors-data.py`, to get the "skilled sponsors" from the sponsors lists
7. `get-care-sponsors.py`, to get the domiciliary care sponsors, run twice, updating the `sponsor_status` variable at the top of the script for "all" and "current"
8. `add-sponsors-group.csv`, this evaluate if the domiciliary care sponsors is a local authority or NHS body
9. `check-employment-tribunal.py`, check for cases involving domiciliary care sponsors, the first time you run this you'll want to add a blank file named `documents-data.csv` to the `data-in` folder

Now that we know which tribunal employment cases involve domiciliary care sponsors, we'll go back to the employment tribunal project and go through the more cumbersome step of getting the documents relevant to these sponsors, it will for instance allow us to know if the case was dismissed, strike-out, withdrawn etc... 

So copy `all-skilled-home-care-sponsors.csv` to the `data-in` folder of the employmen tribunal project and continue with...
10. `get-reports-with-priority.py`, download the documents and get the data for the domiciliary care sponsors cases
11. `assign-outcome-to-document-data.py`, evaluate from the name of the document what the outcome of the case was
12. `json-to-csv.py`, convert the json data to csv

Now that we have both the decisions and documents data for the domiciliary care sponsors we can complete the final part of the process. You'll want to download the latest version of the `Sponsors employment tribunal cases` sheet found in the data above, name tha file `sponsors-cases-with-manual-input.csv` and place it in the `data-in` folder of this project.

13. `check-employment-tribunal.py`, run this again now that we can account for dismissed/withdrawn/striked-out cases
14. `find-missing-sponsors.py`, get the list of sponsors which are no longer on the register 
15. `add-user-input-data.py`, add the data that was added manually by the reporters to the sponsors cases data
16. `get-care-sponsors-count-by-date.py`, get the analysis of the number of care sponsors on the register at various point in time
