

from KuiperAPI import Kuiper_API
import argparse

import json 

Kuiper_URL = "https://192.168.220.5/api/"
api_token = "API_TOKEN"


def getJsonByPath(json , path):
	if type(path) == str:
		path = path.split(".")
	try:
		if len(path) > 1:
			return getJsonByPath(json[path[0]] , path[1:])
		return json[path[0]]
	except:
		return ""

def main():
	# ================== Arguments
	parser = argparse.ArgumentParser(description="Get specific fields from Kuiper and write to csv file.\n\n")
	requiredargs = parser.add_argument_group('required arguments')
	requiredargs.add_argument('-c' , dest='case_id' ,             help='case id', required=True)
	requiredargs.add_argument('-f' , dest='fields' ,              help='specific fields to retrieve (split by comma)', required=True)
	requiredargs.add_argument('-o' , dest='output_file' ,         help='Output file to store the results to', required=True)

	parser.add_argument('-u'  , dest='url' ,                 help='API URL for kuiper (default: '+Kuiper_URL+')' , default=Kuiper_URL)
	parser.add_argument('-t'  , dest='token' ,               help='API token (default:<taken from script>)' , default=api_token)
	parser.add_argument('-q'  , dest='query' ,               help='query string for elasticsearch', default='*')
	parser.add_argument('-s'  , dest='sort_by' ,             help='field to sort by', default=None)
	parser.add_argument('-cs' , dest='chunk_size' ,          help='field to sort by', default=30)


	args = parser.parse_args()


	# ================= get records from kuiper
	k 		= Kuiper_API(args.url , args.token)
	sort_by = None if args.sort_by is None else {'name':args.sort_by , 'order':0 }
	fields  = None if args.fields is None or args.fields == "*" else args.fields
	res 	= k.get_artifacts(case=args.case_id , query_string=args.query,sort_by=sort_by , fields=fields , chunk_size=int(args.chunk_size))

	isJson = True if fields is None else False # if there are no selected fields, write output to json file
	output = open(args.output_file, 'w')

	if not isJson:
		output.write(fields + "\n")
		fields_list = fields.split(",")

	for r in res:
		if 'success' in r.keys() and r['success'] == False:
			print("Failed to fetch the records: %s" % (r['message']))
			break
		for record in r['data']['hits']['hits']:
			# if output is json, then write all the records
			if isJson:
				output.write(json.dumps({"_source": record['_source'] , "_index" : record['_index']}) + "\n")

			# if output is not json, then write only specified records
			else:
				rec = []
				for f in fields_list:
					if f == "index" or f == "case_id": 
						rec.append(record['_index'])
					else: 
						rec.append(getJsonByPath(record['_source'] , f))

				line = ','.join(rec)
				if line.replace("," , "") != "": # if the line is not empty
					output.write(line  + "\n")
			
		print("total:%d, retrieved_records:%d, chunk_number: %d" % (r['total'] , r['retrieved_records'] , r['seq_number']))
	output.close()


main()