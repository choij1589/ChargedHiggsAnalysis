#include <iostream>
#include <TString.h>
#include <TFile.h>
#include <TH1D.h>
using namespace ROOT;

void hadd(const TString ERA,
          const TString CHANNEL,
          const TString SIGNAL, 
          const TString NETWORK,
          const TString suffix) {
    //vector<TString> promptList = {"ttX", "diboson", "others"};
    vector<TString> promptList = {"ttX", "diboson"};
    vector<TString> systematics = {"Central", "MuonIDSF", "DblMuTrigSF", "JetEn", "JetRes"};

    const TString WORKDIR = static_cast<TString>(std::getenv("WORKDIR"));
    const TString basePath = WORKDIR+"/SignalRegionStudy/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/"+SIGNAL;
    const TString outPath = basePath+"/datacard.input"+suffix;
    TFile *out = new TFile(outPath, "recreate");
    TFile *f = nullptr;     // pointer for processed TFiles
    TH1D *data = nullptr;   // pointer for data_obs as sum of all the central estimation of bkgs
    //==== copy signal
    const TString sigPath = basePath+"/datacard.input."+SIGNAL+suffix;
    f = new TFile(sigPath, "read");
    for (const auto &syst : systematics) {
        if (syst == "Central") {
            TH1D *h = static_cast<TH1D*>(f->Get(SIGNAL+"_"+syst));
            TH1D *h_copy = static_cast<TH1D*>(h->Clone("signal"));
            out->cd();
            h_copy->Write();
        }
        else {
            TH1D *h_up = static_cast<TH1D*>(f->Get(SIGNAL+"_"+syst+"Up"));
            TH1D *h_up_copy = static_cast<TH1D*>(h_up->Clone("signal_"+syst+"Up"));
            TH1D *h_down = static_cast<TH1D*>(f->Get(SIGNAL+"_"+syst+"Down"));
            TH1D *h_down_copy = static_cast<TH1D*>(h_down->Clone("signal_"+syst+"Down"));
            out->cd();
            h_up_copy->Write();
            h_down_copy->Write();
        }
    }
    //==== copy nonprompt
    const TString fakePath = basePath+"/datacard.input.nonprompt"+suffix;
    f = new TFile(fakePath, "read");
    TH1D *h = static_cast<TH1D*>(f->Get("nonprompt_Central"));
    TH1D *h_copy = static_cast<TH1D*>(h->Clone("nonprompt"));
    TH1D *h_up = static_cast<TH1D*>(f->Get("nonprompt_NonpromptUp"));
    TH1D *h_down = static_cast<TH1D*>(f->Get("nonprompt_NonpromptDown"));
    data = static_cast<TH1D*>(h->Clone("data_obs"));
    out->cd();
    h_copy->Write();
    h_up->Write();
    h_down->Write();

    //==== copy conversion
    const TString convPath = basePath+"/datacard.input.conversion"+suffix;
    f = new TFile(convPath, "read");
    h = static_cast<TH1D*>(f->Get("conversion_Central"));
    h_copy = static_cast<TH1D*>(h->Clone("conversion"));
    h_up = static_cast<TH1D*>(f->Get("conversion_ConversionUp"));
    h_down = static_cast<TH1D*>(f->Get("conversion_ConversionDown"));
    data->Add(h_copy);
    out->cd();
    h_copy->Write();
    h_up->Write();
    h_down->Write();
    
    delete h, h_copy, h_up, h_down;

    //==== copy prompt samples
    for (const auto &sampleName: promptList) {
        const TString filePath = basePath+"/datacard.input."+sampleName+suffix;
        f = new TFile(filePath, "read");
        for (const auto &syst: systematics) {
            if (syst == "Central") {
                TH1D *h = static_cast<TH1D*>(f->Get(sampleName+"_"+syst));
                TH1D *h_copy = static_cast<TH1D*>(h->Clone(sampleName));
                data->Add(h_copy);
                out->cd();
                h_copy->Write();
            }
            else {
                TH1D *h_up = static_cast<TH1D*>(f->Get(sampleName+"_"+syst+"Up"));
                TH1D *h_up_copy = static_cast<TH1D*>(h_up->Clone(sampleName+"_"+syst+"Up"));
                TH1D *h_down = static_cast<TH1D*>(f->Get(sampleName+"_"+syst+"Down"));
                TH1D *h_down_copy = static_cast<TH1D*>(h_down->Clone(sampleName+"_"+syst+"Down"));
                out->cd();
                h_up_copy->Write();
                h_down_copy->Write();
            }
        }
    }
    out->cd();
    data->Write();
    f->Close();
    out->Close();
}   
