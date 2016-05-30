""" --------------------------------------------------------------------------------------
Screening protocol: repeat for 3 light levels 1%, 5%, 10%

(1) quadrant assay
pulsed light, alternating presentation of 2 patterns, 3 repeats

(2) test of light response
Brief stimulation with continuous light

-------------------------------------------------------------------------------------- """
import time
from datetime import datetime
import serial
import os

import Tkinter as tk

serialPortName = '/dev/cu.usbmodem12341'  # 'COM3'


# (1) set protocol specific parameter
flyListFileLocation = 'gal4LineList.csv'

preProtocolWait = 10  # in sec

LEDpowerQuadrant = 1  # red LED power in percent
LEDpowerContinuous = 1  # red LED power in percent
IRpower = 20  # red LED power in percent


# Quadrant stimulation: 2ms at 62.5 Hz --> on 2ms, off 14 off
quadrantStim = dict([('stimSec', 50),
                     ('pauseSec', 10),
                     ('onMSec', 2),
                     ('offMSec', 14),
                     ('numRepeat', 3)])
#   stimSec and pauseSec are in sec, onMSec and offMSec are in ms

# Continuous stimulation
continuousStim = dict([('stimSec', 5),
                       ('pauseSec', 25)])

defaultPattern = '1111111111111111'
quadrantPatternA = '1100110000110011'
quadrantPatternB = '0011001111001100'


# (2) Set file name
with open(flyListFileLocation) as f:
    lines = f.read().splitlines()

root = tk.Tk()
root.geometry("%dx%d+%d+%d" % (650, 80, 200, 200)) # use width x height + x_offset + y_offset (no spaces!)
root.title("Please select genotype and trial, close window when done.")
varC = tk.StringVar(root)   # chrimson
varG = tk.StringVar(root)   # gal4
varE = tk.StringVar(root)   # trial

# Genotype
varC.set('please select effector line')
choicesC = ['5xCsChr', '10xCsChr', '20xCsChr']
optionC = tk.OptionMenu(root, varC, *choicesC)
optionC.pack(side='left', padx=5, pady=10)

varG.set('please select driver line')
choicesG = lines
optionG = tk.OptionMenu(root, varG, *choicesG)
optionG.pack(side='left', padx=5, pady=10)

# Experiment
varE.set('please select the experiment')
choicesE = ['repeat1', 'repeat2', 'repeat3', 'other']
optionE = tk.OptionMenu(root, varE, *choicesE)
optionE.pack(side='left', padx=5, pady=10)

root.mainloop()

# after window closes...
selectedUAS = varC.get()
selectedGal4 = varG.get()
selectedExperiment = varE.get()

genotype = selectedUAS + '_x_' + selectedGal4
experimentName = genotype + '_' + selectedExperiment

print('Selected:')
print(experimentName)
print('\n')

# log parameter to file

if not os.path.exists(genotype):
    os.mkdir(genotype)

now = datetime.now()
timeStamp = now.strftime("%Y%m%d-%H%M%S")
protocolFile = genotype + '/' + experimentName + '_optogeneticsScreenProtocol_' + timeStamp + '.txt'

def writeDict(dictionary, filehandle):
    for i in dictionary.keys():
        filehandle.write(' ' + i + ': ' + str(dictionary[i]) + '\n')

with open(protocolFile, 'a+') as f:
    f.write('Optogenetic Screen Protocol \n')
    f.write(timeStamp + '\n \n')
    f.write('LED intensities... \n')
    f.write(' IR:' + str(IRpower) + '\n')
    f.write(' Red (continuous):' + str(LEDpowerContinuous) + '\n')
    f.write(' Red (pulsed 1):' + str(LEDpowerQuadrant) + '\n')
    f.write('\nQuadrant stimulation parameter...\n')
    writeDict(quadrantStim, f)
    f.write('\nContinuous stimulation parameter... \n')
    writeDict(continuousStim, f)
    f.write('\nPatterns...\n')
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
except SerialException:
    print('Port was already open.')


# (4) Switch on IR illumination with defined intensity and wait a bit before starting protocol
switchIROn(IRpower)
time.sleep(preProtocolWait)


# (5) Start experimental protocol
print('Starting CsChrimson stimulation protocol...........')

# a) 4-quadrant assay: pulsed for X s in 2 out of 4 quadrants; switch quadrants (numRepeat)
setRedPower(LEDpowerQuadrant)
for repeat in range(quadrantStim['numRepeat']):
    setPattern(quadrantPatternA)
    pulseRedLight(quadrantStim['onMSec'], quadrantStim['offMSec'], quadrantStim['stimSec'])
    time.sleep(quadrantStim['pauseSec'])

    setPattern(quadrantPatternB)
    pulseRedLight(quadrantStim['onMSec'], quadrantStim['offMSec'], quadrantStim['stimSec'])
    time.sleep(quadrantStim['pauseSec'])

print('Quadrant stimulation done.............')

# b) test for responses to continous light
#    continuous ON in whole arena for X s, then X s off
setRedPower(LEDpowerContinuous)
setPattern(defaultPattern)
switchRedOn(0, 0)
time.sleep(continuousStim['stimSec'])
switchRedOff(0, 0)
time.sleep(continuousStim['pauseSec'])

print('Continuous light stimulation done.............')


# (6) Terminate session
ser.close()
print('Protocol terminated successfully.............')
