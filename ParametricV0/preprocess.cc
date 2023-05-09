#include <iostream>
using namespace std;

// data field
const TString SIGNAL = "MHc-70_MA-65";
const TString ERA = "2018";
const TString CHANNEL = "Skim3Mu";
const TString NETWORK = "DenseNet";
const TString DATASTREAM = "DoubleMuon";
const TString METHOD = "method2";

const vector<TString> bkg_VV = {"WZTo3LNu_amcatnlo", "ZZTo4L_powheg"};
const vector<TString> bkg_ttX = {"ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"};
const vector<TString> bkg_conv = {"DYJets", "DYJets10to50_MG", "ZGToLLG"};
const vector<TString> bkg_others = {"WWW", "WWZ", "WZZ", "ZZZ",
                                    "GluGluHToZZTo4L", "VBF_HToZZTo4L",
                                    "tZq", "TTG", "WWG", "TTTT", "tHq"};
const vector<TString> bkg_skimmed = {"WZTo3LNu_amcatnlo", "ZZTo4L_powheg",
                                     "ttWToLNu", "ttZToLLNuNu", "ttHToNonbb",
                                     "DYJets", "DYJets10to50_MG", "ZGToLLG",
                                     "WWW", "WWZ", "WZZ", "ZZZ",
                                     "GluGluHToZZTo4L", "VBF_HToZZTo4L",
                                     "tZq", "TTG"};
const vector<TString> bkg_nskimmed = {"WWG", "TTTT", "tHq"};
const vector<TString> matrixSysts = {"NonpromptUp", "NonpromptDown"};
const vector<TString> convSysts = {"ConversionUp", "ConversionDown"};
const vector<TString> promptSysts = {"L1PrefireUp", "L1PrefireDown",
                                     "PileupReweightUp", "PileupReweightDown",
                                     "MuonIDSFUp", "MuonIDSFDown",
                                     "DblMuTrigSFUp", "DblMuTrigSFDown",
                                     "JetResUp", "JetResDown",
                                     "JetEnUp", "JetEnDown",
                                     "MuonEnUp", "MuonEnDown",
                                     "ElectronEnUp", "ElectronEnDown",
                                     "ElectronResUp", "ElectronResDown"};
double mass, mass1, mass2, scoreX, scoreY, weight;

// function declaration
TFile *getTFile(const TString &sampleName, const bool isPrompt=true, const bool isSkimmed=true);
void fillOutTree(TTree *tree, TTree *outTree, const TString &sampleName, const TString &method, const TString &syst="Central");
double getAmass(const TString &SIGNAL);
double getConvSF(const TString &region, int sys=0);

// main function
void preprocess() {
    const TString baseOutPath = SIGNAL+"/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/"+METHOD+"/";
    gSystem->mkdir(baseOutPath, true);
    gROOT->SetBatch(true);

    // prepare pointers
    TFile *f = nullptr;
    TFile *out = new TFile(baseOutPath+"background.root", "recreate");
    TTree *tree = nullptr;
    TTree *outTree = nullptr;

    // make systematic vector
    vector<TString> systematics = {"Central"};
    for (const auto &syst : matrixSysts) systematics.emplace_back(syst);
    for (const auto &syst : convSysts)   systematics.emplace_back(syst);
    for (const auto &syst : promptSysts) systematics.emplace_back(syst);

    // fill events
    for (const auto &syst: systematics) {
        cout << "@@@@ processing " << syst << "..." << endl;
        if (syst == "Central") outTree = new TTree("Events", "");
        else                   outTree = new TTree("Events_"+syst, "");
        outTree->Branch("mass", &mass);
        outTree->Branch("scoreX", &scoreX);
        outTree->Branch("scoreY", &scoreY);
        outTree->Branch("weight", &weight);
    
        // nonprompt
        f = getTFile("nonprompt", false);
        if (syst.Contains("Nonprompt")) tree = static_cast<TTree*>(f->Get("Events_"+syst));
        else                            tree = static_cast<TTree*>(f->Get("Events_Central"));
        fillOutTree(tree, outTree, "nonprompt", METHOD, syst);
        f->Close();
        
        // prompt
        // conversion variation done in fillOutTree function
        for (const auto &sampleName: bkg_skimmed) {
            f = getTFile(sampleName);
            if (syst.Contains("Nonprompt") || syst.Contains("Conversion")) tree = static_cast<TTree*>(f->Get("Events_Central"));
            else                                                           tree = static_cast<TTree*>(f->Get("Events_"+syst));
            fillOutTree(tree, outTree, sampleName, METHOD, syst);
            f->Close();
        }
        for (const auto &sampleName: bkg_nskimmed) {
            f = getTFile(sampleName, true, false);
            if (syst.Contains("Nonprompt") || syst.Contains("Conversion")) tree = static_cast<TTree*>(f->Get("Events_Central"));
            else                                                           tree = static_cast<TTree*>(f->Get("Events_"+syst));
            fillOutTree(tree, outTree, sampleName, METHOD);
            f->Close();
        }
        out->cd();
        outTree->Write();
    }
    out->Close();
}

