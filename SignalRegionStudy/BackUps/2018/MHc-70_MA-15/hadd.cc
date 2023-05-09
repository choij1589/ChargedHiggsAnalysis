#include <iostream>
using namespace ROOT;

void hadd() {
    const TString SIGNAL = "MHc-70_MA-15";
    const TString suffix = ".shape.withcut.root";
    vector<TString> promptList = {"ttX", "diboson", "others"};
    vector<TString> systematics = {"Central", "MuonIDSF", "DblMuTrigSF", "JetEn"};

    TFile *out = new TFile("datacard_input"+suffix, "recreate");
    TFile *f = nullptr;     // pointer for processed TFiles
    //==== copy signal
    f = new TFile("datacard_input."+SIGNAL+suffix, "read");
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
    f = new TFile("datacard_input.nonprompt"+suffix, "read");
    TH1D *h = static_cast<TH1D*>(f->Get("nonprompt_Central"));
    TH1D *h_copy = static_cast<TH1D*>(h->Clone("nonprompt"));
    TH1D *h_up = static_cast<TH1D*>(f->Get("nonprompt_NonpromptUp"));
    TH1D *h_down = static_cast<TH1D*>(f->Get("nonprompt_NonpromptDown"));
    out->cd();
    h_copy->Write();
    h_up->Write();
    h_down->Write();

    //==== copy conversion
    f = new TFile("datacard_input.conversion"+suffix, "read");
    h = static_cast<TH1D*>(f->Get("conversion_Central"));
    h_copy = static_cast<TH1D*>(h->Clone("conversion"));
    h_up = static_cast<TH1D*>(f->Get("conversion_ConversionUp"));
    h_down = static_cast<TH1D*>(f->Get("conversion_ConversionDown"));
    out->cd();
    h_copy->Write();
    h_up->Write();
    h_down->Write();
    delete h, h_copy, h_up, h_down;

    //==== copy prompt samples
    for (const auto &sampleName: promptList) {
        f = new TFile("datacard_input."+sampleName+suffix, "read");
        for (const auto &syst: systematics) {
            if (syst == "Central") {
                TH1D *h = static_cast<TH1D*>(f->Get(sampleName+"_"+syst));
                TH1D *h_copy = static_cast<TH1D*>(h->Clone(sampleName));
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

    f->Close();
    out->Close();
}   
            
