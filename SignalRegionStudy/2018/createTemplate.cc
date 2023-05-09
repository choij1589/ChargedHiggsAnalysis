#include <iostream>
#include <TString.h>

void createTemplate() {
    const TString MASSPOINT = "MHc-130_MA-90";
    const TString CHANNEL = "Skim3Mu";
    const TString NETWORK = "DenseNet";
    const bool doCut = true;

    TString filePath = "";
    TString outPath = "";
    if (doCut) {
        filePath = CHANNEL+"__"+NETWORK+"__/"+MASSPOINT+"/datacard.input.shape.withcut.root";
        outPath = CHANNEL+"__"+NETWORK+"__/"+MASSPOINT+"/template.withcut.png";
    }
    else {
        filePath = CHANNEL+"__"+NETWORK+"__/"+MASSPOINT+"/datacard.input.shape.nocut.root";
        outPath = CHANNEL+"__"+NETWORK+"__/"+MASSPOINT+"/template.nocut.png";
    }
    
    TFile *f = new TFile(filePath, "read");
    auto *h_sig = (TH1D*)f->Get("signal");
    auto *h_bkg = (TH1D*)f->Get("data_obs");

    h_sig->SetStats(0);
    h_bkg->SetStats(0);
    h_sig->SetLineColor(kBlack);
    h_bkg->SetLineColor(kBlue);
    h_sig->SetLineWidth(2);
    h_bkg->SetLineWidth(2);
    h_sig->Rebin(5);
    h_bkg->Rebin(5);

    TLegend *legend = new TLegend(0.65, 0.6, 0.85, 0.8);
    legend->SetFillStyle(0);
    legend->SetBorderSize(0);
    legend->AddEntry(h_sig, "sig. template", "lep");
    legend->AddEntry(h_bkg, "bkg. template", "lep");

    TLatex *lumi = new TLatex();
    lumi->SetTextSize(0.035); lumi->SetTextFont(42);
    TLatex *cms = new TLatex();
    cms->SetTextSize(0.04); cms->SetTextFont(61);
    TLatex *preliminary = new TLatex();
    preliminary->SetTextSize(0.035); preliminary->SetTextFont(52);

    TCanvas *c = new TCanvas("c", "", 750, 800);
    c->cd();
    
    if (h_sig->GetMaximum() > h_bkg->GetMaximum()) {
        h_sig->GetXaxis()->SetTitle("M(#mu^{+}#mu^{-})");
        h_sig->GetYaxis()->SetTitle("Events");
        h_sig->Draw("hist");
        h_bkg->Draw("hist&same");
    }
    else {
        h_bkg->GetXaxis()->SetTitle("M(#mu^{+}#mu^{-})");
        h_bkg->GetYaxis()->SetTitle("Events");
        h_bkg->Draw("hist");
        h_sig->Draw("hist&same");
    }
    legend->Draw("same");
    lumi->DrawLatexNDC(0.585, 0.91, "L_{int} = 59.8 fb^{-1} (13TeV)");
    cms->DrawLatexNDC(0.17, 0.83, "CMS");
    preliminary->DrawLatexNDC(0.17, 0.78, "Work in progress");
    c->SaveAs(outPath);
    f->Close();
}
