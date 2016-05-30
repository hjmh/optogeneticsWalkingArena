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

serialPortName = '/dev/cu.usbmodem12341'  # 'COM3'

# (1) set protocol specific parameter
preProtocolWait = 10  # in sec

LEDpowerContinuous = 20  # red LED power in percent
LEDpowerPulsed1 = 20  # red LED power in percent
LEDpowerPulsed2 = 20  # red LED power in percent
IRpower = 20  # red LED power in percent

continuousStim = dict([('stimSec', 5),
					   ('pauseSec', 25),
					   ('numRepeat', 2)])
# stimSec and pauseSec are in sec
# onMSec and offMSec are in ms

# Stim1: 2ms at 40 Hz --> on 2ms, off 22 off			   
pulsedPatternStim1 = dict([('stimSec', 50),
						   ('pauseSec', 10),
						   ('onMSec', 2),
						   ('offMSec', 23),
						   ('numRepeat', 3)])

# Stim2: 2ms at 62.5 Hz --> on 2ms, off 14 off
pulsedPatternStim2 = dict([('stimSec', 50),
						   ('pauseSec', 10),
						   ('onMSec', 2),
						   ('offMSec', 14),
						   ('numRepeat', 3)])

defaultPattern = '1111111111111111'
quadrantPatternA = '1100110000110011'
quadrantPatternB = '0011001111001100'

# log parameter to file
experimentName = raw_input("Please enter a name for the exeriment: ")

now = datetime.now()
timeStamp = now.strftime("%Y%m%d-%H%M%S")
protocolFile = 'optogeneticsScreenProtocol_' + experimentName + '_' + timeStamp + '.txt'


def writeDict(dict, fileHandle):
	for i in dict.keys():
		fileHandle.write(' ' + i + ': ' + str(dict[i]) + '\n')


with open(protocolFile, 'a+') as f:
	f.write('Optogenetic Screen Protocol \n \n')
	f.write('LED intensities... \n')
	f.write(' IR:' + str(IRpower) + '\n')
	f.write(' Red (continuous):' + str(LEDpowerContinuous) + '\n')
	f.write(' Red (pulsed 1):' + str(LEDpowerPulsed1) + '\n')
	f.write(' Red (pulsed 2):' + str(LEDpowerPulsed2) + '\n')
	f.write('\nContinuous stimulation parameter... \n')
	writeDict(continuousStim, f)
	f.write('\nPatterned pulsed stimulation parameter (set1)...\n')
	writeDict(pulsedPatternStim1, f)
	f.write('\nPatterned pulsed stimulation parameter (set2)...\n')
	writeDict(pulsedPatternStim2, f)
	f.write('\nPatterns...\n')
	writeDict(patternedStim, f)
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


def switchRedOn(xLED, yLED):
	ser.write('ON ' + ''.join([str(xLED), ', ', str(yLED)]) + '\r')
	# x=0, y=0 turns all LEDs on
	print('ON ' + ''.join([str(xLED), ', ', str(yLED)]) + '\r')


def switchRedOff(xLED, yLED):
	ser.write('OFF ' + ''.join([str(xLED), ', ', str(yLED)]) + '\r')
	# x=0, y=0 turns all LEDs off
	print('OFF ' + ''.join([str(xLED), ', ', str(yLED)]) + '\r')


def pulseRedLight(pulseOnLength, pulseOffLength, pulseStimT):
	ser.write(
		'PULSE, ' + ','.join([str(pulseOnLength), str(pulseOnLength + pulseOffLength), '50000', '0', '0', '1']) + '\r')
	# PULSE width, period, number, off, wait, iterations  - pulse setup command
	print(
		'PULSE, ' + ','.join([str(pulseOnLength), str(pulseOnLength + pulseOffLength), '50000', '0', '0', '1']) + '\r')

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
time.sleep(preProtocolWait)


# (5) Start experimental protocol
print('Starting protocol...........')

# 	a) test for responses to continous light
#	continuous ON in whole arena for X s, then X s off (twice)
setRedPower(LEDpowerContinuous)
setPattern(defaultPattern)
for repeat in range(continuousStim['numRepeat']):
	switchRedOn(0, 0)
	time.sleep(continuousStim['stimSec'])
	switchRedOff(0, 0)

	time.sleep(continuousStim['pauseSec'])

print('set 1 "full-field continuous light" done.............')


# 	b) 4-quadrant assay: pulsed (parameter set 1) for X s in 2 out of 4 quadrants; switch quadrants (twice)
setRedPower(LEDpowerPulsed1)
for repeat in range(pulsedPatternStim1['numRepeat']):
	setPattern(quadrantPatternA)
	pulseRedLight(pulsedPatternStim1['onMSec'], pulsedPatternStim1['offMSec'], pulsedPatternStim1['stimSec'])
	time.sleep(pulsedPatternStim1['pauseSec'])

	setPattern(quadrantPatternB)
	pulseRedLight(pulsedPatternStim1['onMSec'], pulsedPatternStim1['offMSec'], pulsedPatternStim1['stimSec'])
	time.sleep(pulsedPatternStim1['pauseSec'])

print('set 2 "quadrant pulsed light (set 1)" done.............')

# 	c) 4-quadrant assay: pulsed (parameter set 2) for X s in 2 out of 4 quadrants; switch quadrants (twice)
setRedPower(LEDpowerPulsed2)
for repeat in range(pulsedPatternStim2['numRepeat']):
	setPattern(quadrantPatternA)
	pulseRedLight(pulsedPatternStim2['onMSec'], pulsedPatternStim2['offMSec'], pulsedPatternStim2['stimSec'])
	time.sleep(pulsedPatternStim2['pauseSec'])

	setPattern(quadrantPatternB)
	pulseRedLight(pulsedPatternStim2['onMSec'], pulsedPatternStim2['offMSec'], pulsedPatternStim2['stimSec'])
	time.sleep(pulsedPatternStim2['pauseSec'])

print('set 2 "quadrant pulsed light (set 2)" done.............')


# (6) Terminate session
ser.close()
