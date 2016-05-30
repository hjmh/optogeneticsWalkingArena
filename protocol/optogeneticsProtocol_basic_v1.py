''' --------------------------------------------------------------------------------------
Possible screening protocol: repeat for 3 light levels 10%, 50%, 100%

(1) test for responses to light
continuous on in whole arena for 30s; 60s off (twice)
1s on, 1s off in whole arena for 60s; then 60s off (twice)

(2) test if aversive or attractive
continuous for 30s in 2 out of 4 quadrants; switch quadrants (twice)
1s on, 1s off for 60s in 2 out of 4 quadrants; switch quadrants (twice)
-------------------------------------------------------------------------------------- ''' 
import time, serial
from datetime import datetime

def writeDict(dict, fileHandle):
    for i in dict.keys():            
        fileHandle.write(' ' + i + ': ' + str(dict[i]) + '\n')

serialPortName = '/dev/cu.usbmodem12341'

# (1) set protocol specific parameter
LEDpowerContinuous = 2 #red LED power in percent
LEDpowerPulsed = 2 #red LED power in percent
IRpower = 0 #red LED power in percent

continuousStim = dict([('stimSec',10),
					   ('pauseSec',3),
					   ('numRepeat',2)])
# stimSec and pauseSec are in sec

pulsedStim = dict([('stimSec',3),
				   ('pauseSec',3),
				   ('onMSec',10),
				   ('offMSec',40),
				   ('numRepeat',2)])
# onMSec and offMSec are in ms


defaultPattern = '1111111111111111'
quadrantPatternA = '1100110000110011'
quadrantPatternB = '0011001111001100'

quadrantRepeat = 1

# log parameter to file
now = datetime.now()
timeStamp = now.strftime("%Y%m%d-%H%M%S")
protocolFile = 'optogeneticsScreenProtocol_' + timeStamp + 'txt'

with open(protocolFile, 'a+') as f:
	f.write('Optogenetic Screen Protocol \n \n')
	f.write('LED intensities... \n')
	f.write(' IR:' + str(IRpower) + '\n')
	f.write(' Red (continuous):' + str(LEDpowerContinuous) + '\n')
	f.write(' Red (pulsed):' + str(LEDpowerPulsed) + '\n')
	f.write('\nContinuous stimulation parameter... \n')
	writeDict(continuousStim,f)
	f.write('\nPulsed stimulation parameter...\n')
	writeDict(pulsedStim,f)
	f.write('\nPatterened stimulation parameter...\n')
	f.write(' quadrantRepeat: ' + str(quadrantRepeat) + '\n')
	f.write(' defaultPattern: ' + defaultPattern + '\n')
	f.write(' quadrantPatternA: ' + quadrantPatternA + '\n')
	f.write(' quadrantPatternB: ' + quadrantPatternB + '\n')
	
	
# (2) LED board control functions
def switchIROn(IRpower):
	ser.write('IR ' + str(IRpower) + '\r')
	print('IR ' + str(IRpower) + '\r')
	
def setRedPower(LEDpower):
	ser.write('CHR ' + str(LEDpower) + '\r')
	print('CHR ' + str(LEDpower) + '\r')
	
def switchRedOn(xLED,yLED):
	ser.write('ON ' + ''.join([str(xLED),', ',str(yLED)]) + '\r')
	# x=0, y=0 turns all LEDs on
	print('ON ' + ''.join([str(xLED),', ',str(yLED)]) + '\r')

def switchRedOff(xLED,yLED):
	ser.write('OFF ' + ''.join([str(xLED),', ',str(yLED)]) + '\r')
	# x=0, y=0 turns all LEDs off
	print('OFF ' + ''.join([str(xLED),', ',str(yLED)]) + '\r')
	
def pulseRedLight(pulseOnLength, pulseOffLength,pulseStimT):
	ser.write('PULSE, ' + ','.join([str(pulseOnLength), str(pulseOnLength+pulseOffLength),'1000', '0', '0', '1']) + '\r')
	#PULSE width, period, number, off, wait, iterations  - pulse setup command
	print('PULSE, ' + ','.join([str(pulseOnLength), str(pulseOnLength+pulseOffLength),'1000', '0', '0', '1']) + '\r')
	
	ser.write('RUN \r')
	time.sleep(pulseStimT)
	ser.write('STOP \r')

def setPattern(quadrantPattern):
	ser.write('PATT, ' + quadrantPattern + '\r')
	print('PATT, ' + quadrantPattern + '\r')
	
# (3) initialise and configure serial connection
ser = serial.Serial(serialPortName)
ser.baudrate = 115200
try:
	ser.open()
except:
	print('Port was already open.')


# (4) Switch on IR illumination with defined intensity
switchIROn(IRpower)


# (5) Start experimental protocol
print('Starting protocol...........')

# 	a) test for responses to continous light
#	continuous ON in whole arena for 30s; 60s off (twice)
setRedPower(LEDpowerContinuous)
setPattern(defaultPattern)
for repeat in range(continuousStim['numRepeat']):
	switchRedOn(0,0)
	time.sleep(continuousStim['stimSec'])
	switchRedOff(0,0)
	
	time.sleep(continuousStim['pauseSec'])

print('set 1 "fullfield continuous light" done.............')

# 	b) test for responses to pulsed light
#	1s on, 1s off in whole arena for 60s; then 60s off (twice)
setRedPower(LEDpowerPulsed)
setPattern(defaultPattern)
for repeat in range(pulsedStim['numRepeat']):
	pulseRedLight(pulsedStim['onMSec'],pulsedStim['offMSec'],pulsedStim['stimSec'])
	time.sleep(pulsedStim['pauseSec'])


print('set 2 "fullfield pulsed light" done.............')

# 	c) 4-quadrant assay: continuous for 30s in 2 out of 4 quadrants; switch quadrants (twice)
setRedPower(LEDpowerContinuous)
for repeat in range(quadrantRepeat):
	setPattern(quadrantPatternA)
	pulseRedLight(1000, 0,continuousStim['stimSec'])
	time.sleep(continuousStim['pauseSec'])

	setPattern(quadrantPatternB)
	pulseRedLight(1000, 0,continuousStim['stimSec'])
	time.sleep(continuousStim['pauseSec'])

print('set 3 "quadrant continuous light" done.............')

# 	d) 4-quadrant assay: 1s on, 1s off for 60s in 2 out of 4 quadrants; switch quadrants (twice)
setRedPower(LEDpowerPulsed)
for repeat in range(quadrantRepeat):
	setPattern(quadrantPatternA)
	pulseRedLight(pulsedStim['onMSec'],pulsedStim['offMSec'],pulsedStim['stimSec'])
	time.sleep(pulsedStim['pauseSec'])

	setPattern(quadrantPatternB)
	pulseRedLight(pulsedStim['onMSec'],pulsedStim['offMSec'],pulsedStim['stimSec'])
	time.sleep(pulsedStim['pauseSec'])

print('set 4 "quadrant pulsed light" done.............')

# (6) Terminate session
ser.close()