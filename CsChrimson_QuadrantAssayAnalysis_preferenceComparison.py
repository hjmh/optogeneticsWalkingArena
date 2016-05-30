"""
...
"""

__author__ = 'Hannah Haberkern, hjmhaberkern@gmail.com'

import csv
import os
import sys
from scipy.io import loadmat
import matplotlib.colors as colors
import numpy as np
import seaborn as sns

# import custrom-written modules
from ctraxFlyTracePlots import *
from ctraxQuadrantPlots import *
from protocolParameter import *

# -----------------------------------------------------------------------------------------
# Load protocol parameter
# -----------------------------------------------------------------------------------------
try:
    expListFile = sys.argv[1]
    protocolToAnalyse = sys.argv[2]
    print('Reading in experiment list from ' + expListFile)
    print('Protocol: ' + protocolToAnalyse)
except IndexError:
    print('Please provide exactly two command line arguments:\n' +
          '\t 1) the path to the experiment list file (*.csv)\n' +
          '\t 2) the type of protocol in the experiments to be analysed {v1,v2,v3}')

# load file specifying data to be analysed
fileList = open(expListFile, 'r')
csv_fileList = csv.reader(fileList)

# get header
header = fileList.readline().split(',')

baseDirs = []
genotypes = []
experiments = []
fileNames = []
stimStartFrames = []
protocols = []
LEDintensitiesQuad = []

for line in csv_fileList:
    baseDirs.append(line[0])
    genotypes.append(line[1])
    experiments.append(line[2])
    fileNames.append(line[3])
    stimStartFrames.append(line[4])
    protocols.append(line[5])
    LEDintensitiesQuad.append(line[7])

numFiles = len(experiments)
genotypeSet = list(set(genotypes))
print('Number of experiments to be analysed: ' + str(numFiles))
print('Number of genotypes to be analysed: ' + str(len(genotypeSet)))

# Set up directory for plots
plotSaveDir = baseDirs[0] + '/' + 'fractionFliesInON_plots'
if not os.path.exists(plotSaveDir):
    os.mkdir(plotSaveDir)

# Initialise list that contains average response (= fraction of flies in LED on) per quadrant block per genotype
#averageFractionInON = ... # numGenotypes x array of potentially varying size (dep. on number of quad repeats)

