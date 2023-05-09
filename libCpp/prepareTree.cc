#include <iostream>
#include <vector>
#include <map>
#include <TString.h>
#include <TFile.h>
#include <TTree.h>
using namespace ROOT;

TTree* prepareDataset(const TString filepath, const TString sample, const double MA, const TString syst) {
    std::cout << "[prepareDataset] Processing " << filepath << "..." << std::endl;

    TFile *f = new TFile(filepath, "read");
    
    TString prefix;
    if (syst.Contains("Jet")) prefix = syst;
    else                      prefix = "Central";

    TTree *tree = static_cast<TTree*>(f->Get("Events"));
    TTree *copy = new TTree("Events_"+syst, "");

    float pair1_mass; tree->SetBranchAddress(prefix+"_mass1", &pair1_mass);
    float pair2_mass; tree->SetBranchAddress(prefix+"_mass2", &pair2_mass);
    float w_nonprompt, w_norm, w_l1prefire, w_pileup;
    float sf_muonID, sf_dblmutrig, sf_btag;

    if (sample == "nonprompt") {
        if (syst.Contains("Up"))        tree->SetBranchAddress("w_nonprompt_up", &w_nonprompt);
        else if (syst.Contains("Down")) tree->SetBranchAddress("w_nonprompt_down", &w_nonprompt);
        else                            tree->SetBranchAddress("w_nonprompt", &w_nonprompt);
    }
    else {
        tree->SetBranchAddress("w_norm", &w_norm);
        tree->SetBranchAddress("w_l1prefire", &w_l1prefire);
        tree->SetBranchAddress("w_pileup", &w_pileup);
        if (syst == "MuonIDSFUp")        tree->SetBranchAddress(prefix+"_sf_muonID_up", &sf_muonID);
        else if (syst == "MuonIDSFDown") tree->SetBranchAddress(prefix+"_sf_muonID_down", &sf_muonID);
        else                             tree->SetBranchAddress(prefix+"_sf_muonID", &sf_muonID);

        if (syst == "DblMuTrigSFUp")        tree->SetBranchAddress(prefix+"_sf_dblmutrig_up", &sf_dblmutrig);
        else if (syst == "DblMuTrigSFDown") tree->SetBranchAddress(prefix+"_sf_dblmutrig_down", &sf_dblmutrig);
        else                                tree->SetBranchAddress(prefix+"_sf_dblmutrig", &sf_dblmutrig);

        tree->SetBranchAddress(prefix+"_sf_btag_central", &sf_btag);
    }

    float Amass; copy->Branch("Amass", &Amass);
    float weight; copy->Branch("weight", &weight);
    
    for (unsigned int i = 0; i < tree->GetEntries(); i++) {
        tree->GetEntry(i);
        if (pair1_mass < 0. &&  pair2_mass < 0.) continue;

        Amass = fabs(pair1_mass - MA) < fabs(pair2_mass - MA) ? pair1_mass : pair2_mass;
        if (sample == "nonprompt")
            weight = w_nonprompt;
        else
            weight = w_norm * w_l1prefire * w_pileup * sf_muonID * sf_dblmutrig * sf_btag;
        
        copy->Fill();
    }
    copy->SetDirectory(0);
    return copy;
}

    
