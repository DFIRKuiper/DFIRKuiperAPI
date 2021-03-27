# DFIR-Kuiper-API

This script to communicate with [DFIRKuiper](https://github.com/DFIRKuiper/Kuiper) API, currently this script only retrives parsed data from Kuiper.

### Use Cases

If analyst want to exteract a chunk of data (such as hash values, IP addresses, paths, etc.) as a CSV format from Kuiper database, and then check if with other sources (VT, whois, etc.), then you could use the API script,

### Usage

Script parameters

```shell
usage: GetFieldsScript.py [-h] -c CASE_ID -f FIELDS -o OUTPUT_FILE [-u URL]
                          [-t TOKEN] [-q QUERY] [-s SORT_BY]

Get specific fields from Kuiper and write to csv file.

optional arguments:
  -h, --help      show this help message and exit
  -u URL          API URL for kuiper (default: https://192.168.1.110/api/)
  -t TOKEN        API token (default:<taken from script>)
  -q QUERY        query string for elasticsearch
  -s SORT_BY      field to sort by

required arguments:
  -c CASE_ID      case id
  -f FIELDS       specific fields to retrieve (split by comma)
  -o OUTPUT_FILE  Output file to store the results to
```

**TOKEN**: You should use the same token in the server side (in `configuration.yaml` file as `Kuiper`->`api_token`). 

**QUERY**: it is elasticsearch query string, for ease of use, you can copy the same raw query from Kuiper interface and place it here 

![search_query_string](https://github.com/DFIRKuiper/DFIRKuiperAPI/blob/main/search_query_string.png?raw=true)

FIELDS: the exteracted fields, to get the current path, open Kuiper interface, then select record, and click on artifact details icon, and copy the wanted field

![select_fields_1](https://github.com/DFIRKuiper/DFIRKuiperAPI/blob/main/select_fields_1.png?raw=true)

![select_fields_2](https://github.com/DFIRKuiper/DFIRKuiperAPI/blob/main/select_fields_2.png?raw=true)

#### Example

```shell
python3 GetFieldsScript.py -u https://192.168.1.110/api/ -t "<api_token>"  -c test -q 'data_type:"LastVisitedMRU"' -f 'Data.File_name' -o output.csv
```







