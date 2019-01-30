import requests
import json
from shutil import copyfile

def compare(File1, File2):
    with open(File1, 'r') as f:
        d = set(f.readlines())
		
    with open(File2, 'r') as f:
        e = set(f.readlines())
		
    open('difference.txt', 'w').close()
	
    with open('difference.txt', 'a') as f:
        for line in list(d-e):
            f.write(line)

error = 0

with open("tvaDomains.txt", "r") as f:
    copyfile('newOutput.txt', 'oldOutput.txt')
    with open('newOutput.txt', 'w') as out:

        for line in f:
            domain = line.strip()
            lst = []
            while True:
                aResponse = requests.get("https://dns.google.com/resolve?name={}&type=A".format(domain)).json()
                if 'Answer' in aResponse and len(aResponse["Answer"]) > 0:
                    break
            while True:
                mxResponse = requests.get("https://dns.google.com/resolve?name={}&type=MX".format(domain)).json()
                if 'Answer' in mxResponse and len(mxResponse["Answer"]) > 0:
                    break
            while True:
                nsResponse = requests.get("https://dns.google.com/resolve?name={}&type=NS".format(domain)).json()
                if 'Answer' in nsResponse and len(nsResponse["Answer"]) > 0:
                    break
            lst.append("Domain")
            lst.append(domain)
			
            if not 'Answer' in aResponse or len(aResponse["Answer"]) == 0:
                print "'A' record query failed."
                lst.append("A Record:")
                lst.append("Null")
                error += 1
            else:
                #print len(aResponse["Answer"])
                for i in xrange(len(aResponse["Answer"])):
                    lst.append("A Record:")
                    lst.append(aResponse["Answer"][i]["data"])
					
            if not 'Answer' in mxResponse or len(mxResponse["Answer"]) == 0:
                print "'MX' record query failed."
                lst.append("MX Record:")
                lst.append("Null")
                error += 1
            else:
                #print len(aResponse["Answer"])
                for i in xrange(len(mxResponse["Answer"])):
                    lst.append("MX Record:")
                    lst.append(mxResponse["Answer"][i]["data"])
					
            if not 'Answer' in nsResponse or len(nsResponse["Answer"]) == 0:
                print "'NS' record query failed."
                lst.append("NS Record:")
                lst.append("Null")
                error += 1
            else:
                #print len(nsResponse["Answer"])
                for i in xrange(len(nsResponse["Answer"])):
                    lst.append("NS Record:")
                    lst.append(nsResponse["Answer"][i]["data"])
            print >> out, lst
        print "Total Errors: {}".format(error)
f.close()
out.close()

compare('oldOutput.txt', 'newOutput.txt')