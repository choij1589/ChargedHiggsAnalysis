#include <iostream>
#include <TString.h>
#include <TFile.h>
#include <TTree.h>
#include <TCanvas.h>
#include <RooRealVar.h>
#include <RooDataSet.h>
#include <RooVoigtian.h>
#include <RooPlot.h>
using namespace ROOT;
using namespace RooFit;

vector<RooRealVar> fitAmass(const TString ERA, 
                            const TString CHANNEL,
                            const TString MASSPOINT, 
                            const double MA, const double low, const double high) {
    TFile *f = new TFile("/home/choij/workspace/ChargedHiggsAnalysis/data/PromptUnbinned/"+ERA+"/"+CHANNEL+"__DenseNet__/PromptUnbinned_TTToHcToWAToMuMu_"+MASSPOINT+".root");
    TFile *out = new TFile(ERA+"/"+CHANNEL+"__/"+MASSPOINT+".root", "recreate");
    TTree *tree = (TTree*)f->Get("Events");
    TTree *copy = new TTree("Events", "");

    float pair1_mass; tree->SetBranchAddress("Central_mass1", &pair1_mass);
    float pair2_mass; tree->SetBranchAddress("Central_mass2", &pair2_mass);
    float w_norm; tree->SetBranchAddress("w_norm", &w_norm);
    float w_l1prefire; tree->SetBranchAddress("w_l1prefire", &w_l1prefire);
    float w_pileup; tree->SetBranchAddress("w_pileup", &w_pileup);
    float sf_muonID; tree->SetBranchAddress("Central_sf_muonID", &sf_muonID);
    float sf_dblmutrig; tree->SetBranchAddress("Central_sf_dblmutrig", &sf_dblmutrig);
    float sf_btag; tree->SetBranchAddress("Central_sf_btag_central", &sf_btag);

    float Amass; copy->Branch("Amass", &Amass);
    float weight; copy->Branch("weight", &weight);

    for (unsigned int i = 0; i < tree->GetEntries(); i++) {
        tree->GetEntry(i);
        if (pair1_mass < 0. &&  pair2_mass < 0.) continue;

        Amass = fabs(pair1_mass - MA) < fabs(pair2_mass - MA) ? pair1_mass : pair2_mass;
        weight = w_norm * w_l1prefire * w_pileup * sf_muonID * sf_dblmutrig * sf_btag;
        copy->Fill();
    }
    out->cd();
    copy->Write();

    // load dataset
    RooRealVar mass("Amass", "Amass", low, high);
    RooRealVar w("weight", "weight", 0., 10.);
    RooDataSet ds("ds", "", RooArgSet(mass, w), WeightVar(w), Import(*copy));

    RooRealVar mA("mA", "mA", MA, low, high); 
    //mA.setConstant(true);
    RooRealVar sigma("sigma", "sigma", 0.5, 0., 3.);
    RooRealVar width("width", "width", 0.5, 0., 3.);
    RooVoigtian model("model", "model", mass, mA, width, sigma);
    model.fitTo(ds, SumW2Error(kTRUE));

    TCanvas *c = new TCanvas();
    RooPlot *plot = mass.frame();
    ds.plotOn(plot);
    model.plotOn(plot, LineColor(2));
    plot->Draw();
    c->SaveAs(ERA+"/"+CHANNEL+"__/"+MASSPOINT+".png");
    c->Close();
    f->Close();
    out->Close();
    
    vector<RooRealVar> results;
    results.emplace_back(mA);
    results.emplace_back(sigma);
    results.emplace_back(width);

    return results;
}
