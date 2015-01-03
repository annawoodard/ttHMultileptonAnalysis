##########################################
#
#  Configuration script for parsing job 
#  options
#
#  Will read the command line and
#   determine what job configurations
#   are appropriate.
#
#  Main parameters specified by user at CL
#    1. Sample name
#    2. Job label
#    3. (optional) Systematics
#    4. (optional) Job number, default 0
#    5. (optional) Total num jobs, default 1
#    6. (optional) File name (run on this file only)
#
#  Important configurations that don't change often
#  and are written into script
#    1. list directory
#    2. maximum number of events
#    3. a name for this group of jobs
##########################################
import os
import FWCore.ParameterSet.Config as cms
import sys

cmssw_base = os.environ['CMSSW_BASE']
try: #For running with submit_condor_jobs
    thisDir = open(os.path.basename(sys.argv[0]) + '_lists.txt').read().splitlines()[0]
except: #For running without submit_condor_jobs
    thisDir = open(sys.argv[0] + '_lists.txt').read().splitlines()[0]
directoryOfLists = cmssw_base + thisDir
outputBaseDir = "batch_trees/"
maxEvents = -1

# -----------  Define some useful functions
def printHostInfo():
    host = os.environ['HOST']
    thisDir = os.environ['PWD']
    print "CONDOR: running on host ", host, " in directory ", thisDir

def checkDir(inDir):
    if not os.path.exists(inDir):
        try:
            os.mkdir(inDir)
        except OSError, e:    #There is a race condition when jobs check if the directory exists; don't fail if a different job
            if e.errno != 17: #beats you to making the new directory
                raise

def printUsage() :
    print "Usage: ", sys.argv[0], " ssCondor.py  sampleName jobLabel [jetSyst] [jobNum totalJobs]"

def calcBeginEndFileThisJob(totalFiles, totalJobs, thisJob):
    filesPerJob = totalFiles/totalJobs
    firstFile = thisJob * filesPerJob
    lastFile = firstFile
    # if you are the last job, it is your duty to
    # process up until the last file
    if thisJob == totalJobs-1:
        lastFile = totalFiles-1
    else:
        lastFile = firstFile + filesPerJob -1

    return (firstFile, lastFile)

#-----------  Set up cms objects as input
process = cms.Process("ttH2lss")
process.inputs = cms.PSet(
    fileNames = cms.vstring(),
    maxEvents = cms.int32(maxEvents),
	jetSyst = cms.string("dummy")
    )
process.analysis = cms.PSet (
    sampleName = cms.string("dummy")
    )
process.outputs = cms.PSet(
    fileName = cms.string("dummy")
    )

#------------ parse arguments
if len(sys.argv) <= 2 :
    printUsage()
    exit (3)

sampleName = sys.argv[2]
jobLabel   = sys.argv[3]
process.analysis.sampleName = sampleName
sampleList = directoryOfLists + sampleName + ".list"

if len(sys.argv) > 4:
    jetSyst = sys.argv[4]
    if not 'NA' in jetSyst:
        jobLabel = jobLabel+'_'+jetSyst
else:
    jetSyst = 'NA'
process.inputs.jetSyst = jetSyst

if not os.path.exists(sampleList):
    print "Error - can't find list ", sampleList
    exit(4)
else :
    print "CONFIG: the list is ", sampleList

#-----------  read the list and decide what to run on
listFile = open(sampleList, 'r')
linesInFile = listFile.readlines()
numFiles = len(linesInFile)

print "CONFIG: sample name = ", sampleName

jobNum = 0
totalNumJobs = 0
doAllFiles = True

#---------- parse more arguments if they exist
#This would be much more convenient with ArgumentParser, but the c++ executable steals the arguments
if len(sys.argv) >= 7:
    doAllFiles = False
    jobNum = int (sys.argv[5])
    totalNumJobs = int (sys.argv[6])

#---------- figure out what files to add
if not doAllFiles:
    (firstFile, lastFile) = calcBeginEndFileThisJob(numFiles, totalNumJobs, jobNum)
else :
    firstFile = 0
    lastFile = numFiles-1

if len(sys.argv) > 7:
    process.inputs.fileNames.append('file:'+sys.argv[7].strip())
else:
    nLine = 0
    for iLine in linesInFile:
        cleanLine = iLine.strip()
        if (nLine >= firstFile and nLine <= lastFile) or doAllFiles:
            print "CONFIG: Adding file " , cleanLine
            process.inputs.fileNames.append(cleanLine)
        nLine = nLine + 1

print "CONFIG: Input files will be ", process.inputs.fileNames

checkDir(outputBaseDir)

outputDir = outputBaseDir + sampleName + "_" + jobLabel + "/"

checkDir(outputDir)

outputFileName = outputDir + sampleName + "_%s_job%03d.root" % (jobLabel, jobNum)

process.outputs.fileName = outputFileName

print "CONFIG: Output dir = ", outputDir, "\nFile name = ", outputFileName

print "CONFIG: Jet energy systematic = ", process.inputs.jetSyst, "\njetSyst = ", jetSyst
