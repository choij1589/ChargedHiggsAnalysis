#include <iostream>
using namespace std;

// We have measured the width of the dimuon pair based on 2 order polynomial
// Currently not considering extracting limits for 1E2Mu channel

// Cut and count method
// Using two OS dimuon pairs, count the number of pairs within mA \pm 3*sigma window
// Binned shape method
// Using two OS dimuon pairs, make mass templated for mA \pm 5*sigma window with sigma/2 binning
// before using any method, it is easier to make trees that store needed informations

// data field
const TString ERA = "2018";
const TString CHANNEL = "Skim3Mu";
const TString NETWORK = "GraphNet";     // None, GraphNet
const TString DATASTREAM = "DoubleMuon";

// signal samples

const vector<TString> SIGNALs = {"MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
                                 "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
                                 "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
                                 "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"};

// background samples
const vector<TString> bkg_VV     = {"WZTo3LNu_amcatnlo", "ZZTo4L_powheg"};
const vector<TString> bkg_ttX    = {"ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"};
const vector<TString> bkg_conv   = {"DYJets", "DYJets10to50_MG", "ZGToLLG"};
const vector<TString> bkg_others = {"WWW", "WWZ", "WZZ", "ZZZ",
                                    "GluGluHToZZTo4L", "VBF_HToZZTo4L",
                                    "tZq", "TTG", "WWG", "TTTT", "tHq"};

// systematics
const vector<TString> matrixSysts = {"Central", "NonpromptUp", "NonpromptDown"};
const vector<TString> convSysts   = {"Central", "ConversionUp", "ConversionDown"};
const vector<TString> promptSysts = {"Central",
                                     "L1PrefireUp", "L1PrefireDown",
                                     "PileupReweightUp", "PileupReweightDown",
                                     "MuonIDSFUp", "MuonIDSFDown",
                                     "DblMuTrigSFUp", "DblMuTrigSFDown",
                                     "JetResUp", "JetResDown",
                                     "JetEnUp", "JetEnDown",
                                     "MuonEnUp", "MuonEnDown"};

// global variables to store
double mass1, mass2, scoreX, scoreY, scoreZ, weight;

// function declarations
TFile *getFile(const TString &sampleName, const bool isPrompt=true, const bool isSignal=false);
void fillOutTree(TTree *tree, TTree *outTree, const TString &sampleName, const TString &signal, const TString &syst="Central", const bool isTrainedSample=false);
double getAmass(const TString &signal);
double getConvSF(const TString &region, int sys=0);

// main function
void preprocess() {
    for (const auto &SIGNAL: SIGNALs) {
        cout << "@@@@ processing for " << SIGNAL << "..." << endl;
        const TString baseOutPath = "samples/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/"+SIGNAL+"/";
        gSystem->mkdir(baseOutPath, true);
        gROOT->SetBatch(true);

        // prepare pointers
        TFile *f = nullptr;
        TFile *out = nullptr;
        TTree *tree = nullptr;
        TTree *outTree = nullptr;
        const double mA = getAmass(SIGNAL);
        const bool isTrainedSample = (60 < mA && mA < 125);

        // fill events
        cout << "@@@@ processing signal..." << endl;
        out = new TFile(baseOutPath+SIGNAL+".root", "recreate");
        for (const auto &syst: promptSysts) {
            outTree = new TTree(SIGNAL+"_"+syst, "");
            outTree->Branch("mass1", &mass1);
            outTree->Branch("mass2", &mass2);
            if (isTrainedSample) {
                outTree->Branch("scoreX", &scoreX);
                outTree->Branch("scoreY", &scoreY);
                outTree->Branch("scoreZ", &scoreZ);
            }
            outTree->Branch("weight", &weight);

            f = getFile(SIGNAL, true, true);
            tree = static_cast<TTree*>(f->Get("Events_"+syst));
            fillOutTree(tree, outTree, SIGNAL, SIGNAL, syst, isTrainedSample);
            f->Close();

            out->cd();
            outTree->Write();
        }
        out->Close();

        // nonprompt
        cout << "@@@@ processing nonprompt..." << endl;
        out = new TFile(baseOutPath+"nonprompt.root", "recreate");
        for (const auto &syst: matrixSysts) {
            outTree = new TTree("nonprompt_"+syst, "");
            outTree->Branch("mass1", &mass1);
            outTree->Branch("mass2", &mass2);
            if (isTrainedSample) {
                outTree->Branch("scoreX", &scoreX);
                outTree->Branch("scoreY", &scoreY);
                outTree->Branch("scoreZ", &scoreZ);
            }
            outTree->Branch("weight", &weight);

            f = getFile("nonprompt", false);
            tree = static_cast<TTree*>(f->Get("Events_"+syst));
            fillOutTree(tree, outTree, "nonprompt", SIGNAL, syst, isTrainedSample);
            out->cd();
            outTree->Write();
        }
        out->Close();

        // conversion
        cout << "@@@@ processing conversion..." << endl;
        out = new TFile(baseOutPath+"conversion.root", "recreate");
        for (const auto &syst: convSysts) {
            outTree = new TTree("conversion_"+syst, "");
            outTree->Branch("mass1", &mass1);
            outTree->Branch("mass2", &mass2);
            if (isTrainedSample) {
                outTree->Branch("scoreX", &scoreX);
                outTree->Branch("scoreY", &scoreY);
                outTree->Branch("scoreZ", &scoreZ);
            }
            outTree->Branch("weight", &weight);

            for (const auto &sampleName: bkg_conv) {
                f = getFile(sampleName);
                tree = static_cast<TTree*>(f->Get("Events_Central"));
                fillOutTree(tree, outTree, sampleName, SIGNAL, syst, isTrainedSample);
                f->Close();
            }
            out->cd();
            outTree->Write();
        }
        out->Close();

        // VV
        cout << "@@@@ processing diboson..." << endl;
        out = new TFile(baseOutPath+"diboson.root", "recreate");
        for (const auto &syst: promptSysts) {
            outTree = new TTree("diboson_"+syst, "");
            outTree->Branch("mass1", &mass1);
            outTree->Branch("mass2", &mass2);
            if (isTrainedSample) {
                outTree->Branch("scoreX", &scoreX);
                outTree->Branch("scoreY", &scoreY);
                outTree->Branch("scoreZ", &scoreZ);
            }
            outTree->Branch("weight", &weight); 

            for (const auto &sampleName: bkg_VV) {
                f = getFile(sampleName);
                tree = static_cast<TTree*>(f->Get("Events_"+syst));
                fillOutTree(tree, outTree, sampleName, SIGNAL, syst, isTrainedSample);
                f->Close();
            }
            out->cd();
            outTree->Write();
        }
        out->Close();

        // ttX
        cout << "@@@@ processing ttX..." << endl;
        out = new TFile(baseOutPath+"ttX.root", "recreate");
        for (const auto &syst: promptSysts) {
            outTree = new TTree("ttX_"+syst, "");
            outTree->Branch("mass1", &mass1);
            outTree->Branch("mass2", &mass2);
            if (isTrainedSample) {
                outTree->Branch("scoreX", &scoreX);
                outTree->Branch("scoreY", &scoreY);
                outTree->Branch("scoreZ", &scoreZ);
            }
            outTree->Branch("weight", &weight);

            for (const auto &sampleName: bkg_ttX) {
                f = getFile(sampleName);
                tree = static_cast<TTree*>(f->Get("Events_"+syst));
                fillOutTree(tree, outTree, sampleName, SIGNAL, syst, isTrainedSample);
                f->Close();
            }
            out->cd();
            outTree->Write();
        }
        out->Close();

        // others
        cout << "@@@@ processing others..." << endl;
        out = new TFile(baseOutPath+"others.root", "recreate");
        for (const auto &syst: promptSysts) {
            outTree = new TTree("others_"+syst, "");
            outTree->Branch("mass1", &mass1);
            outTree->Branch("mass2", &mass2);
            if (isTrainedSample) {
                outTree->Branch("scoreX", &scoreX);
                outTree->Branch("scoreY", &scoreY);
                outTree->Branch("scoreZ", &scoreZ);
            }
            outTree->Branch("weight", &weight);

            for (const auto &sampleName: bkg_others) {
                f = getFile(sampleName);
                tree = static_cast<TTree*>(f->Get("Events_"+syst));
                fillOutTree(tree, outTree, sampleName, SIGNAL, syst, isTrainedSample);
                f->Close();
            }
            out->cd();
            outTree->Write();
        }
        out->Close();
    }
}