TFile *getTFile(const TString &sampleName, const bool isPrompt, const bool isSkimmed) {
    const TString dataPath = "/home/choij/workspace/ChargedHiggsAnalysis/data";
    const TString promptPath = dataPath+"/PromptUnbinned/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__";
    const TString matrixPath = dataPath+"/MatrixUnbinned/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/DATA";

    TString filePath;
    // data
    if (sampleName == DATASTREAM && isPrompt)
        filePath = promptPath+"/DATA/PromptUnbinned_"+DATASTREAM+".root";
    // signal sample
    if (sampleName == SIGNAL)
        filePath = promptPath+"/PromptUnbinned_TTToHcToWAToMuMu_"+SIGNAL+".root";
    // prompt sample
    else if (isPrompt && isSkimmed)
        filePath = promptPath+"/PromptUnbinned_SkimTree_SS2lOR3l_"+sampleName+".root";
    // nonprompt
    else if (! isPrompt)
        filePath = matrixPath+"/MatrixUnbinned_SkimTree_SS2lOR3l_"+DATASTREAM+".root";
    // prompt not skimmed
    else
        filePath = promptPath+"/PromptUnbinned_"+sampleName+".root";

    TFile *out = new TFile(filePath, "read");

    return out;
}

void fillOutTree(TTree *tree, TTree *outTree, const TString &sampleName, const TString &method, const TString &syst) {
    tree->SetBranchAddress("mass1", &mass1);
    tree->SetBranchAddress("mass2", &mass2);
    tree->SetBranchAddress("score_"+SIGNAL+"_vs_ttFake", &scoreX);
    tree->SetBranchAddress("score_"+SIGNAL+"_vs_ttX", &scoreY);
    tree->SetBranchAddress("weight", &weight);
    const double mA = getAmass(SIGNAL);
    // loop
    for (unsigned int entry=0; entry < tree->GetEntries(); entry++) {
        tree->GetEntry(entry);
        // conversion SF for DYJets / ZGToLLG samples
        if (sampleName.Contains("DYJets")) {
            if (syst == "ConversionUp")        weight *= getConvSF("LowPT3Mu", 1);
            else if (syst == "ConversionDown") weight *= getConvSF("LowPT3Mu", -1);
            else                               weight *= getConvSF("LowPT3Mu");
        }
        if (sampleName.Contains("ZGToLLG")) {
            if (syst == "ConversionUp")        weight *= getConvSF("HighPT3Mu", 1);
            else if (syst == "ConversionDown") weight *= getConvSF("HighPT3Mu", -1);
            else                               weight *= getConvSF("HighPT3Mu");
        }

        // fill mass method
        if (method == "method1") {
            mass = fabs(mass1-mA) < fabs(mass2-mA) ? mass1 : mass2;
            outTree->Fill();
        }
        else if (method == "method2") {
            mass = mass1; outTree->Fill();
            mass = mass2; outTree->Fill();
        }
        else {
            cerr << "Wrong method" << endl;
            exit(EXIT_FAILURE);
        }
    }
}


double getAmass(const TString &SIGNAL) {
    TObjArray *tokens = SIGNAL.Tokenize("_");
    TString Astring = ((TObjString*) tokens->At(1))->GetString();
    TString mAstr = ((TObjString*) tokens->At(1))->GetString();
    double mA = mAstr.Atof();
    return mA;
}

double getConvSF(const TString &region, int sys) {
    if (ERA == "2016") {
        if (region == "LowPT3Mu")       {
            double sf = 0.902 + sys*0.890;
            return sf > 0. ? sf : 0.;
        }
        else if (region == "HighPT3Mu") {
            double sf = 2.003 + sys*0.738;
            return sf > 0. ? sf : 0.;
        }
        else { cerr << "Wrong region " << region << endl; exit(EXIT_FAILURE); }
    }
    if (ERA == "2017") {
        if (region == "LowPT3Mu")       {
            double sf = 0.901 + sys*1.303;
            return sf > 0. ? sf : 0.;
        }
        else if (region == "HighPT3Mu") {
            double sf = 1.239 + sys*0.464;
            return sf > 0. ? sf : 0.;
        }
        else { cerr << "Wrong region " << region << endl; exit(EXIT_FAILURE); }
    }
    if (ERA == "2018") {
        if (region == "LowPT3Mu")       {
            double sf = 0.628 + sys*0.522;
            return sf > 0. ? sf : 0.;
        }
        else if (region == "HighPT3Mu") {
            double sf = 0.981 + sys*0.412;
            return sf > 0. ? sf : 0.;
        }
        else { cerr << "Wrong region " << region << endl; exit(EXIT_FAILURE); }
    }
    else {
        cerr << "Wrong era " << ERA << endl;
        exit(EXIT_FAILURE);
    }
}