# -----------------------------------------------------------------------------------------
# Iterate over all genotypes
for genotypeID, genotype in enumerate(genotypeSet):
    # -----------------------------------------------------------------------------------------
    # Find all experiments done with this genotype
    fileIDsPerGenotype = []

    for gen in range(len(genotypes)):
        if genotypes[gen] == genotypeSet[genotypeID]:
            fileIDsPerGenotype.append(gen)

    # -----------------------------------------------------------------------------------------
    #find number of quadrant repeats
    protocolParams = loadOptogenProtocolParameter(protocolToAnalyse, 10)
    fps = protocolParams['fps']
    imageSizePx = protocolParams['imageSizePx']
    numRepeatQ1 = protocolParams['numRepeatQ1']
    numRepeatQ2 = protocolParams['numRepeatQ2']
    stimSecQ = protocolParams['stimSecQ']
    pauseSecQ = protocolParams['pauseSecQ']

    numRepeatsQ = [numRepeatQ1, numRepeatQ2]
    numQuadRepeat = 2* max(numRepeatQ1, numRepeatQ2)

    fractionInLEDonPerGenotype = np.zeros((len(fileIDsPerGenotype), numQuadRepeat, stimSecQ))
    #  numFliesPerGenotype x numRepeat x frameRange (= stimSecQ)

    # -------------------------------------------------------------------------------------
    # Define masks (for the moment assume that arena is perfectly centered and
    # that quadrants are squares. Need to read in image frame and extract shapes by using edges.)

    LEDon = np.ones((imageSizePx[0] / 2, imageSizePx[1] / 2))
    LEDoff = np.zeros((imageSizePx[0] / 2, imageSizePx[1] / 2))

    # first stimulation pattern
    patternA = np.hstack((np.vstack((LEDon, LEDoff)), np.vstack((LEDoff, LEDon))))

    # second stimulation pattern
    patternB = np.hstack((np.vstack((LEDoff, LEDon)), np.vstack((LEDon, LEDoff))))

    # -------------------------------------------------------------------------------------
    # Iterate over experiments from a specific genotype
    for idInd, fileIDPerGenotype in enumerate(fileIDsPerGenotype):

        # check if current file needs to be analysed
        if not protocols[fileIDPerGenotype] == protocolToAnalyse:
            print('Experiment list contains data from a different protocol.')
            continue
        else:
            protocol = protocolToAnalyse

        # -------------------------------------------------------------------------------------
        # Set experiment parameter
        baseDir = baseDirs[fileIDPerGenotype]
        experiment = experiments[fileIDPerGenotype]
        fileName = fileNames[fileIDPerGenotype]
        stimStartFrame = int(stimStartFrames[fileIDPerGenotype])
        LEDintensityQuad = LEDintensitiesQuad[fileIDPerGenotype]

        print('\n Analyse data from file: ' + fileName + '\n')

        # -------------------------------------------------------------------------------------
        # load protocol parameter (only need quadrant stimulation related values)
        protocolParams = loadOptogenProtocolParameter(protocol, stimStartFrame)
        stimStartFrameQ1 = protocolParams['stimStartFrameQ1']
        stimStartFrameQ2 = protocolParams['stimStartFrameQ2']
        stimStartFramesQ = [stimStartFrameQ1, stimStartFrameQ2]

        # -------------------------------------------------------------------------------------
        # Import and rearrange data
        try:
            # load existing python file
            npzData = np.load(baseDir + '/' + genotype + '/' + genotype + '_' + experiment + '/' + fileName + '.npz')
            xPos = npzData['xPos']
            yPos = npzData['yPos']
            angle = npzData['angle']
            flyID = npzData['flyID']
            numFrames = len(xPos)
            maxFlyID = npzData['maxFlyID']
        except IOError:
            print('Failed to load data from ' + baseDir + '/' + genotype + '/' + genotype + '_' + experiment + '/'
                  + fileName + '.npz')
            print('Please run basic analysis of files first using e.g. ' +
                  'CsChrimson_QuadrantAssayAnalysis_protocol2-3batch.py')

        # Reorganise fly track fragments into matrix (frame x fly id )
        flyIDperFrame = np.zeros((numFrames, maxFlyID + 1))
        for frame in range(numFrames):
            for idx in np.array(flyID[frame]).squeeze().astype('int'):
                flyIDperFrame[frame][idx] = 1

        # -----------------------------------------------------------------------------------------
        # Compute fraction of flies in illuminated quadrants

        fractionInLEDonPerFly = np.zeros((numQuadRepeat, stimSecQ))
        #           1 (only one stim set per protocol) x numRepeat x frameRange (= stimSecQ)
        for stimSet in range(2):
            numQuadRepeat = 2 * numRepeatsQ[stimSet]
            if numQuadRepeat == 0:
                continue

            for quadrantRepeat in range(numQuadRepeat):
                startFrame = stimStartFramesQ[stimSet] + quadrantRepeat * (stimSecQ + pauseSecQ) * fps
                frameRange = range(startFrame, startFrame + stimSecQ * fps, fps)

                time = np.linspace(0, stimSecQ, len(frameRange))

                fliesInLEDon = np.zeros((len(frameRange), 1))
                fractionInLEDon = np.zeros((len(frameRange), 1))

                if quadrantRepeat % 2 == 0:
                    ONpattern = patternA
                else:
                    ONpattern = patternB

                for ind, frame in enumerate(frameRange):
                    # assemble fly positions for frame
                    spsData = np.ones((len(xPos[frame]), 1)).squeeze()
                    spsColInds = np.array(xPos[frame].astype('int').squeeze())
                    spsRowInds = np.array(yPos[frame].astype('int').squeeze())

                    flyLocations = sps.coo_matrix((spsData, (spsRowInds, spsColInds)),
                                                  shape=(imageSizePx[0], imageSizePx[1])).toarray()

                    # check in wich pattern flies appear
                    fliesInONpattern = (ONpattern + flyLocations) > 1
                    fliesInLEDon[ind] = sum(sum(fliesInONpattern))
                    fractionInLEDon[ind] = sum(sum(fliesInONpattern)) / sum(sum(flyLocations))

                fractionInLEDonPerFly[quadrantRepeat, :] = fractionInLEDon.squeeze()

        fractionInLEDonPerGenotype[idInd, :, :] = fractionInLEDonPerFly

    # New figure for this genotype
    quadFractionFig_singleGenotype = plt.figure(figsize=(11, 3))
    sns.set_style('ticks')
    time = np.linspace(0, stimSecQ, stimSecQ)

    for quadrantRepeat in range(numQuadRepeat):
        subplt = quadFractionFig_singleGenotype.add_subplot(1, numQuadRepeat, quadrantRepeat + 1)
        subplt.plot(time, np.mean(fractionInLEDonPerGenotype[:, quadrantRepeat, :], 0).squeeze(), marker='.',
                    linestyle='none', color='black', alpha=0.75)
        lightONindicator(subplt, 0, 0.5, stimSecQ, 0.5)

        sns.despine(right=True, offset=0)  # trim=True)
        sns.axes_style({'axes.linewidth': 1, 'axes.edgecolor': '.8', })
        subplt.set_title('block ' + str(quadrantRepeat + 1), fontsize = 10)
        subplt.set_ylim((0, 1))

        if quadrantRepeat == 0:
            subplt.set_xlabel('time [s]')
            subplt.set_ylabel('fraction of detected\nflies in "ON-quadrants"')
        else:
            subplt.set_yticks([])
    quadFractionFig_singleGenotype.suptitle('Genotype ' + genotype + ', quadrant protocol ' + protocol
                                            + ', n = ' + str(len(fileIDsPerGenotype)) + '\n', fontsize=14)
    quadFractionFig_singleGenotype.tight_layout()
    quadFractionFig_singleGenotype.savefig(plotSaveDir + '/' + genotype + '_protocol' + protocol + '_fractionInLEDon' + '.pdf', format='pdf')
    plt.close(quadFractionFig_singleGenotype)

    print('Saved fraction of flies in ON quadrants plot')

print('Analysis run successfully')
