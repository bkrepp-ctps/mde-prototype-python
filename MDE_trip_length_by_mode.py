#!/usr/bin/env python
# coding: utf-8
#
# MDE_trip_length_by_mode.py - Derived from Model Data Explorer prototype #1.
#
#	Calculate trip length distribution by mode
#
# Author: Ben Krepp

import openmatrix as omx
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import geopandas


# Work with the trip tables OMX file

trip_tables_file = r'C:/Users/ben_k/work_stuff/tdm/datastore/sample_data/AfterSC_Final_AM_Tables.omx'
trip_tables_omx = omx.open_file(trip_tables_file, 'r')
trip_tables_omx.list_matrices()
# Returns: ['Bike', 'DAT_Boat', 'DAT_CR', 'DAT_LB', 'DAT_RT', 'DET_Boat', 'DET_CR', 'DET_LB', 'DET_RT', 
#			'HOV', 'HOV2p', 'HOV3p', 'HOV_Person_Trips', 'Heavy_Truck', 'Heavy_Truck_HazMat', 'Light_Truck', 
#			'Medium_Truck', 'Medium_Truck_HazMat', 'SOV', 'WAT', 'Walk']
trip_tables_omx.shape()
# Returns: (5839, 5839)

# Very crude way to get the # of SOV trips from TAZ[1] to TAZ[1]
trip_tables_omx['SOV'][0][0]

# A more elegant way to do the same thing, using TAZ IDs rather than OMX table indices
trip_tables_omx.list_mappings()
# Returns: ['CTPS', 'ID', 'MAPC', 'extZ', 'intZ']
taz_to_omxid = trip_tables_omx.mapping('ID')
trip_tables_omx['SOV'][taz_to_omxid[1]][taz_to_omxid[1]]

#####

# Work with the skims OMX file

skim_file = r'C:/Users/ben_k/work_stuff/tdm/datastore/sample_data/AM_SOV_Skim.omx'
skim_omx = omx.open_file(skim_file, 'r')
skim_omx.list_matrices()
# Returns: ['Auto_Toll (Skim)', 'CongTime', 'CongTime_wTerminalTimes', 'Drive_Cost', 
#			'LT_Toll (Skim)', 'Length (Skim)', 'TerminalTimes', 'Total_Cost']
skim_omx.shape()
# Returns: (5839, 5839)
skim_omx.list_mappings()
# Returns: ['Destination', 'Origin', 'extZ', 'inCTPS', 'intZ']


# Do some real work!
# Now, let's do what Marty _really_ asked us to do:
# For each mode, make a plot of trip-length distribution
#
# t_lengths: TAZ-to-TAZ distance, no?
t_lengths = skim_omx['Length (Skim)']
t_lengths_np = np.array(t_lengths)
t_lengths_flat = t_lengths_np.flatten(order='C')
# len(t_lengths_flat)

# Let's find out a	bit about TAZ-to-TAZ distances
np.min(t_lengths_flat)
np.max(t_lengths_flat)
np.mean(t_lengths_flat)
np.std(t_lengths_flat)

# Brute-force display of distribution of TAZ-to-TAZ trip-lengths
# plt.hist(t_lengths, bins=6)

# (1) Trip length distribution for SOV mode
# 
# Number of SOV trips TAZ-to-TAZ
tt_sov = trip_tables_omx['SOV']
tt_sov_np =	 np.array(tt_sov)
tt_sov_flat = tt_sov_np.flatten(order='C')
# len(tt_sov_flat)

# 'bins' for trip length classification
bins =		 [ 1.0,		 5.0,	   10.0,	   20.0,	   50.0,	  100.0,	   10000.0 ]
bin_labels = [ '< 1 mi', '1-5 mi', '5-10 mi', '10-20 mi', '20-50 mi', '50-100 mi', '> 100 mi' ]

classification = np.digitize(t_lengths_flat, bins, right=False)

results = [ 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 ]

for (num_trips, trip_len, bucket_ix) in zip(tt_sov_flat, t_lengths_flat, classification):
	results[bucket_ix] += num_trips
# end_for

fig, ax = plt.subplots()
ax.bar(bin_labels, results)
plt.title('SOV Trip Length Distribution')
plt.xlabel('Trip Length')
plt.ylabel('Number of Trips')

# Genericized routine to generate trip-length distribution by mode
# 
def get_tld_for_mode(trip_lengths_skim, tt_omx, mode_name, bins):
	# Initialize return value
	results = [0.0 for x in bins]
	
	# Flatten trip_lengths array
	t_lengths_np = np.array(trip_lengths_skim)
	t_lengths_flat = t_lengths_np.flatten(order='C')
	
	# Number of trips TAZ-to-TAZ using specified mode
	tt = tt_omx[mode_name]
	tt_np =	 np.array(tt)
	tt_flat = tt_np.flatten(order='C')
	
	# Classify trip lengths into bins
	classification = np.digitize(t_lengths_flat, bins, right=False)
	
	for (num_trips, bucket_ix) in zip(tt_flat, classification):
		results[bucket_ix] += num_trips
	# end_for

	return results
# get_tld_for_mode()

# Routline to plot  trip length distribution as bar graph
#
def plot_tld_for_mode(tld_array, bin_labels, plot_title):
	names = bin_labels
	values = tld_array
	plt.title(plot_title)
	plt.xlabel('Trip Length')
	plt.ylabel('Number of Trips')
	plt.bar(names, values)
# plot_tld_for_mode()

# Trip-length distribution for SOV mode
sov_tld = get_tld_for_mode(skim_omx['Length (Skim)'], trip_tables_omx, 'SOV', bins)
plot_tld_for_mode(sov_tld, bin_labels, 'SOV Trip Length Distribution')

# Trip-length distribution for HOV mode
hov_tld = get_tld_for_mode(skim_omx['Length (Skim)'], trip_tables_omx, 'HOV', bins)
plot_tld_for_mode(hov_tld, bin_labels, 'HOV Trip Length Distribution')

# Trip-length distribution for Bike mode
bike_tld = get_tld_for_mode(skim_omx['Length (Skim)'], trip_tables_omx, 'Bike', bins)
plot_tld_for_mode(bike_tld, bin_labels, 'Bike Trip Length Distribution')

# Trip-length distribution for Walk mode
walk_tld = get_tld_for_mode(skim_omx['Length (Skim)'], trip_tables_omx, 'Walk', bins)
plot_tld_for_mode(walk_tld, bin_labels, 'Walk Trip Length Distribution')
