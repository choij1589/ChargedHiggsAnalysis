#include <iostream>
#include <filesystem>
#include <cmath>
#include <string>
#include <TString.h>
#include <TObjArray.h>
#include <TObjString.h>
#include <TFile.h>
#include <TTree.h>
using namespace ROOT;

void prepareOptimization(const TString ERA, 
                         const TString CHANNEL,
                         const TString NETWORK, 
                         const TString SIGNAL, 
                         const TString SAMPLE, 
                         const bool isSignal, 
                         const bool isFake, 
                         const bool isSS2lOR3l) {
    std::cout << "[prepareOptimization] Preprocessing " << SAMPLE << "..." << std::endl;

    const TString WORKDIR = static_cast<TString>(std::getenv("WORKDIR"));
    TString promptDir = WORKDIR+"/data/PromptUnbinned/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__";
    TString matrixDir = WORKDIR+"/data/MatrixUnbinned/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/DATA";

    double convsf_lowpt3mu, convsf_highpt3mu;
    if (ERA.Contains("2016")) {
        convsf_lowpt3mu = 0.902;
        convsf_highpt3mu = 2.003;
    }
    else if (ERA.Contains("2017")) {
        convsf_lowpt3mu = 0.901;
        convsf_highpt3mu = 1.239;
    }
    else if (ERA.Contains("2018")) {
        convsf_lowpt3mu = 0.628;
        convsf_highpt3mu = 0.981;
    }
    else {
        cerr << "[prepareDataFrame::prepareOptimization] Wrong era " << ERA << endl;
        exit(EXIT_FAILURE);
    }

    // mass of A
    TObjArray *tokens = SIGNAL.Tokenize("_");
    TString Astring = ((TObjString*) tokens->At(1))->GetString();
    tokens = Astring.Tokenize("-");
    TString mAstr = ((TObjString*) tokens->At(1))->GetString();
    double mA = mAstr.Atof();
    const TString outfile = WORKDIR+"/SignalRegionStudy/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/"+SIGNAL+"/"+SAMPLE+".root";
    std::cout << outfile << std::endl;
    TFile *out = new TFile(outfile, "recreate");
    TTree *copyTree = new TTree("Events", "");

    TString filePath;
    if (isSignal)
        filePath = promptDir+"/PromptUnbinned_TTToHcToWAToMuMu_"+SAMPLE+".root";
    else if (isFake)
        filePath = matrixDir+"/MatrixUnbinned_SkimTree_SS2lOR3l_DoubleMuon.root";
    else if (isSS2lOR3l)
        filePath = promptDir+"/PromptUnbinned_SkimTree_SS2lOR3l_"+SAMPLE+".root";
    else
        filePath = promptDir+"/PromptUnbinned_"+SAMPLE+".root";
    // check if file exists
    if (! std::filesystem::exists(static_cast<string>(filePath))) {
        std::cout << "[prepareDataFrame] missing root file " << filePath << std::endl;
        return;
    }
    TFile *f = new TFile(filePath, "read");
    TTree *tree = (TTree*)f->Get("Events");

    float pair1_mass;   tree->SetBranchAddress("Central_mass1", &pair1_mass);
    float pair2_mass;   tree->SetBranchAddress("Central_mass2", &pair2_mass);
    float score_ttFake; tree->SetBranchAddress("Central_score_"+SIGNAL+"_vs_TTLL_powheg", &score_ttFake);
    float score_ttX;    tree->SetBranchAddress("Central_score_"+SIGNAL+"_vs_ttX", &score_ttX);
    float w_nonprompt, w_norm, w_l1prefire, w_pileup;
    float sf_muonID, sf_dblmutrig, sf_btag;

    if (isFake) {
        tree->SetBranchAddress("w_nonprompt", &w_nonprompt);
    }
    else {
        tree->SetBranchAddress("w_norm", &w_norm);
        tree->SetBranchAddress("w_l1prefire", &w_l1prefire);
        tree->SetBranchAddress("w_pileup", &w_pileup);
        tree->SetBranchAddress("Central_sf_muonID", &sf_muonID);
        tree->SetBranchAddress("Central_sf_dblmutrig", &sf_dblmutrig);
        tree->SetBranchAddress("Central_sf_btag_central", &sf_btag);
    }


    float weight; copyTree->Branch("weight", &weight);
    float Amass; copyTree->Branch("Amass", &Amass);
    copyTree->Branch("score_ttFake", &score_ttFake);
    copyTree->Branch("score_ttX", &score_ttX);

    for (unsigned int i = 0; i < tree->GetEntries(); i++) {
        tree->GetEntry(i);
        if (pair1_mass < 0. &&  pair2_mass < 0.) continue;

        Amass = fabs(pair1_mass - mA) < fabs(pair2_mass - mA) ? pair1_mass : pair2_mass;
        if (isFake)
            weight = w_nonprompt;
        else
            weight = w_norm * w_l1prefire * w_pileup * sf_muonID * sf_dblmutrig * sf_btag;
        // conversion sf
        if (SAMPLE.Contains("DYJets")) weight *= convsf_lowpt3mu;
        if (SAMPLE.Contains("ZGToLLG")) weight *= convsf_highpt3mu;
        copyTree->Fill();
    }

    out->cd();
    copyTree->Write();
    f->Close();
    out->Close();
}


