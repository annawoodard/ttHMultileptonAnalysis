////////////////////////////////////////////////////////////////
//
//   The purpose of this file is to have all the
//   includes for the kinematic variables
//   in a single location so that every program can easily
//   include them and use them as necessary.
//
////////////////////////////////////////////////////////////////

#include "ttHMultileptonAnalysis/TemplateMakers/interface/KinematicVariable.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/GenericObjectMember.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/GenericCollectionMember.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CSVWeights.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CSVWeightsSF.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/PUWeights.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/TopPtWeights.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/LeptonIDAndIsoScaleFactors.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/LeptonTriggerScaleFactors.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CleanEventVars.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CheckTwoLepTrigger.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CERN/LepMVAs.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/LepGenInfos.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CERN/TightCharges.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/GenericCollectionSizeVariable.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/MetLD.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/DBCorrectedRelIsoDR04s.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/HiggsDecayType.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/TwoObjectKinematic.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CERN/FinalBDT.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CERN/TightChargeAndLepMVAScaleFactors.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CERN/DataDrivenFR.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/BTagWeights.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/BTagShapeWeights.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/PassZmask.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/TwoJetVariables.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_OS_2012.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/GenericVariable.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CERN/RecoIDIsoSIPSFs.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CERN/TightChargeAndLepMVAScaleFactorsPerLepton.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CERN/DataDrivenFRPerLepton.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/ThreeObjectKinematic.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/FourObjectKinematic.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/CERN/FinalBDT_3l.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/MatchTester_ttZ_3l.h"
//#include "ttHMultileptonAnalysis/TemplateMakers/interface/MatchTester_ttZ_3l_GP.h"
//#include "ttHMultileptonAnalysis/TemplateMakers/interface/MatchTesterBDT_ttZ_3l.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/MatchTester_ttW_3l.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/MatchTester_ttbar_fake_3l.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/MatchTester_ttW_SS.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/MatchTester_ttbar_fake_SS.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_ttZ_3l.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_ttW_3l.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_ttW_SS.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_ttZ_3l_Oct31.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_ttW_3l_Oct31.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_ttW_SS_Oct31.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/MatchTester_ttbar_jj.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/KinFitterttHadHad.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/LepCuts.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/TightChargeAndLepCutScaleFactors.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/TightChargeAndLepCutScaleFactorsPerLepton.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/DataDrivenFRLepCut.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/DataDrivenFRLepCutPerLepton.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/MatchTester_ttbar_ll.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_ttZ_vs_ttbar_OS.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_ttZ_vs_zjets_OS.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_ttZ_vs_zjets_ttbar_OS.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_ttZ_vs_ttbar_OS_Oct31.h"
#include "ttHMultileptonAnalysis/TemplateMakers/interface/NOVa/FinalBDT_ttZ_vs_zjets_ttbar_OS_Oct31.h"
