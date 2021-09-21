import ast
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages as pdf
import statistics
import os


def readOutput():  # remove when we connect to pose estimation
    file = open("front_on.txt", "r")
    contents = file.read()
    dictionary = ast.literal_eval(contents)
    file.close()
    return dictionary


def parseDictionary(keyword, inputData):  # parses the input dictionary for the left and right data points
    keyword1 = 'L_' + keyword  # corresponding to keyword i.e. knee, ankle, hip
    keyword2 = 'R_' + keyword
    leftDataPoints = inputData[keyword1]
    del leftDataPoints[0]
    rightDataPoints = inputData[keyword2]
    del rightDataPoints[0]
    return leftDataPoints, rightDataPoints


def getDataPoints(data, index):  # gets x or y data points of the dictionary results
    outputPoints = list()
    for n in data:
        if n:
            outputPoints.append(n[index])
    #outputPoints = normaliseData(outputPoints)
    return outputPoints


def normaliseData(data):            # probably take out
    average = statistics.mean(data)
    for i in range(0, len(data)):
        data[i] = data[i] - average
    return data


def addLegends(leftData, rightData, keyword):       # add legend and standard deviation on each plot
    lines = plt.gca().get_lines()
    legend1 = plt.legend()
    leftVar = statistics.stdev(leftData)
    rightVar = statistics.stdev(rightData)
    plt.legend([lines[i] for i in [0, 1]], ['Left ' + keyword + ' Standard Deviation is: ' + "{:.2f}".format(leftVar),
                                            'Right ' + keyword + ' Standard Deviation is: ' + "{:.2f}".format(rightVar)]
               , loc=3)
    plt.gca().add_artist(legend1)


def generateGraphs(leftData, rightData, outputFile, keyword):   # generates the graphs and outputs them to the pdf
    fig = plt.figure(figsize=(12, 12))
    title = keyword + ' Data Points'
    fig.suptitle(title, fontsize=20)
    leftLabel = 'Left ' + keyword
    rightLabel = 'Right ' + keyword

    plt.subplot(2, 1, 1, title='Horizontal Movement')
    lData = getDataPoints(leftData, 0)
    plt.plot(lData, label=leftLabel)
    rData = getDataPoints(rightData, 0)
    plt.plot(rData, label=rightLabel)
    addLegends(lData, rData, keyword)

    plt.subplot(2, 1, 2, title='Vertical Movement')
    lData = getDataPoints(leftData, 1)
    plt.plot(lData, label=leftLabel)
    rData = getDataPoints(rightData, 1)
    plt.plot(rData, label=rightLabel)
    addLegends(lData, rData, keyword)

    outputFile.savefig(fig)


def outputToPDF(keyword, dictionary, outputFile):       # high level function to get data and then generate graphs
    leftData, rightData = parseDictionary(keyword, dictionary)
    generateGraphs(leftData, rightData, outputFile, keyword)


def gaitAnalysis(dictionary):
    outputPDF = pdf('test1.pdf')        # might need to change file path !!!!!!
    outputToPDF('Hip', dictionary, outputPDF)
    outputToPDF('Knee', dictionary, outputPDF)
    outputToPDF('Ankle', dictionary, outputPDF)

    outputPDF.close()
    os.system('test1.pdf')
