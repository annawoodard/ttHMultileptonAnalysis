#!/usr/bin/env python
import os
import sys
import time
from argparse import ArgumentParser

#------------------- Utility functions -------------
def getNumLinesInFile(fileName):
    theFile = open (fileName, 'r')
    numLines = len(theFile.readlines())
    return numLines

#------------------ Don't fail if directories don't exist ----
def checkCondorDirs() :
    if not os.path.exists("batch_trees"):
        os.mkdir("batch_trees")
    if not os.path.exists("batch_trees/condor_logs"):
        os.mkdir("batch_trees/condor_logs")

def getSampleFromListPath(listFileName):
    dir, listFile = os.path.split(listFileName)
    sampleName, extension = os.path.splitext(listFile)
    return sampleName

#-------------- Get all list files, skipping a few
def getAllListFiles(listDirectory):
    returnList = []

    linesFromDir = os.popen("ls -1 %s*.list | grep -v part" % listDirectory)
    for iLine in linesFromDir:
        cleanLine = iLine.strip()
        returnList.append(cleanLine)
    return returnList

def getSelectedListFiles(listDirectory, executable):
    returnList = []

    linesFromFile = open(executable + '_lists.txt').read().splitlines()[2:]

    for iLine in linesFromFile:
        cleanLine = iLine.strip()
        returnList.append(listDirectory+cleanLine+'.list')
    return returnList

def getListThatMatches(everyList, sample) :
    returnList = None
    for iList in everyList:
        samp = getSampleFromListPath(iList)
        if samp == sample:
            returnList = iList
    if not returnList:
        print "Error, could not find list for sample ", sample
        exit (6)
    return [returnList]

def createCondorSubFileAndSubmit(executable, sample, label, jetSyst, numJobs, wait):
    with open("multiLepBatch.submit", "w") as condorJobFile:
        labelSyst = label
        if not 'NA' in jetSyst:
            labelSyst = label+'_'+jetSyst
        #echo_executable = '/afs/crc.nd.edu/user/a/abrinke1/CMSSW_5_3_8_patch1/src/ttHMultileptonAnalysis/TemplateMakers/test/echo_'+executable.split('/')[-1]
        #print echo_executable
        contents = ('universe = vanilla\n'
                    'List = {list}\n'
                    'executable = {executable}\n'
                    ## Executable to write hostname to log
                    ##'executable = {echo_executable}\n'
                    #'executable = /afs/crc.nd.edu/user/a/abrinke1/CMSSW_5_3_8_patch1/src/ttHMultileptonAnalysis/TemplateMakers/test/echo_lepEff.sh\n'
                    #'executable = /afs/crc.nd.edu/user/a/abrinke1/CMSSW_5_3_8_patch1/src/ttHMultileptonAnalysis/TemplateMakers/test/echo_ttV_OS.sh\n'
                    #'executable = /afs/crc.nd.edu/user/a/abrinke1/CMSSW_5_3_8_patch1/src/ttHMultileptonAnalysis/TemplateMakers/test/echo_ttV.sh\n'
                    #'executable = /afs/crc.nd.edu/user/a/abrinke1/CMSSW_5_3_8_patch1/src/ttHMultileptonAnalysis/TemplateMakers/test/echo_ttV_SS.sh\n'
                    'notification = Never\n'
                    'log = batch_trees/multilepton.logfile\n'
                    'getenv = True\n'
                    'Label = {label}\n'
                    'LabelSyst = {labelSyst}\n'
                    'jetSyst = {jetSyst}\n'
                    'NJobs = {numJobs}\n'
                    'arguments = ssCondor.py $(List) $(Label) $(jetSyst) $(Process) $(NJobs)\n'
                    'output = batch_trees/condor_logs/condor_$(List)_$(LabelSyst)_$(Process).stdout\n'
                    'error = batch_trees/condor_logs/condor_$(List)_$(LabelSyst)_$(Process).stderr\n'
                    ## Requests 2000 MB of memory.  If job exceeds this, it will be killed.
                    'RequestMemory = 2000\n'
#                     ## Runs on 32 cores on earth
#                     '+IsExpressJob = True\n'
#                     ## Excludes some problematic nodes
#                     'requirements = (machine != "d6copt309.crc.nd.edu" && machine != "d6copt353.crc.nd.edu")\n'
#                     'requirements = (machine != "skynet005.crc.nd.edu" && machine != "skynet006.crc.nd.edu" && machine != "skynet008.crc.nd.edu")\n'
                    'queue $(NJobs)')
        condorJobFile.write(contents.format(executable=executable,
                                            list=sample,
                                            label=label,
                                            labelSyst=labelSyst,
                                            jetSyst=jetSyst,
                                            numJobs=numJobs))

    print "Trying to submit jobs..."
    if wait:
        time.sleep(float(wait))
    print os.popen("condor_submit multiLepBatch.submit").readlines()

def main ():
    parser = ArgumentParser(description='Submit tree-making jobs to the condor queue.')
    parser.add_argument('executable', help='Executable to run (ssTwoLep, threeLep, etc)')
    parser.add_argument('project_label', help='Project label.')
    parser.add_argument('-o', '--oneSample', help="Run on only this sample")
    parser.add_argument('-w', '--wait', help='Add a wait time between submitting jobs')
    parser.add_argument('-j', '--jetSyst', help="Jet systematic")
    args = parser.parse_args()

    print 'args.executable: ' + args.executable

    totalJobs = 0
    checkCondorDirs()
    baseDir = os.environ['CMSSW_BASE']
    scramArch = os.environ['SCRAM_ARCH']

    thisDir = open(args.executable + '_lists.txt').read().splitlines()[0] 
    listDir = baseDir + thisDir

    executable = os.path.join(baseDir, 'bin', scramArch, args.executable)

    print "Looking for lists in ", listDir

    listsInDir = getSelectedListFiles(listDir, args.executable)
#     listsInDir = getAllListFiles(listDir)

    if args.oneSample:
        listsToRun = getListThatMatches(listsInDir, args.oneSample)
    else :
        listsToRun = listsInDir

    if args.jetSyst:
        jetSyst = args.jetSyst
    else:
        jetSyst = 'NA'

    print "Running over the following:\n", listsToRun

    for iList in listsToRun:
        sampleName = getSampleFromListPath(iList)
        nJobs = getNumLinesInFile(iList)
#        nJobs = int(nJobs/10)
        print "Calling create with ", executable, " ", sampleName, " ", args.project_label, " ", jetSyst, " ", nJobs
        createCondorSubFileAndSubmit(executable, sampleName, args.project_label, jetSyst, nJobs, args.wait)

    print "Done with loop over samples"

    return

# This allows you to run at the command line
# tells you to call the main function defined above
if __name__ == '__main__':
    main()

