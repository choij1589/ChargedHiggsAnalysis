void createTemplate() {
    TFile *f = new TFile("datacard.input.shape.nocut.root", "read");
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

    TCanvas *c = new TCanvas("c", "");
    c->cd();
    h_bkg->Draw("hist&same");
    h_sig->Draw("hist&same");
    c->SaveAs("template.nocut.png");
    f->Close();
}
