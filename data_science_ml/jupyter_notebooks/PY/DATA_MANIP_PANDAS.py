#PANDAS TO MANIPULATE DATA
import pandas as pd

#LOAD DATAFRAME
df= pd.read_csv('/Volumes/F4L SWBB/iPSC_MEASUREMENT_DATA_1027.csv')

# SORTING DATA
df.sort_values("column_name",ascending=False)

# MORE THAN ONE AT A TIME
df.sort_values(["column_name1","column_name2"], ascending=[True,False])

#REPRESENT A SINGLE COLUMN
df["column_name"]

#CREATING A SUBSET FROM THE DATA FRAME FROM A LIST OF n COLUMN NAMES
#When we need to select more than one column and/or make the output to be a DataFrame, we should use double brackets:
df[["column_name","column_name"]]

# SUBSETTING ROWS WITH CONDITIONALS // CAN BE NUMERIC OR TEXT
df["column_name"] > 50
df[df["column_name"] == 50]

# FOR MULTIPLE CONDITIONS:
is_value1 = df["column_name"] == "value1"
is_value2 = df["column_name"] == "value2"
df[is_value1 & is_value2]

# Filter for rows where family_members is less than 1000
# and region is Pacific
condition1 = homelessness["family_members"] < 1000
condition2 = homelessness["region"] == "Pacific"
fam_lt_1k_pac = homelessness[condition1 & condition2]

# See the result
print(fam_lt_1k_pac)

# FOR MULTIPLE VARIABLES WITHIN A CATEGORY
is_value1_or_value2 = df["column_name"].isin(["value1","value2"])
df[is_value1_or_value2]

########

# SORT HOMELESSNESS BY INDIVIDUALS
homelessness_ind = homelessness.sort_values("individuals")

# HEAD() FXN PRINTS FIRST FEW ROWS.
print(homelessness_ind.head())

# Sort homelessness by descending family members
homelessness_fam = homelessness.sort_values(["family_members"], ascending=False)

# Print the top few rows
print(homelessness_fam.head())

# Sort homelessness by region, then descending family members
homelessness_reg_fam = homelessness.sort_values(["region","family_members"], ascending=[True,False])

# Print the top few rows
print(homelessness_reg_fam.head

###############################

# Filter for rows where individuals is greater than 10000
ind_gt_10k = homelessness[homelessness["individuals"] > 10000]

# See the result
print(ind_gt_10k)

#################

# Subset for rows in South Atlantic or Mid-Atlantic regions
south_mid_atlantic = homelessness[(homelessness["region"] == "South Atlantic") | (homelessness["region"] == "Mid-Atlantic")]

# See the result
print(south_mid_atlantic)

################

#MULTIPLE MANIPULAITONS
condition1 = 100
conditioned_subset_of_dataframe = df[df["column_name"] < condition1 ]
conditioned_subset_of_dataframe_descending = conditioned_subset_of_dataframe.sort_values("height_cm", ascending = True)
#JUST THE RELEVANT COLUMNS INTO A DATAFRAME
conditioned_subset_of_dataframe_descending[["name", "height_cm", "bmi"]]

###IN THIS CASE FOR EXAMPLE - THE [] DENOTE A COLUMN OR DIMENSION WITHIN THE HOMELESSNESS DF
### SIMILARLY, [p_individuals] iIS A COLUMN CREATED PER THE [] AND FROM THE ALGEBRAIC SUM

# Add total col as sum of individuals and family_members
homelessness["total"] = homelessness["individuals"] + homelessness["family_members"]

# Add p_individuals col as proportion of total that are individuals
homelessness["p_individuals"] = homelessness["individuals"]/homelessness["total"]

# See the result
print(homelessness)

########################

# Create indiv_per_10k col as homeless individuals per 10k state pop
homelessness["indiv_per_10k"] = 10000 * homelessness["individuals"] / homelessness["state_pop"]

# Subset rows for indiv_per_10k greater than 20
high_homelessness = homelessness[homelessness["indiv_per_10k"] > 20]

# Sort high_homelessness by descending indiv_per_10k
high_homelessness_srt = high_homelessness.sort_values("indiv_per_10k", ascending=False)

# From high_homelessness_srt, select the state and indiv_per_10k cols
result = high_homelessness_srt[["state", "indiv_per_10k"]]

# See the result
print(result)
