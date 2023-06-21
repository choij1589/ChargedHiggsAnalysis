#include <iostream>
using namespace std;

const TString ERA = "2018";	
const TString CHANNEL = "Skim3Mu";	// Skim1E2Mu, Skim3Mu
const TString METHOD = "GNNOptim";		// Shape / GNNOptim
const TString SIGNAL = "MHc-100_MA-95";

void drawTemplate() {
    // get root file
	const TString rtpath = ERA+"/"+CHANNEL+"__"+METHOD+"__/"+SIGNAL+"/shapes_input.root";
	TFile *f = new TFile(rtpath, "read");
	
	TH1D *sig = static_cast<TH1D*>(f->Get(SIGNAL));
	TH1D *bkg = static_cast<TH1D*>(f->Get("data_obs"));
	sig->SetStats(0); bkg->SetStats(0);
	sig->SetLineColor(kBlack); sig->SetLineWidth(2);
	bkg->SetLineColor(kRed); bkg->SetLineWidth(2);
	
	// texts
	sig->GetXaxis()->SetTitle("M(#mu^{+}#mu^{-})");
	sig->GetYaxis()->SetTitle("N_{pairs}");

	bkg->GetXaxis()->SetTitle("M(#mu^{+}#mu^{-})");
	bkg->GetYaxis()->SetTitle("N_{pairs}");

	TCanvas *c = new TCanvas("canvas", "", 800, 800);
	TLatex *text = new TLatex();

	c->cd();
	if (sig->GetMaximum() > bkg->GetMaximum()) {
	  sig->GetYaxis()->SetRangeUser(0., sig->GetMaximum()*1.4);
	  sig->Draw("hist");
	  bkg->Draw("same");
	}
	else {
	  bkg->GetYaxis()->SetRangeUser(0., bkg->GetMaximum()*1.4);
	  bkg->Draw();
	  sig->Draw("hist&same");
	}

	// text
	text->SetTextSize(0.04); text->SetTextFont(61);
	text->DrawLatexNDC(0.17, 0.83, "CMS");
	
	text->SetTextSize(0.035); text->SetTextFont(52);
	text->DrawLatexNDC(0.17, 0.78, "Work in progress");

	text->SetTextSize(0.035); text->SetTextFont(42);
	text->DrawLatexNDC(0.7, 0.912, "L_{int} = 59.8 fb^{-1}");
	c->SaveAs("template."+ERA+"."+CHANNEL+"."+METHOD+"."+SIGNAL+".png");

}
