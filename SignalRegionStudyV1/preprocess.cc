#include <iostream>
using namespace std;

//==== Discrimination variables
// 1E2Mu channel - only one dimuon pair for each event
// 3Mu channel - use two OS dimuon pairs
//==== Cut and Count method
// count the number of pairs within mA \pm 3*sigma window
//==== Binned shape method
// make mass templates for mA \pm 5*sigma window with sigma/1.5 binning

// NOTE: Signal cross section scaled to 5 fb

// data field
const TString ERA = "2016postVFP";
const TString CHANNEL = "Skim3Mu";
const TString DATASTREAM = "DoubleMuon";

// signal samples
const vector<TString> SIGNALs = {"MHc-70_MA-15", "MHc-70_MA-40", "MHc-70_MA-65",
                                 "MHc-100_MA-15", "MHc-100_MA-60", "MHc-100_MA-95",
                                 "MHc-130_MA-15", "MHc-130_MA-55", "MHc-130_MA-90", "MHc-130_MA-125",
                                 "MHc-160_MA-15", "MHc-160_MA-85", "MHc-160_MA-120", "MHc-160_MA-155"};
// background samples
const vector<TString> bkg_VV     = {"WZTo3LNu_amcatnlo", "ZZTo4L_powheg"};
const vector<TString> bkg_ttX    = {"ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"};
const vector<TString> bkg_conv   = {"DYJets_MG", "DYJets10to50_MG", "TTG", "WWG"};
const vector<TString> bkg_others = {"WWW", "WWZ", "WZZ", "ZZZ",
                                    "GluGluHToZZTo4L", "VBF_HToZZTo4L",
                                    "tZq", "tHq", "TTTT"};

// systematics
const vector<TString> matrixSysts = {"Central", "NonpromptUp", "NonpromptDown"};
const vector<TString> convSysts   = {"Central", "ConversionUp", "ConversionDown"};
vector<TString> promptSysts = {"Central"};

// tree contents to be store
double mass, mass1, mass2, scoreX, scoreY, scoreZ, weight;

// function declarations
void setSystematics();
TFile *getFile(const TString &sampleName, const bool isPrompt=true, const bool isSignal=false);
void fillOutTree(TTree *tree, TTree *outTree, const TString &sampleName, const TString &signal, 
                 const TString &syst="Central", const bool isTrainedSample=false);
double getAmass(const TString &signal);
double getConvSF(int sys=0);

void setSystematics() {
    if (CHANNEL == "Skim1E2Mu") {
        promptSysts.emplace_back("L1PrefireUp"); promptSysts.emplace_back("L1PrefireDown");
        promptSysts.emplace_back("PileupReweightUp"); promptSysts.emplace_back("PileupReweightDown");
        promptSysts.emplace_back("MuonIDSFUp"); promptSysts.emplace_back("MuonIDSFDown");
        promptSysts.emplace_back("ElectronIDSFUp"); promptSysts.emplace_back("ElectronIDSFDown");
        promptSysts.emplace_back("EMuTrigSFUp"); promptSysts.emplace_back("EMuTrigSFDown");
        promptSysts.emplace_back("ElectronResUp"); promptSysts.emplace_back("ElectronResDown");
        promptSysts.emplace_back("ElectronEnUp"); promptSysts.emplace_back("ElectronEnDown");
        promptSysts.emplace_back("JetResUp"); promptSysts.emplace_back("JetResDown");
        promptSysts.emplace_back("JetEnUp"); promptSysts.emplace_back("JetEnDown");
        promptSysts.emplace_back("MuonEnUp"); promptSysts.emplace_back("MuonEnDown");
    }
    if (CHANNEL == "Skim3Mu") {
        promptSysts.emplace_back("L1PrefireUp"); promptSysts.emplace_back("L1PrefireDown");
        promptSysts.emplace_back("PileupReweightUp"); promptSysts.emplace_back("PileupReweightDown");
        promptSysts.emplace_back("MuonIDSFUp"); promptSysts.emplace_back("MuonIDSFDown");
        promptSysts.emplace_back("DblMuTrigSFUp"); promptSysts.emplace_back("DblMuTrigSFDown");
        promptSysts.emplace_back("ElectronResUp"); promptSysts.emplace_back("ElectronResDown");
        promptSysts.emplace_back("ElectronEnUp"); promptSysts.emplace_back("ElectronEnDown");
        promptSysts.emplace_back("JetResUp"); promptSysts.emplace_back("JetResDown");
        promptSysts.emplace_back("JetEnUp"); promptSysts.emplace_back("JetEnDown");
        promptSysts.emplace_back("MuonEnUp"); promptSysts.emplace_back("MuonEnDown");
    }
}


