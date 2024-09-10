import re

pattern1 = re.compile(r'((\d+)s(\d+)ms)')
pattern2 = re.compile(r'((\d+)m(\d+)s(\d+)ms)')

def summaryFile(filename):
	lminute = []
	lsecond = []
	lmicrosecond = []
	microsecond = 0
	second = 0
	minute = 0
	with open(filename, 'r') as f:
		for line in f.readlines():
			res = pattern1.findall(line)
			if len(res) > 0:
				lsecond.append(int(res[0][1]))
				lmicrosecond.append(int(res[0][2]))
			res = pattern2.findall(line)
			if len(res) > 0:
				lminute.append(int(res[0][1]))
				#lsecond.append(int(res[0][2]))
				#lmicrosecond.append(int(res[0][3]))
	for e in range(0, len(lmicrosecond)):
		microsecond = microsecond + lmicrosecond[e]
	for e in range(0, len(lsecond)):
		second = second + lsecond[e]
	for e in range(0, len(lminute)):
		minute = minute + lminute[e]
	second = second + (int)(microsecond / 1000);
	microsecond = microsecond % 1000;
	minute = minute + (int)(second / 60)
	second = second % 60
	print("out", minute, second, microsecond)
	return [minute, second, microsecond]

minute = 0
second = 0
microsecond = 0
[a, b, c] = summaryFile('D:/dataset/lab/Parking/InterfaceCOLMAP-2401160834110005BD.log')
minute = minute + a
second = second + b
microsecond = microsecond + c
[a, b, c] = summaryFile('D:/dataset/lab/Parking/DensifyPointCloud-240116133649003D49.log')
minute = minute + a
second = second + b
microsecond = microsecond + c
[a, b, c] = summaryFile('D:/dataset/lab/Parking/ReconstructMesh-240116153445004285.log')
minute = minute + a
second = second + b
microsecond = microsecond + c
[a, b, c] = summaryFile('D:/dataset/lab/Parking/TextureMesh-240116155450004731.log')
minute = minute + a
second = second + b
microsecond = microsecond + c

second = second + (int)(microsecond / 1000);
microsecond = microsecond % 1000;
minute = minute + (int)(second / 60)
second = second % 60

print(minute, "minute", second, "second", microsecond, "microsecond")


'''
out 0 0 0
out 173 17 658
out 15 41 641
out 70 42 588
259 minute 41 second 887 microsecond
'''