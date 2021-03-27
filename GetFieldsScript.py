

from KuiperAPI import Kuiper_API
import argparse


Kuiper_URL = "https://192.168.1.110/api/"
api_token = ""


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

	parser.add_argument('-u' , dest='url' ,                 help='API URL for kuiper (default: '+Kuiper_URL+')' , default=Kuiper_URL)
	parser.add_argument('-t' , dest='token' ,               help='API token (default:<taken from script>)' , default=api_token)
	parser.add_argument('-q' , dest='query' ,               help='query string for elasticsearch', default='*')
	parser.add_argument('-s' , dest='sort_by' ,             help='field to sort by', default=None)


	args = parser.parse_args()


	# ================= get records from kuiper
	k 		= Kuiper_API(args.url , args.token)
	sort_by = None if args.sort_by is None else {'name':args.sort_by , 'order':0 }
	res 	= k.get_artifacts(case=args.case_id , query_string=args.query,sort_by=sort_by , fields=args.fields)

	output = open(args.output_file, 'w')
	fields = args.fields.split(",")
	output.write(args.fields + "\n")

	for r in res:
		hashes = []
		for record in r['data']['hits']['hits']:
			rec = []
			for f in fields:
				rec.append(getJsonByPath(record['_source'] , f))
			line = ','.join(rec)
			if line.replace("," , "") != "": # if the line is not empty
				output.write(line  + "\n")
			
		print("total:%d, retrieved_records:%d, chunk_number: %d" % (r['total'] , r['retrieved_records'] , r['seq_number']))

	output.close()


main()