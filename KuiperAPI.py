

import json
import requests
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


from requests_toolbelt import MultipartEncoder
import base64


class Kuiper_API:

	def __init__(self, Kuiper_URL, api_token):
		self.Kuiper_URL = Kuiper_URL
		self.api_token  = api_token

	# ================= get_artifacts
	# this function request kuiper to retrive parsed artifacts from the server
	# case: 		case id from in kuiper
	# query_string: the search query from the database
	# sort_by: 		the field to sort by (example: {'name': 'Data.@timestamp' , 'order': 0}) >> 0=asc, 1=desc
	# fields: 		retrive specific fields from the server (if not specified it will return all the values), split fields by comma
	# return: this function return a generator that retrieves the data from the server as a chunks 
	def get_artifacts(self, case , query_string , sort_by=None, fields=None, chunk_size=30):

		total_records 		= -1 # this store the number of records in the database
		retrieved_records 	= 0  # this is the number of records retrieved so far 
		seq_number 			= 0  # this is the iteration number

		json_request = {
			'query' 	: query_string,
			'sort_by' 	: sort_by,
			'fields' 	: fields,
			'api_token' : self.api_token,
			'case_id'	: case,
			'chunk_size': chunk_size
		}
		
		while retrieved_records < total_records or seq_number == 0:

			json_request['seq_num'] = seq_number
			json_string = json.dumps({'data': json_request})
			response = requests.post(self.Kuiper_URL + "get_artifacts", data=json_string , verify=False)
			#print(response.content)
			response_json 	 = json.loads(response.content)
			if response_json['success']:
				retrieved_records += len(response_json['data']['hits']['hits'])
				total_records 	 = response_json['total']

				response_json['retrieved_records'] = retrieved_records
				response_json['seq_number'] 	   = seq_number

				seq_number		 +=1 
				yield response_json
			else:
				yield response_json



	# ================== upload machine
	# this function upload specific machine to Kuiper server for specific case
	# case:			case id from Kuiper
	# machine_name: machine name to be created in the case
	# file_path:	path of the zip file
	def upload_machine(self, case , machine_name , file_path):
		m_name_base64 = base64.urlsafe_b64encode(machine_name.encode("utf-8"))
		m = MultipartEncoder(
			fields={
					'api_token'	 : self.api_token , 
					'base64_name': m_name_base64,
					'files'		 : (m_name_base64 , open(file_path , "rb") , "application/zip") 
				}
			)


		r = requests.post(self.Kuiper_URL + "upload_machine/"+case , data=m, headers={'Content-Type': m.content_type}, verify=False)
		return json.loads(r.content)






