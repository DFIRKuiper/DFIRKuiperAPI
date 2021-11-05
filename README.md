# DFIR-Kuiper-API

This script to communicate with [DFIRKuiper](https://github.com/DFIRKuiper/Kuiper) API, currently available features:

- [GetFieldsScript](#GetFieldsScript): Retrieves parsed data from Kuiper. 
- [UploadMachines](#UploadMachines): Upload new machine (.zip file) to specific case

NOTE: the API feature added to Kuiper from version 2.0.10


## GetFieldsScript

If analyst want to extract a chunk of data (such as hash values, IP addresses, paths, etc.) as a CSV/Json format from Kuiper database, and then check it with other sources (VT, whois, etc.), then you could use the API script,

### Usage

Script parameters

```shell
usage: GetFieldsScript.py [-h] -c CASE_ID -f FIELDS -o OUTPUT_FILE [-u URL] [-t TOKEN] [-q QUERY] [-s SORT_BY] [-cs CHUNK_SIZE]

Get specific fields from Kuiper and write to csv file.

optional arguments:
  -h, --help      show this help message and exit
  -u URL          API URL for kuiper (default: https://192.168.220.5/api/)
  -t TOKEN        API token (default:<taken from script>)
  -q QUERY        query string for elasticsearch
  -s SORT_BY      field to sort by
  -cs CHUNK_SIZE  field to sort by

required arguments:
  -c CASE_ID      case id
  -f FIELDS       specific fields to retrieve (split by comma)
  -o OUTPUT_FILE  Output file to store the results to

```

**TOKEN**: You should use the same token in the server side (in `configuration.yaml` file as `Kuiper`->`api_token`) or specified on the environment variable. 

**QUERY**: it is elasticsearch query string, for ease of use, you can copy the same raw query from Kuiper interface and place it here 

![search_query_string](https://github.com/DFIRKuiper/DFIRKuiperAPI/blob/main/search_query_string.png?raw=true)

**FIELDS**: the extracted fields, to get the correct path, open Kuiper interface, then select record, and click on artifact details icon, and copy the wanted field (use `*` to get all fields of the records and store it as json format)

![select_fields_1](https://github.com/DFIRKuiper/DFIRKuiperAPI/blob/main/select_fields_1.png?raw=true)

![select_fields_2](https://github.com/DFIRKuiper/DFIRKuiperAPI/blob/main/select_fields_2.png?raw=true)

**CASE_ID**: allowed parameters (`<case_id>` for specific case, `case_id,case_id` for multiple cases, and `*` for all cases)

#### Example

```shell
python3 GetFieldsScript.py -u https://192.168.1.110/api/ -t "<api_token>"  -c test -q 'data_type:"LastVisitedMRU"' -f 'Data.File_name' -o output.csv
```


## UploadMachines

Upload specific machine (.zip file) to a case


### Usage

Script parameters

```shell
                      
usage: UploadMachines.py [-h] -c CASE_ID -m MACHINE_NAME -p MACHINE_PATH [-u URL] [-t TOKEN]

Upload package machine (.zip) to Kuiper

optional arguments:
  -h, --help       show this help message and exit
  -u URL           API URL for kuiper (default: https://192.168.220.5/api/)
  -t TOKEN         API token (default:<taken from script>)

required arguments:
  -c CASE_ID       Case id
  -m MACHINE_NAME  Machine name
  -p MACHINE_PATH  Machine compressed file (.zip)

```

#### Example

```shell
python3 UploadMachines.py -c "<case_id>" -m "<machine_name>" -p ./machine.zip
```
