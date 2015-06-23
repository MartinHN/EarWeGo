"""OSC Test Script
Written by Aaron Chamberlain Dec. 2013
The purpose of this script is to make a very simple communication structure to the popular 
application touchOSC. This is achieved through the pyOSC library. However, since the pyOSC 
documentation is scarce and only one large example is included, I am going to strip down 
the basic structures of that file to implement a very simple bi-directional communication.
"""
 
#!/usr/bin/env python
 
import socket, OSC, re, time, threading, math,os,subprocess,json

debug = False;
dbSlicePath = "dataset/dataset.json"
filenamesPath = "dataset/filenames.json"
receive_address = '1.1.1.2', 4444 #Mac Adress, Outgoing Port
receive_addresslocal = 'localhost', 4444 #Mac Adress, Outgoing Port
send_address = '1.1.1.1', 4445 #iPhone Adress, Incoming Port

key = "C#"
mode = "minor"
bpm = 100

minMax = {}
minMax["flatness"] = [0,1]
minMax["spectral_centroid"] = [0,1]




slices = []
loops = {}



# loading stuff
f = open(dbSlicePath);
print dbSlicePath
jdata = json.load(f)
bpms = set()
numSlices = 0
for v in jdata["BPM"]:
	numSlices+=1
	bpms.add(v);

for i in range(numSlices):
	dicti = {}
	for k,v in jdata.iteritems():
		if isinstance (v,dict):
			dicti[k] = v["mean"][i]
			if(k=="flatness"):
				minMax["flatness"][0] = min(minMax["flatness"][0], dicti[k])
				minMax["flatness"][1] = max(minMax["flatness"][1], dicti[k])
			elif k == "spectral_centroid":
				minMax["spectral_centroid"][0] = min(minMax["spectral_centroid"][0], dicti[k])
				minMax["spectral_centroid"][1] = max(minMax["spectral_centroid"][1], dicti[k])
		elif isinstance(v,list):
			dicti[k] = v[i]
		else:
			print "not supported"
		# print dicti
		
	slices+= [dicti]
f.close()

f = open(filenamesPath);
jdata = json.load(f)

sounds = [x for x in jdata["names"] if '.wav' in x]
if len(sounds) : 
	
	for s in sounds:
		info = s.split('_')
		i = int(info[0])
		slices[i]["name"] = s
		slices[i]["genre"] = info[1]
		slices[i]["key"] = info[2].split('-')[0]
		slices[i]["mode"] = info[2].split('-')[1]
		
print len(slices)

f.close()




def setclosestBPM(bp):
	global bpms;
	minDist = 300
	print bpms
	for b in bpms:
		if abs(b-bp)<minDist :
			minDist = abs(b-bp)
			bpm = b
	


class PiException(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
 
##########################
#	OSC
##########################

	


# Initialize the OSC server and the client.
print receive_address
s = OSC.OSCServer(receive_address)
s2 = OSC.OSCServer(receive_addresslocal)
c = OSC.OSCClient()
c.connect(send_address)
 
s.addDefaultHandlers()

 




# /data noise centroid bpm
def getFiles(add,type,data,sender):
	
	if debug:
		print "recieved : "+key + " : "+ mode
 	global key
	global mode
	global bpm
	global minMax
	global c
	noise = data[0]
	centroid = data[1]
	bp = data[2]
	setclosestBPM(bp)
	if debug:
		print key
		print mode 
		print bpm
		

	bpSlice = []
	for x in slices:
		# print x , mode , x["mode"] , key , x["key"]
		if x["mode"] == mode and x["key"] == key:
			bpSlice+=[x]
			

	
	if debug:
		print bpSlice
	outSlice = []
	
	count = 0
	for s in bpSlice:
		if count>16:
			break;
		if( (abs(s["BPM"] - bp )< 3) and abs((s["spectral_centroid"]-minMax["spectral_centroid"][0])/(minMax["spectral_centroid"][1]-minMax["spectral_centroid"][0]) - s["spectral_centroid"]) < .2 ) or (abs((s["flatness"]-minMax["flatness"][0])/(minMax["flatness"][1]-minMax["flatness"][0])) - s["flatness"])< .2:
			count+=1;
			outSlice+=[s["name"]];
		



	
	for s in outSlice:
		msg = OSC.OSCMessage()
		msg.setAddress("/file")
		print s
		msg.append(s)
		c.send(msg)
	
	





def setKey(add,type,data,sender):
	global key
	global mode
	# print(add,p,_key,_mode)
	# mode = data[0]
	key = data[1]
	print key
	print mode

	
# adding my functions
s.addMsgHandler("/data", getFiles);
s2.addMsgHandler("/key",setKey)

print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
	print addr
print "listening on :"+ receive_address[0] +":"+ str(receive_address[1])
print "sending on" + send_address[0] +":"+ str(send_address[1])
 
# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever )
st.start()
st2 = threading.Thread( target = s2.serve_forever )
st2.start()
# Loop while threads are running.
try :
	while 1 :
		time.sleep(10)
 
except KeyboardInterrupt :
	print "\nClosing OSCServer."
	s.close()
	print "Waiting for Server-thread to finish"
	st.join()
	print "Done"