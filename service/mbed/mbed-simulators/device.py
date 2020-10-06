import sys
import os
import time

def main():
    deviceNum = int(sys.argv[1])
    fileDir = os.path.dirname(os.path.realpath('__file__'))
    file = open(os.path.join(fileDir, 'source/main.cpp'), "r+")
    fileData = file.read()
    typeFilter = 'ENDPOINT_NAME,'
    typePosition = fileData.find(typeFilter)
       
    for x in range(deviceNum):
	file.seek(typePosition + 14, 0)
	if (int(x) % 2)==0:
	    file.write('"test2"' + ",        ")
	else:
	    file.write('"test"' + ",        ")
        data = "/bin/cp security/security_{}.h source/security.h".format(x)  
        os.system(data)
        os.system('yotta build')
        os.system('./build/x86-linux-native/source/mbed-client-linux-example &> /dev/null &')
        time.sleep(1)

    file.close()

    while True: 
        pass

if __name__=="__main__":
    main()
