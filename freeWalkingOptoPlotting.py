__author__ = 'hannah'

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.colors as colors
import seaborn as sns


def myAxisTheme(myax):
    myax.get_xaxis().tick_bottom()
    myax.get_yaxis().tick_left()
    myax.spines['top'].set_visible(False)
    myax.spines['right'].set_visible(False)

def plotSparseMatrix(figsize,aspectRatio,matrixToPlot,titleString):
    fig = plt.figure(figsize = figsize)
    fig.set_canvas(plt.gcf().canvas)
    sns.set_style('ticks')
    ax = fig.add_subplot(111)

    ax.spy(matrixToPlot)
    ax.set_aspect(aspectRatio)
    ax.set_title(titleString)

    sns.axes_style({'axes.linewidth': 1, 'axes.edgecolor': '.8'})
    myAxisTheme(ax)

    return fig


def plotPosInRange(ax, frameRange, xPos, yPos, angle, flyID, currCmap):
    cNorm  = colors.Normalize(vmin=-0.5*len(frameRange), vmax=1*len(frameRange))
    scalarMap = plt.cm.ScalarMappable(norm=cNorm, cmap=currCmap)
    colCounter = 0
    for frame in frameRange:
        currCol=scalarMap.to_rgba(len(frameRange)-colCounter)
        colCounter += 1
        ax.plot(xPos[frame], yPos[frame], marker='.', markersize=10, linestyle='none', alpha=0.5,
                color=currCol)

        for fly in flyID[frame]:
            plotBodyAngle(ax, xPos[frame][flyID[frame] == fly], yPos[frame][flyID[frame] == fly],
                          angle[frame][flyID[frame] == fly], currCol, 0.5, 20)

    ax.set_aspect('equal')

    plt.xlim([0, 1000])
    plt.ylim([0, 1000])

    sns.axes_style({'axes.linewidth': 1, 'axes.edgecolor': '.8'})
    myAxisTheme(ax)


def plotBodyAngle(ax, x, y, angle, markerColor, alphaVal, arrowScale):
    try:
        newArrow = patches.Arrow(x, y,np.cos(angle).squeeze()*arrowScale, np.sin(angle).squeeze()*arrowScale, width=2,
                                edgecolor=markerColor, facecolor=markerColor, alpha=alphaVal)
        ax.add_patch(newArrow)
    except:
        couldNotPrint = True
