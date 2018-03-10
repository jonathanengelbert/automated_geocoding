# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# geocoding.py
# Created on: 2018-02-23 10:51:03.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: This script geocodes a table of addresses from an Excel
# spreadsheet.
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy
arcpy.env.overwriteOutput = True

arcpy.env.workspace = r"I:\GIS\OASIS\Geocoder\geocoder.gdb"

def geocode():
    try:
        # Local variables:
        transformed_xlsx = "I:\\GIS\\OASIS\\Geocoder\\transformed.xlsx"
        transfomed = "I:\\GIS\\OASIS\\Geocoder\\geocoder.gdb\\transfomed"
        AddressLocator_Master_Address_Database = "I:\\GIS\\OASIS\\AddressLocators\\AddressLocator_Master_Address_Database"
        geocoded_addresses = "I:\\GIS\\OASIS\\Geocoder\\geocoder.gdb\\geocoded_addresses"
        geocoder_gdb = "I:\\GIS\\OASIS\\Geocoder\\geocoder.gdb"
        geocoded_addresses_failed = "geocoded_addresses_failed"
        unmatched_xls = "I:\\GIS\\OASIS\\Geocoder\\unmatched.xls"
        unmatched = "I:\\GIS\\OASIS\\Geocoder\\geocoder.gdb\\unmatched"
        unmatched__3_ = unmatched
        AddressLocator_Street_Centerlines__2_ = "I:\\GIS\\OASIS\\AddressLocators\\AddressLocator_Street_Centerlines"
        geocoded_street_centerlines = "I:\\GIS\\OASIS\\Geocoder\\geocoder.gdb\\geocoded_street_centerlines"
        geocoded_street_centerlines_successful = "geocoded_street_centerlines_successful"
        geocoded_street_centerlines_successful__2_ = geocoded_street_centerlines_successful
        geocoded_street_centerlines_successful__3_ = geocoded_street_centerlines_successful__2_
        geocoder_gdb__2_ = "I:\\GIS\\OASIS\\Geocoder\\geocoder.gdb"
        geocoded_master_successful = "geocoded_master_successful"
        geocoded_master_successful__2_ = geocoded_master_successful
        geocoded_master_successful__4_ = geocoded_master_successful__2_
        geocoder_eas = "I:\\GIS\\OASIS\\Geocoder\\geocoder.gdb\\geocoder_eas"
        final = "I:\\GIS\\OASIS\\Geocoder\\geocoder.gdb\\final"

        # Process: Excel To Table
        try:
            arcpy.ExcelToTable_conversion(transformed_xlsx, transfomed)
        except Exception as e:
            print(e)
        # Process: Geocode Addresses
        try:
            arcpy.GeocodeAddresses_geocoding(transfomed,
                                             AddressLocator_Master_Address_Database,
                                             "Key transformed_address VISIBLE NONE",
                                             geocoded_addresses, "STATIC", "", "")
        except Exception as e:
            print(e)

        # Process: Make Feature Layer
        try:
            arcpy.MakeFeatureLayer_management(geocoded_addresses,
                                              geocoded_addresses_failed,
                                              "Status = 'U'", geocoder_gdb,
                                              "ObjectID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Status Status VISIBLE NONE;Score Score VISIBLE NONE;Match_type Match_type VISIBLE NONE;Match_addr Match_addr VISIBLE NONE;X X VISIBLE NONE;Y Y VISIBLE NONE;Xmin Xmin VISIBLE NONE;Xmax Xmax VISIBLE NONE;Ymin Ymin VISIBLE NONE;Ymax Ymax VISIBLE NONE;Addr_type Addr_type VISIBLE NONE;ARC_Single_Line_Input ARC_Single_Line_Input VISIBLE NONE")
        except Exception as e:
            print(e)
        # Process: Table To Excel

        try:
            arcpy.TableToExcel_conversion(geocoded_addresses_failed, unmatched_xls,
                                      "NAME", "CODE")

        except Exception as e:
            print(e)
        # Process: Excel To Table (2)


        arcpy.ExcelToTable_conversion(unmatched_xls, unmatched, "")

        # Process: Delete Field
        arcpy.DeleteField_management(unmatched,
                                     "OBJECTID_1;Status;Score;Match_type;Match_addr;X;Y;Xmin;Xmax;Ymin;Ymax;Addr_type;ARC_Single_Line_Input;ARC_SingleKey")

        # Process: Geocode Addresses (2)
        arcpy.GeocodeAddresses_geocoding(unmatched__3_,
                                         AddressLocator_Street_Centerlines__2_,
                                         "'Full Address' transformed_address VISIBLE NONE",
                                         geocoded_street_centerlines, "STATIC", "",
                                         "")

        # Process: Make Feature Layer (3)
        arcpy.MakeFeatureLayer_management(geocoded_street_centerlines,
                                          geocoded_street_centerlines_successful,
                                          "", "",
                                          "ObjectID ObjectID VISIBLE NONE;Shape Shape VISIBLE NONE;Status Status VISIBLE NONE;Score Score VISIBLE NONE;Match_type Match_type VISIBLE NONE;Match_addr Match_addr VISIBLE NONE;Side Side VISIBLE NONE;Ref_ID Ref_ID VISIBLE NONE;User_fld User_fld VISIBLE NONE;Addr_type Addr_type VISIBLE NONE;ARC_Single_Line_Input ARC_Single_Line_Input VISIBLE NONE")

        # Process: Add Field (2)
        arcpy.AddField_management(geocoded_street_centerlines_successful,
                                  "geocoder", "TEXT", "", "", "", "", "NULLABLE",
                                  "NON_REQUIRED", "")

        # Process: Calculate Field (2)
        arcpy.CalculateField_management(geocoded_street_centerlines_successful__2_,
                                        "geocoder", "classifyGeocoder(!Status!)",
                                        "PYTHON",
                                        "def classifyGeocoder(Status):\\n  if Status == \"M\" or Status == \"T\":\\n   return \"SC\"\\n  else:\\n    return \"U\"")

        # Process: Make Feature Layer (2)
        arcpy.MakeFeatureLayer_management(geocoded_addresses,
                                          geocoded_master_successful,
                                          "Status = 'M'  OR  Status = 'T'",
                                          geocoder_gdb__2_,
                                          "ObjectID OBJECTID VISIBLE NONE;Shape Shape VISIBLE NONE;Status Status VISIBLE NONE;Score Score VISIBLE NONE;Match_type Match_type VISIBLE NONE;Match_addr Match_addr VISIBLE NONE;X X VISIBLE NONE;Y Y VISIBLE NONE;Xmin Xmin VISIBLE NONE;Xmax Xmax VISIBLE NONE;Ymin Ymin VISIBLE NONE;Ymax Ymax VISIBLE NONE;Addr_type Addr_type VISIBLE NONE;ARC_Single_Line_Input ARC_Single_Line_Input VISIBLE NONE")

        # Process: Add Field
        arcpy.AddField_management(geocoded_master_successful, "geocoder", "TEXT",
                                  "", "", "20", "", "NULLABLE", "NON_REQUIRED", "")

        # Process: Calculate Field
        arcpy.CalculateField_management(geocoded_master_successful__2_, "geocoder",
                                        "\"EAS\"", "PYTHON", "")

        # Process: Copy Features
        arcpy.CopyFeatures_management(geocoded_master_successful__4_, geocoder_eas,
                                      "", "0", "0", "0")

        # Process: Merge
        print("SUCCEDED")
        fieldmappings = arcpy.FieldMappings()
        fieldmappings.addTable(transfomed)

        arcpy.Merge_management(
            "I:\\GIS\\OASIS\\Geocoder\\geocoder.gdb\\geocoder_eas; geocoded_street_centerlines_successful",
            final, fieldmappings)

        print("GEOCODING SUCCESSFUL")
    except Exception as e:
        print("ERROR")
        print(e)

if __name__ == "__main__":
    geocode()
    print("\nAddresses Processed")
    exit()


