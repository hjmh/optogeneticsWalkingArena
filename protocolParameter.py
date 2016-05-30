__author__ = 'Hannah Haberkern, hjmhaberkern@gmail.com'

def loadOptogenProtocolParameter(protocolVersion, stimStartFrame):

    if protocolVersion == 'v2':
        #Version 2
        imageSizePx = (1000,1000) #size of the recorded frames in pixel
        fps = 30

        #  Continuous full-field stimulation
        stimSecC = 5
        pauseSecC = 25
        numRepeatC = 2

        # Pulsed Quadrant stimulation (set1 and set2)
        stimSecQ = 50
        pauseSecQ = 10
        numRepeatQ1 = 0 #2 repeats x 2 patterns
        numRepeatQ2 = 3 #2 repeats x 2 patterns

        stimStartFrameC = stimStartFrame
        stimStartFrameQ1 = stimStartFrameC + fps * numRepeatC * (stimSecC + pauseSecC)
        stimStartFrameQ2 = stimStartFrameQ1 + fps * numRepeatQ1 * (stimSecQ + pauseSecQ)


    elif protocolVersion == 'v3':
        #Version 3
        imageSizePx = (1000,1000) #size of the recorded frames in pixel
        fps = 30

        # Pulsed Quadrant stimulation (set1 and set2)
        stimSecQ = 50
        pauseSecQ = 10
        numRepeatQ1 = 0  # 2 repeats x 2 patterns
        numRepeatQ2 = 3  # 2 repeats x 2 patterns

        # Continuous full-field stimulation
        stimSecC = 5
        pauseSecC = 25
        numRepeatC = 2

        stimStartFrameQ1 = stimStartFrame
        stimStartFrameQ2 = stimStartFrameQ1 + fps * numRepeatQ1 * (stimSecQ + pauseSecQ)
        stimStartFrameC = stimStartFrameQ2 + fps * numRepeatQ2 * (stimSecC + pauseSecC)

    return {'fps': fps, 'stimSecC': stimSecC, 'pauseSecC': pauseSecC, 'numRepeatC': numRepeatC, 'stimStartFrameC': stimStartFrameC,
            'stimSecQ': stimSecQ, 'pauseSecQ': pauseSecQ, 'numRepeatQ1': numRepeatQ1, 'numRepeatQ2': numRepeatQ2,
            'stimStartFrameQ1': stimStartFrameQ1, 'stimStartFrameQ2': stimStartFrameQ2, 'imageSizePx': imageSizePx}