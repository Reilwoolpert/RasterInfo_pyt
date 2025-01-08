# -*- coding: utf-8 -*-

import arcpy
import csv
import os
from collections import Counter


class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Raster Statistics Toolbox"
        self.alias = "RasterStats"

        # List of tool classes associated with this toolbox
        self.tools = [Tool]


class Tool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Tool"
        self.description = ""
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        # First parameter
        param0 = arcpy.Parameter(
            displayName="Input Raster Folder",
            name="in_folder",
            datatype="DEFolder",
            parameterType="Required",
            direction="Input")

        # Second parameter
        param1 = arcpy.Parameter(
            displayName="Output CSV File",
            name="out_csv",
            datatype="DEFile",
            parameterType="Required",
            direction="Output")
            #param1.filter.list = "csv"
            #filter = "csv")

        param1.filter.list = ['csv']

        params = [param0, param1]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        in_folder = parameters[0].valueAsText
        output_csv = parameters[1].valueAsText
        export_statistics_to_csv(raster_folder, output_csv)
        messages.addMessage(f"Raster statistics have been exported to {output_csv}")
        return

    def get_raster_statistics(raster_path):
        raster = arcpy.Raster(raster_path)
    
        # Get the extent
        extent = raster.extent
        xmin, xmax, ymin, ymax = extent.XMin, extent.XMax, extent.YMin, extent.YMin
    
        # Get basic statistics
        mean = arcpy.GetRasterProperties_management(raster, "MEAN").getOutput(0)
        max_val = arcpy.GetRasterProperties_management(raster, "MAXIMUM").getOutput(0)
        min_val = arcpy.GetRasterProperties_management(raster, "MINIMUM").getOutput(0)
    
        # Get the spatial reference
        spatial_ref = raster.spatialReference
        horizontal_datum = spatial_ref.GCS.datumName if spatial_ref.GCS else "Unknown"
        horizontal_projection = spatial_ref.name if spatial_ref.name else "Unknown"
        horizontal_units = spatial_ref.linearUnitName if spatial_ref.linearUnitName else "Unknown"
        vertical_datum = spatial_ref.VCS.name if spatial_ref.VCS else "Unknown"
        vertical_projection = spatial_ref.VCS.name if spatial_ref.VCS else "Unknown"
        vertical_units = spatial_ref.VCS.verticalUnitName if spatial_ref.VCS and spatial_ref.VCS.verticalUnitName else "Unknown"
    
        # Get cell size
        cell_size_x = raster.meanCellWidth
        cell_size_y = raster.meanCellHeight
    
        # Get the number of bands
        band_count = raster.bandCount
    
        # Get band names
        band_names = raster.bandNames
    
        return {
            'raster_path': raster_path,
            'xmin': xmin,
            'xmax': xmax,
            'ymin': ymin,
            'ymax': ymax,
            'mean': mean,
            'max_val': max_val,
            'min_val': min_val,
            'horizontal_datum': horizontal_datum,
            'horizontal_projection': horizontal_projection,
            'horizontal_units': horizontal_units,
            'vertical_datum': vertical_datum,
            'vertical_projection': vertical_projection,
            'vertical_units': vertical_units,
            'cell_size_x': cell_size_x,
            'cell_size_y': cell_size_y,
            'band_count': band_count,
            'band_names': ', '.join(band_names)  # Convert list of band names to a comma-separated string
        }

    def export_statistics_to_csv(raster_folder, output_csv):
        # List to hold statistics for each raster
        statistics = []

        #newstuff here
        horizontal_datums = []
        horizontal_projections = []
        horizontal_units = []

        vert_datums = []
        vert_projs = []
        vert_units = []

        cell_x = []
        cell_y = []
        band_count = []
        band_names = []


        for root, _, files in os.walk(raster_folder):
            for file in files:
                if file.endswith(('.tif', '.img', '.sid')):
                    raster_path = os.path.join(root, file)
                    stats = get_raster_statistics(raster_path)
                    statistics.append(stats)
                    #horizontal stuff
                    horizontal_datums.append(stats['horizontal_datum'])
                    horizontal_projections.append(stats['horizontal_projection'])
                    horizontal_units.append(stats['horizontal_units'])

                    #vertical stuff
                    vert_datums.append(stats['vertical_datum'])
                    vert_projs.append(stats['vertical_projection'])
                    vert_units.append(stats['vertical_units'])

                    #cell size and band stuff
                    cell_x.append(stats['cell_size_x'])
                    cell_y.append(stats['cell_size_y'])
                    band_count.append(stats['band_count'])
                    band_names.append(stats['band_names'])

        #get unique and totals
        unique_datums = Counter(horizontal_datums)
        total_unique_datums = len(unique_datums)

        unique_H_proj = Counter(horizontal_projections)
        total_unique_proj = len(unique_H_proj)

        unique_H_units = Counter(horizontal_units)
        total_unique_Hunits = len(unique_H_units)

        unique_Vdatums = Counter(vert_datums)
        total_UVdatums = len(unique_Vdatums)

        unique_Vproj = Counter(vert_projs)
        total_UVprojs = len(unique_Vproj)

        unique_Vunits = Counter(vert_units)
        total_UVunits = len(unique_Vunits)

        unique_cellX = Counter(cell_x)
        total_cellX = len(unique_cellX)

        unique_cellY = Counter(cell_y)
        total_cellY = len(unique_cellY)

        unique_bandC = Counter(band_count)
        total_bandC = len(unique_bandC)

        unique_bandN = Counter(band_names)
        total_bandN = len(unique_bandN)



        # Define the CSV fieldnames based on the keys of the dictionary
        fieldnames = [
            'raster_path', 'xmin', 'xmax', 'ymin', 'ymax',
            'mean', 'max_val', 'min_val', 'horizontal_datum', 'horizontal_projection', 'horizontal_units', 'vertical_datum',
            'vertical_projection', 'vertical_units',
            'cell_size_x', 'cell_size_y', 'band_count', 'band_names'
        ]
    
        # Write statistics to the CSV file
        with open(output_csv, mode='w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
            # Write the header with the number of files scanned
            writer.writerow({'raster_path': f'Files scanned: {len(statistics)}'})

            #horizontal
            writer.writerow({'raster_path': f'H Datum: {total_unique_datums} unique -- ' + ', '.join(unique_datums)})
            writer.writerow({'raster_path': f'H Proj: {total_unique_proj} unique -- ' + ', '.join(unique_H_proj)})
            writer.writerow({'raster_path': f'H Unit: {total_unique_Hunits} unique -- ' + ', '.join(unique_H_units)})

            #vertical
            writer.writerow({'raster_path': f'V Datum: {total_UVdatums} unique -- ' + ', '.join(unique_Vdatums)})
            writer.writerow({'raster_path': f'V Proj: {total_UVprojs} unique -- ' + ', '.join(unique_Vproj)})
            writer.writerow({'raster_path': f'V Units: {total_UVunits} unique -- ' + ', '.join(unique_Vunits)})


            #cast integers as strings
            writer.writerow(
                {'raster_path': f'Cell X Size: {total_cellX} unique -- ' + ', '.join(map(str, unique_cellX.keys()))})
            writer.writerow(
                {'raster_path': f'Cell Y Size: {total_cellY} unique -- ' + ', '.join(map(str, unique_cellY.keys()))})
            writer.writerow(
                {'raster_path': f'Band Count: {total_bandC} unique -- ' + ', '.join(map(str, unique_bandC.keys()))})

            #writer.writerow({'raster_path': f'V BandCount: {total_bandC} unique -- ' + ', '.join(unique_bandC)})
            writer.writerow({'raster_path': f'V BandName: {total_bandN} unique -- ' + ', '.join(unique_bandN)})



            # Write the header for field names
            writer.writeheader()
        
            for stats in statistics:
                writer.writerow(stats)


    def postExecute(self, parameters):
        """This method takes place after outputs are processed and
        added to the display."""
        return
