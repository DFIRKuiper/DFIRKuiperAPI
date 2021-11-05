
from KuiperAPI import Kuiper_API
import argparse


Kuiper_URL = "https://192.168.220.5/api/"
api_token = "API_TOKEN"

def main():
	# ================== Arguments
	parser = argparse.ArgumentParser(description="Upload package machine (.zip) to Kuiper\n\n")
	requiredargs = parser.add_argument_group('required arguments')
	requiredargs.add_argument('-c' , dest='case_id' ,             help='Case id ', required=True)
	requiredargs.add_argument('-m' , dest='machine_name' ,        help='Machine name', required=True)
	requiredargs.add_argument('-p' , dest='machine_path' ,        help='Machine compressed file (.zip)', required=True)

	
	parser.add_argument('-u' , dest='url' ,                 help='API URL for kuiper (default: '+Kuiper_URL+')' , default=Kuiper_URL)
	parser.add_argument('-t' , dest='token' ,               help='API token (default:<taken from script>)' , default=api_token)
	args = parser.parse_args()


	# ================= upload machine to kuiper
	k 		= Kuiper_API(args.url , args.token)
	res 	= k.upload_machine(case=args.case_id , machine_name=args.machine_name + ".zip" , file_path=args.machine_path)

	print(res)

if __name__ == "__main__":
	main()
