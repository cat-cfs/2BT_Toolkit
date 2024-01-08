#!/usr/bin/env python3
#~-~ encoding: utf-8 ~-~
# geo_attachment_seeker/geo_attachment_seeker.py
#========================================================
# Created By:       Anthony Rodway
# Email:            anthony.rodway@nrcan-rncan.gc.ca
# Creation Date:    Fri January 05 08:30:00 PST 2024
# Organization:     Natural Resources of Canada
# Team:             Carbon Accounting Team
#========================================================
# File Header
#========================================================
"""
File: geo_attachment_seeker/geo_attachment_seeker.py
Created By:       Anthony Rodway
Email:            anthony.rodway@nrcan-rncan.gc.ca
Creation Date:    Fri January 05 08:30:00 PST 2024
Organization:     Natural Resources of Canada
Team:             Carbon Accounting Team

Description: 
    

Usage:
    python path/to/geo_attachment_seeker.py gdb_path output_path
"""


#========================================================
# Imports
#========================================================
import os
import sys
import time
import argparse
import arcpy 


#========================================================
# Functions
#========================================================
def find_attachments(gdb_path, output_path):
    '''
    Searches through the gdb and finds all relevant attachments.

    Parameters:
    - gdb_path (str): Path to input GDB.
    - output_path (str): Path to export the attachments to.
    
    Return:
    - attachment_dict (dict): A dictionary of key value pairs to tie each project id that had attachments to the path they were extracted to.
    ''' 
    # Set the arc environment
    arcpy.env.workspace = gdb_path
    
    # Work all attach tables
    attachment_dict = {}
    for table in arcpy.ListTables(): 
        # Filter out non attachment tables   
        if '__ATTACH' not in table:
            continue
        
        print(table)
        
        # Build the output project paths
        project_id = table.replace('__ATTACH', '')
        output_project_path = os.path.join(output_path, project_id)
        table_path = os.path.join(gdb_path, table)
        
        # Call the processing function
        process_attachment(output_project_path, table_path)
        
        # Add to the dictionary
        attachment_dict[project_id] = output_project_path
            
    print(attachment_dict)
    
    # Return the attachement dictionary
    return attachment_dict

def process_attachment(output_project_path, table_path):
    '''
    Proccesses any attachments handed to it.

    Parameters:
    - gdb_path (str): Path to input GDB.
    - output_path (str): Path to export the attachments to.
    
    Return:
    - attachment_dict (dict): A dictionary of key value pairs to tie each project id that had attachments to the path they were extracted to.
    '''                 
    # Check if the directory exists, if not, create it
    if not os.path.exists(output_project_path):
        os.makedirs(output_project_path)
    
    # Extract the attachment files from each table
    # Credits: To Andrea for finding method and original author at
    # https://support.esri.com/en-us/knowledge-base/how-to-batch-export-attachments-from-a-feature-class-in-000011912
    with arcpy.da.SearchCursor(table_path, ['DATA', 'ATT_NAME', 'ATTACHMENTID']) as cursor:
        for item in cursor:
            attachment = item[0]
            filenum = "ATT" + str(item[2]) + "_"
            filename = filenum + str(item[1])
            open(output_project_path + os.sep + filename, 'wb').write(attachment.tobytes())
            del item
            del filenum
            del filename
            del attachment
            
#========================================================
# Main
#========================================================
def main():#
    """ The main function of the geo_attachment_seeker.py script """
    # Get the start time of the script
    start_time = time.time()
    print(f'Tool is starting...')
    
    # Initialize the argument parse
    parser = argparse.ArgumentParser(description='This tools purpose is to ')
    
    # Define command-line arguments
    parser.add_argument('gdb_path', help='Input GDB path')
    parser.add_argument('output_path', help='Where to export the attachments to')
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Access the values using the attribute notation
    gdb_path = args.gdb_path
    output_path = args.output_path
    
    # Call the function to perform the processing
    find_attachments(gdb_path, output_path)
        
    # Get the end time of the script and calculate the elapsed time
    end_time = time.time()
    print(f'\nTool has completed')
    print(f'Elapsed time: {end_time - start_time:.2f} seconds')


#========================================================
# Main Guard
#========================================================
if __name__ == "__main__":
    sys.exit(main())
    