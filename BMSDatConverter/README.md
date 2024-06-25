# Convert Aircraft Data to Protocol Buffer Format
This utility is able to take the old acdata .dat and _afm.dat with the default TGP data
and create the new protocol buffer version of the data. On average the file size remains
similar or smaller for airframes with .dat only specifically.

The ConvertAirframeData.exe reads the old .dat files, creates the new proto buffer file and 
reads the new file for adherence to the protocol format. You can either generate with the
default scalar lists notation by applying a reflow for arrays and many tables. Optionally you
can use the Google default text output by disabling this reflow. The default is to generate
the proto text format but the tool can also create the binary version if instructed.

## Building The Converter
The build steps are pretty straight forward and are setup for both Debug and Release
cofigurations. The projects are setup for both VS2022 and VS2019.

1. Build ExtLibs
2. Build ConvertAirframeData project

This will create the ConvertAirframeData.exe executable in the Release or Debug folder
of the ProtoConverters folder.

## Usage

The tool takes several options of which two (i.e. sim_data_path and user_config_path) 
are mandatory. The tool uses this to find the .dat files and the BMS Config data.

`ConvertAirframeData -d <sim_data_path> -c <user_config_path> [-l] [-b] [-a <aircraft>]`

The option -l will disable the reflow and outputs fully expanded Text Proto format.
If you just want to convert a single aircraft or a set you can use the -a option with
a match pattern. To be sure to only convert a file use something like "F-18C." with the
dot so it will match a single aircraft. Without -a it will generate all the .txtpb for all
aircraft. The option -b will generate the binary protocol buffer format instead of the
text proto format.

## Examples

`ConvertAirframeData -d "C:\\Falcon BMS 4.37 (Internal)\\Data\\Sim" -c "C:\\Falcon BMS 4.37 (Internal)\\User\\Config" -a "F-18C."`
`ConvertAirframeData -d "C:\\Falcon BMS 4.37 (Internal)\\Data\\Sim" -c "C:\\Falcon BMS 4.37 (Internal)\\User\\Config" -b`
