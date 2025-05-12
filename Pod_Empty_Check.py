#J. Tia - joshtial 3-24-25

import openpyxl ## don't actually need this - using pandas
import pandas as pd ##initializing pandas library.

## I'm a MechE I don't know anything about Algorithms

vantageFile = pd.read_csv('vantage.csv')
stowMapFile = pd.read_csv('stowmap.csv')

v_df = pd.DataFrame(data=vantageFile) #creating data frame of vantage data using not transpose of vantage csv.
s_df = pd.DataFrame(data=stowMapFile) #creating data frame of stowmap data using not transpose of stowMap csv.

### Create a list of vantage pods. Or should it be a Vector? I don't know
vantPods = []
stowPods = []

## Filtering out Vantage data.
#Filter pod Family for H8, H10, H11
v_filt =  v_df[ (v_df['Pod Family'] != "H12") # Filter out Pod Family: H12
                 & (v_df['Pod Empty'] != "No") # Filter out Pod Empty: No
                 #POD_RESERVED_FOR_REMOVAL and STOW_PROHIBITED are applied after Pod Empty Workflow is completed
                 & ((v_df['Reasons'] == "POD_RESERVED_FOR_REMOVAL, STOW_PROHIBITED") | #
                 #POD_BLOCKED_FOR_TRAVEL is a temporary restriction when pods are being carried, are in an oos/managed area, etc.
                  (v_df['Reasons'] == "POD_RESERVED_FOR_REMOVAL, POD_BLOCKED_FOR_TRAVEL, STOW_PROHIBITED"))   
                 ] 
                 
#print(v_filt[v_filt['Reasons'] == "POD_RESERVED_FOR_REMOVAL, POD_BLOCKED_FOR_TRAVEL, STOW_PROHIBITED"])

## Filtering out StowMap Data
s_filt = s_df[ (s_df['Total Units'] == 0)  # Filter for 0 Total units, meaning empty pod.
                & ((s_df['Total Bins'] == 101) #Filter for 101 or 122 or 128 bins, indicating cloth pods.
                | (s_df['Total Bins'] == 122)
                | (s_df['Total Bins'] == 128)                              
                )
                ]

# Filter for Number of Units
#print(s_filt)
empty_vantage_ids = v_filt["Pod_ID"] # defines empty_vantage_ids as a series derived from "Pod_ID" column of v_filt
s_filt = s_filt.rename(columns={"Bay": "Pod_ID"}) #modifies stowmap data frame to use "Pod_ID"
empty_stowmap_ids = s_filt['Pod_ID'] # defines empy_stowmap_ids as a series derived from "Pod_ID" column of s_filt

#iterates through the 
empty_count = 0
empty_pods = []

for index, id_i in empty_vantage_ids.items(): #uses a for loop to iterate over Pod_ID's of both series.
    for jindex, id_j in empty_stowmap_ids.items(): #there's probably a faster way to do this using pandas, but I am bad.
        if id_i == id_j: # if a matching Pod ID is found, then:
            #append the pod_id to the pod ID list.            
            #print(id_i, "is same as ", id_j)
            empty_count += 1
            empty_pods.append(id_j)
            continue

            #continue #end this cycle and move on to the next ID.
                    
#you could probably save memory by taking the series of vantage_ids, since the list is usually bigger,
#and popping or deleting the pod_ids that have no duplicates. However, I am lazy.

empty_df = pd.DataFrame(empty_pods) #converting list to df because I don't know how to append a df otherwise.
empty_df = empty_df.rename(columns={ 0 : "Pod_ID"})

empty_count_series = pd.Series([empty_count]) #convert empty count into series so I can stick it into csv.
#for some reason, you can't insert a singular value into a column using data pandas library.
empty_df['Number of Empty Pods'] = empty_count_series

print("There are ", empty_count, " duplicates.")
print(empty_df.head())

empty_df.to_csv("Empty_Pods_List")
empty_df.to_excel("Empty_Pods_List.xlsx")


