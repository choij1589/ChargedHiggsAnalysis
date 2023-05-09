#include <iostream>
//#include <algorithm>
//using namespace std;

//==== data field
const TString SIGNAL = "MHc-70_MA-65";
const TString ERA = "2018";
const TString CHANNEL = "Skim3Mu";
const TString NETWORK = "DenseNet";
const TString DATASTREAM = "DoubleMuon";
const TString METHOD = "method2";
const vector<TString> promptBkg = {"WZTo3LNu_amcatnlo", "ZZTo4L_powheg",
                                   "ttWToLNu", "ttZToLLNuNu", "ttHToNonbb",
                                   "WWW", "WWZ", "WZZ", "ZZZ",
                                   "GluGluHToZZTo4L", "VBF_HToZZTo4L",
                                   "tZq", "TTG"};
const vector<TString> nonSkimBkg = {"WWG", "TTTT", "tHq"};
const vector<TString> convBkg = {"DYJets", "DYJets10to50_MG", "ZGToLLG"};
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

//==== helper function declaration
TFile *getTFile(const TString &sampleName, const bool isPrompt=true, const bool isSkimmed=true);
double getAmass(const TString &SIGNAL);
TTree *getOutTree(TTree *tree, const TString &sampleName, const TString &method, const TString &syst="Central");
double getConvSF(const TString &region, int sys=0);

//==== main function
void preprocessSingle() {
    const TString baseOutPath = SIGNAL+"/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/"+METHOD+"/";
    gSystem->mkdir(baseOutPath, true);
    gROOT->SetBatch(true);
    
    // prepare pointers
    TFile *f = nullptr;
    TFile *out = nullptr;
    TTree *tree = nullptr;
    TTree *outTree = nullptr;

    // process signal
    cout << "@@@@ processing " << SIGNAL << "..." << endl;
    f = getTFile(SIGNAL);
    out = new TFile(baseOutPath+SIGNAL+".root", "recreate");
    tree = static_cast<TTree*>(f->Get("Events_Central"));
    outTree = getOutTree(tree, SIGNAL, METHOD);
    out->cd();
    outTree->Write();
    for (const auto &syst: promptSysts) {
        tree = static_cast<TTree*>(f->Get("Events_"+syst));
        outTree = getOutTree(tree, SIGNAL, METHOD, syst);
        out->cd();
        outTree->Write();
    }
    f->Close();
    out->Close();

    // process nonpompt
    cout << "@@@@ processing nonprompt..." << endl;
    f = getTFile("nonprompt", false);
    out = new TFile(baseOutPath+"nonprompt.root", "recreate");
    tree = static_cast<TTree*>(f->Get("Events_Central"));
    outTree = getOutTree(tree, "nonprompt", METHOD);
    out->cd();
    outTree->Write();
    for (const auto &syst: matrixSysts) {
        tree = static_cast<TTree*>(f->Get("Events_"+syst));
        outTree = getOutTree(tree, SIGNAL, METHOD, syst);
        out->cd();
        outTree->Write();
    }
    f->Close();
    out->Close();

    // process conversion background
    for (const auto &sampleName: convBkg) {
        cout << "@@@@ processing " << sampleName << "..." << endl;
        f = getTFile(sampleName);
        out = new TFile(baseOutPath+sampleName+".root", "recreate");
        tree = static_cast<TTree*>(f->Get("Events_Central"));
        outTree = getOutTree(tree, sampleName, METHOD);
        out->cd();
        outTree->Write();
        for (const auto &syst: convSysts) {
            tree = static_cast<TTree*>(f->Get("Events_Central"));
            outTree = getOutTree(tree, SIGNAL, METHOD, syst);
            out->cd();
            outTree->Write();
        }
        f->Close();
        out->Close();
    } 
    // process prompts
    for (const auto &sampleName: promptBkg) {
        cout << "@@@@ processing " << sampleName << "..." << endl;
        f = getTFile(sampleName);
        out = new TFile(baseOutPath+sampleName+".root", "recreate");
        tree = static_cast<TTree*>(f->Get("Events_Central"));
        outTree = getOutTree(tree, sampleName, METHOD);
        out->cd();
        outTree->Write();
        for (const auto &syst: promptSysts) {
            tree = static_cast<TTree*>(f->Get("Events_"+syst));
            outTree = getOutTree(tree, SIGNAL, METHOD, syst);
            out->cd();
            outTree->Write();
        }
        f->Close();
        out->Close();
    }
    // process prompts / unskimmed
    for (const auto &sampleName: nonSkimBkg) {
        cout << "@@@@ processing " << sampleName << "..." << endl;
        f = getTFile(sampleName, true, false);
        out = new TFile(baseOutPath+sampleName+".root", "recreate");
        tree = static_cast<TTree*>(f->Get("Events_Central"));
        outTree = getOutTree(tree, sampleName, METHOD);
        out->cd();
        outTree->Write();
        for (const auto &syst: promptSysts) {
            tree = static_cast<TTree*>(f->Get("Events_"+syst));
            outTree = getOutTree(tree, SIGNAL, METHOD, syst);
            out->cd();
            outTree->Write();
        }
        f->Close();
        out->Close();
    }
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

double getAmass(const TString &SIGNAL) { 
    TObjArray *tokens = SIGNAL.Tokenize("_");
    TString Astring = ((TObjString*) tokens->At(1))->GetString();
    TString mAstr = ((TObjString*) tokens->At(1))->GetString();
    double mA = mAstr.Atof();
    return mA;
}

TTree *getOutTree(TTree *tree, const TString &sampleName, const TString &method, const TString &syst) {
    double mass1; tree->SetBranchAddress("mass1", &mass1);
    double mass2; tree->SetBranchAddress("mass2", &mass2);
    double scoreX; tree->SetBranchAddress("score_"+SIGNAL+"_vs_ttFake", &scoreX);
    double scoreY; tree->SetBranchAddress("score_"+SIGNAL+"_vs_ttX", &scoreY);
    double weight; tree->SetBranchAddress("weight", &weight);

    TTree *outTree;
    if (syst == "Central") outTree = new TTree("Events", "");
    else                   outTree = new TTree("Events_"+syst, "");
    double mass; outTree->Branch("mass", &mass);
    outTree->Branch("scoreX", &scoreX);
    outTree->Branch("scoreY", &scoreY);
    outTree->Branch("weight", &weight);
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
    return outTree;
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