// main function
void preprocess() {
    gROOT->SetBatch(true);
    setSystematics();
    for (const auto &SIGNAL: SIGNALs) {
        cout << "@@@@ processing " << SIGNAL << "..." << endl;
        const TString baseOutPath = "samples/"+ERA+"/"+CHANNEL+"__/"+SIGNAL+"/";
        gSystem->mkdir(baseOutPath, true);

        // prepare pointers
        TFile *f = nullptr;
        TFile *out = nullptr;
        TTree *tree = nullptr;
        TTree *outTree = nullptr;
        const double mA = getAmass(SIGNAL);
        const bool isTrainedSample = (80 < mA && mA < 100);

        // fill events
        cout << "@@@@ processing signal..." << endl;
        out = new TFile(baseOutPath+SIGNAL+".root", "recreate");
        for (const auto &syst: promptSysts) {
            outTree = new TTree(SIGNAL+"_"+syst, "");
            outTree->Branch("mass", &mass);
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
            outTree->Branch("mass", &mass);
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
            outTree->Branch("mass", &mass);
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
            outTree->Branch("mass", &mass);
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
            outTree->Branch("mass", &mass);
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
            outTree->Branch("mass", &mass);
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
// function definitions
TFile *getFile(const TString &sampleName, const bool isPrompt, const bool isSignal) {
    const TString dataPath = static_cast<TString>(getenv("WORKDIR"))+"/data";
    const TString promptPath = dataPath+"/PromptUnbinned/"+ERA+"/"+CHANNEL+"__";
    const TString matrixPath = dataPath+"/MatrixUnbinned/"+ERA+"/"+CHANNEL+"__/DATA";
    
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
        if (sampleName.Contains("DYJets") || sampleName.Contains("TTG") || sampleName.Contains("WWG")) {
            if (syst == "ConversionUp")        weight *= getConvSF(1);
            else if (syst == "ConversionDown") weight *= getConvSF(-1);
            else                               weight *= getConvSF();
        }

        if (CHANNEL.Contains("1E2Mu")) {
            mass = mass1;
            outTree->Fill();
        }
        else if (CHANNEL.Contains("3Mu")) {
            mass = mass1; outTree->Fill();
            mass = mass2; outTree->Fill();
        }
        else {
            cerr << "Wrong channel " << CHANNEL << endl;
            exit(EXIT_FAILURE);
        }
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

double getConvSF(int sys) {
    if (CHANNEL.Contains("1E2Mu")) {
        if (ERA.Contains("2016preVFP"))       { return 0.851 + sys*0.046; }
        else if (ERA.Contains("2016postVFP")) { return 1.001 + sys*0.054; }
        else if (ERA.Contains("2017"))        { return 0.866 + sys*0.084; }
        else if (ERA.Contains("2018"))        { return 0.810 + sys*0.094; }
        else {
            cerr << "Not implemented yet" << endl;
            exit(EXIT_FAILURE);
        }
    }
    if (CHANNEL.Contains("3Mu")) {
        if (ERA.Contains("2016preVFP"))       { return 0.645 + sys*0.134; }
        else if (ERA.Contains("2016postVFP")) { return 0.604 + sys*0.215; }
        else if (ERA.Contains("2017"))        { return 0.813 + sys*0.234; }
        else if (ERA.Contains("2018"))        { return 0.806 + sys*0.213; }
        else {
            cerr << "Not implemented yet" << endl;
            exit(EXIT_FAILURE);
        }
    }
    return -999.;
}