// function definitions
TFile *getFile(const TString &sampleName, const bool isPrompt, const bool isSignal) {
    const TString dataPath = static_cast<TString>(getenv("WORKDIR"))+"/data";
    TString promptPath, matrixPath;
    if (NETWORK.Contains("Net")) {
        promptPath = dataPath+"/PromptUnbinned/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__";
        matrixPath = dataPath+"/MatrixUnbinned/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/DATA";
    }
    else {
        promptPath = dataPath+"/PromptUnbinned/"+ERA+"/"+CHANNEL+"__DenseNet__";
        matrixPath = dataPath+"/MatrixUnbinned/"+ERA+"/"+CHANNEL+"__DenseNet__/DATA";
    }
    TString filePath;
    // data
    if (sampleName == DATASTREAM && isPrompt)
        filePath = promptPath+"/DATA/PromptUnbinned_"+DATASTREAM+".root";
    // signal sample
    else if (isSignal)
        filePath = promptPath+"/PromptUnbinned_TTToHcToWAToMuMu_"+sampleName+".root";
    // prompt sample
    else if (isPrompt)
        filePath = promptPath+"/PromptUnbinned_SkimTree_SS2lOR3l_"+sampleName+".root";
    // nonprompt sample
    else if (!isPrompt)
        filePath = matrixPath+"/MatrixUnbinned_SkimTree_SS2lOR3l_"+DATASTREAM+".root";
    else
        cerr << "[WARNING] No category for " << sampleName << endl;

    TFile *out = new TFile(filePath, "read");

    return out;
}

void fillOutTree(TTree *tree, TTree *outTree, const TString &sampleName, const TString &signal, const TString &syst, const bool isTrainedSample) {
    tree->SetBranchAddress("mass1", &mass1);
    tree->SetBranchAddress("mass2", &mass2);
    if (isTrainedSample) {
        tree->SetBranchAddress("score_"+signal+"_vs_nonprompt", &scoreX);
        tree->SetBranchAddress("score_"+signal+"_vs_diboson", &scoreY);
        tree->SetBranchAddress("score_"+signal+"_vs_ttZ", &scoreZ);
    }
    tree->SetBranchAddress("weight", &weight);

    // loop
    for (unsigned int entry=0; entry < tree->GetEntries(); entry++) {
        tree->GetEntry(entry);
        // signal xsec scaled to be 5 fb
        if (sampleName.Contains("MA"))         weight /= 3.;

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
        outTree->Fill();
    }
}

double getAmass(const TString &signal) {
    TObjArray *tokens = signal.Tokenize("_");
    TString Astring = ((TObjString*) tokens->At(1))->GetString();
    tokens = Astring.Tokenize("-");
    TString mAstr = ((TObjString*) tokens->At(1))->GetString();
    double mA = mAstr.Atof();
    return mA;
}

double getConvSF(const TString &region, int sys) {
    if (ERA.Contains("2016")) {
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
