#include <iostream>
#include <vector>
#include <map>
#include <TString.h>
#include <TFile.h>
#include <TH1D.h>
#include <TLegend.h>
#include <TLegendEntry.h>
#include <TCanvas.h>
#include <RooRealVar.h>
#include <RooDataHist.h>
#include <RooHistPdf.h>
#include <RooAddPdf.h>
#include <RooPlot.h>
#include <RooFitResult.h>
#include <RooArgList.h>
using namespace RooFit;

RooFitResult* fitMT(const TString ERA, const TString HLT, const TString ID, const TString SYST) {
//void doFit() {
    // settings
    //const TString ERA  = "2016preVFP";
    //const TString HLT  = "MeasFakeEl23";
    //const TString ID   = "tight";
    //const TString SYST = "Central";
    
    TString DATASTREAM = "";
    if (HLT.Contains("Mu")) DATASTREAM = "DoubleMuon";
    if (HLT.Contains("El") && ERA.Contains("2016")) DATASTREAM = "DoubleEG";
    if (HLT.Contains("El") && ERA.Contains("2017")) DATASTREAM = "SingleElectron";
    if (HLT.Contains("El") && ERA.Contains("2018")) DATASTREAM = "EGamma";

    const vector<TString> QCD = {"QCD_Pt_15to30", "QCD_Pt_30to50", "QCD_Pt_50to80", "QCD_Pt_80to120", "QCD_Pt_120to170",
                                 "QCD_Pt_170to300", "QCD_Pt_300to470", "QCD_Pt_470to600", "QCD_Pt_600to800",
                                 "QCD_Pt_800to1000", "QCD_Pt_1000to1400", "QCD_Pt_1400to1800", "QCD_Pt_1800to2400",
                                 "QCD_Pt_2400to3200", "QCD_Pt_3200toInf"};
    const vector<TString> W   = {"WJets_MG"};
    const vector<TString> DY  = {"DYJets", "DYJets10to50_MG"};
    //const vector<TString> TT  = {"TTLL_powheg", "TTLJ_powheg"};
    const vector<TString> TT  = {"TTLL_powheg"};
    const vector<TString> VV  = {"WW_pythia", "WZ_pythia", "ZZ_pythia"};
    const vector<TString> ST  = {"SingleTop_sch_Lep", "SingleTop_tch_top_Incl", "SingleTop_tch_antitop_Incl",
                                "SingleTop_tW_top_NoFullyHad", "SingleTop_tW_antitop_NoFullyHad"};

    vector<TString> PROMPTs = W;
    for (const auto &sample: DY) PROMPTs.emplace_back(sample);
    for (const auto &sample: TT) PROMPTs.emplace_back(sample);
    for (const auto &sample: VV) PROMPTs.emplace_back(sample);
    for (const auto &sample: ST) PROMPTs.emplace_back(sample);

    vector<TString> MCSamples = PROMPTs;
    for (const auto &sample: QCD) MCSamples.emplace_back(sample);

    const vector<TString> KEYs = {"QCD", "W", "DY", "TT", "ST", "VV"};
    const TString histkey_central = "Inclusive/"+ID+"/Central/MTfix";
    const TString histkey = "Inclusive/"+ID+"/"+SYST+"/MTfix";

    // construct templates
    map<TString, TH1D*> HISTs;
    map<TString, RooHistPdf*> TEMPLATEs;
    map<TString, double> SCALEs;
    map<TString, RooRealVar*> COEFs;
    RooRealVar MT("MT", "MT", 0., 300.);
    
    TFile *f = nullptr;
    // data
    f = new TFile("../data/MeasFakeRateV3/"+ERA+"/"+HLT+"__/DATA/MeasFakeRateV3_"+DATASTREAM+".root");
    TH1D *h_data = (TH1D*)f->Get(histkey_central); h_data->SetDirectory(0); f->Close();
    RooDataHist *data = new RooDataHist("dh_"+DATASTREAM, "", MT, Import(*h_data));

    // prefit - get normalized scale to data
    //double sumMC = 0.;
    //for (const auto &sample: PROMPTs) {
    //    f = new TFile("../data/MeasFakeRateV3/"+ERA+"/"+HLT+"__RunSyst__/MeasFakeRateV3_"+sample+".root");
    //    TH1D *h = (TH1D*)f->Get(histkey); h->SetDirectory(0); f->Close();
    //    sumMC += h->Integral();
    //}
    //double prescale = h_data->Integral() / sumMC;
    //cout << "prefit scale = " << prescale << endl;

    // make mc templates
    for (const auto &sample: QCD) {
        f = new TFile("../data/MeasFakeRateV3/"+ERA+"/"+HLT+"__RunSyst__/MeasFakeRateV3_"+sample+".root");
        //std::cout << sample << std::endl;
        TH1D *h = dynamic_cast<TH1D*>(f->Get(histkey)); 
        if (h) {
            h->SetDirectory(0);
            //h->Scale(prescale);
            map<TString, TH1D*>::iterator it = HISTs.find("QCD");
            if (it == HISTs.end()) HISTs["QCD"] = (TH1D*)h->Clone("h_QCD");
            else                   HISTs["QCD"]->Add(h);
        }
        else {
            std::cout << "no MT distribution for " << sample << std::endl;
        }
        f->Close();
    }
    
    for (const auto &sample: W) {
        f = new TFile("../data/MeasFakeRateV3/"+ERA+"/"+HLT+"__RunSyst__/MeasFakeRateV3_"+sample+".root");
        TH1D *h = (TH1D*)f->Get(histkey); h->SetDirectory(0); f->Close();
        //h->Scale(prescale);
        map<TString, TH1D*>::iterator it = HISTs.find("W");
        if (it == HISTs.end()) HISTs["W"] = (TH1D*) h->Clone("h_W");
        else                   HISTs["W"]->Add(h);
    }
    for (const auto &sample: DY) {
        f = new TFile("../data/MeasFakeRateV3/"+ERA+"/"+HLT+"__RunSyst__/MeasFakeRateV3_"+sample+".root");
        TH1D *h = (TH1D*)f->Get(histkey); h->SetDirectory(0); f->Close();
        //h->Scale(prescale);
        map<TString, TH1D*>::iterator it = HISTs.find("DY");
        if (it == HISTs.end()) HISTs["DY"] = (TH1D*)h->Clone("h_DY");
        else                   HISTs["DY"]->Add(h);
    }
    for (const auto &sample: TT) {
        f = new TFile("../data/MeasFakeRateV3/"+ERA+"/"+HLT+"__RunSyst__/MeasFakeRateV3_"+sample+".root");
        TH1D *h = (TH1D*)f->Get(histkey); h->SetDirectory(0); f->Close();
        //h->Scale(prescale);
        map<TString, TH1D*>::iterator it = HISTs.find("TT");
        if (it == HISTs.end()) HISTs["TT"] = (TH1D*)h->Clone("h_TT");
        else                   HISTs["TT"]->Add(h);
    }
    for (const auto &sample: ST) {
        f = new TFile("../data/MeasFakeRateV3/"+ERA+"/"+HLT+"__RunSyst__/MeasFakeRateV3_"+sample+".root");
        TH1D *h = (TH1D*)f->Get(histkey); h->SetDirectory(0); f->Close();
        //h->Scale(prescale);
        map<TString, TH1D*>::iterator it = HISTs.find("ST");
        if (it == HISTs.end()) HISTs["ST"] = (TH1D*)h->Clone("h_ST");
        else                   HISTs["ST"]->Add(h);
    }
    for (const auto &sample: VV) {
        f = new TFile("../data/MeasFakeRateV3/"+ERA+"/"+HLT+"__RunSyst__/MeasFakeRateV3_"+sample+".root");
        TH1D *h = (TH1D*)f->Get(histkey); h->SetDirectory(0); f->Close();
        //h->Scale(prescale);
        map<TString, TH1D*>::iterator it = HISTs.find("VV");
        if (it == HISTs.end()) HISTs["VV"] = (TH1D*)h->Clone("h_VV");
        else                   HISTs["VV"]->Add(h);
    }


    double scale = 0.;
    for (const auto &key: KEYs) {
        TH1D *h = HISTs[key];
        RooDataHist *dh = new RooDataHist("dh_"+key, "", MT, Import(*h));
        RooHistPdf *pdf = new RooHistPdf("template_"+key, "", MT, *dh, 0);
        TEMPLATEs[key] = pdf;
        scale += h->Integral();
    }

    for (const auto &key : KEYs) {
        TH1D *h = HISTs[key];
        SCALEs[key] = h->Integral() / scale;
    }

    // Make coefficients
    for (const auto &key: KEYs) {
        RooRealVar *coef;
        if (key.Contains("QCD")) coef = new RooRealVar("coef_"+key, "", SCALEs[key], 0., 1.);
        else                     coef = new RooRealVar("coef_"+key, "", SCALEs[key], SCALEs[key]*0.6, SCALEs[key]*1.4);
        COEFs[key] = coef;
    }

    // Make model
    RooAddPdf *model;
    model = new RooAddPdf("model", "", 
                    RooArgList(*TEMPLATEs["W"], *TEMPLATEs["DY"], *TEMPLATEs["TT"], *TEMPLATEs["ST"], *TEMPLATEs["VV"], *TEMPLATEs["QCD"]),
                    RooArgList(*COEFs["W"], *COEFs["DY"], *COEFs["TT"], *COEFs["ST"], *COEFs["VV"]), kFALSE);

    RooFitResult *fitResult = model->fitTo(*data, Save(), PrintLevel(-1));
    RooPlot *frame = MT.frame();
    data->plotOn(frame, Name("data"));
    model->plotOn(frame, Name("MC"));
    model->plotOn(frame, Name("QCD"), Components("template_QCD"), LineColor(kBlack), LineStyle(kDashed));
    model->plotOn(frame, Name("DY"), Components("template_DY"), LineColor(kRed), LineStyle(kDashed));
    model->plotOn(frame, Name("W"), Components("template_W"), LineColor(kBlue), LineStyle(kDashed));
    model->plotOn(frame, Name("TT"), Components("template_TT"), LineColor(kViolet), LineStyle(kDashed));
    model->plotOn(frame, Name("ST"), Components("template_ST"), LineColor(kAzure), LineStyle(kDashed));
    model->plotOn(frame, Name("VV"), Components("template_VV"), LineColor(kOrange), LineStyle(kDashed));

    TCanvas *cvs = new TCanvas("cvs", "", 800, 600);
    TLegend *legend = new TLegend(0.6, 0.6, 0.85, 0.85);
    legend->SetBorderSize(0);
    legend->AddEntry("data", "data", "p");
    //legend->AddEntry("postfit", "postfit", "l");
    legend->AddEntry("QCD", "QCD", "l");
    //legend->AddEntry("DY", "DY", "l");
    //legend->AddEntry("W", "W", "l");
    //legend->AddEntry("TT", "TT", "l");
    //legend->AddEntry("ST", "ST", "l");
    //legend->AddEntry("VV", "VV", "l");

    cvs->cd();
    frame->Draw();
    legend->Draw();
    cvs->SaveAs("results/"+ERA+"/plots/"+HLT+"_"+ID+"_"+SYST+".png");
    return fitResult;

    //RooArgList coefList = fitResult->floatParsFinal();
    //coefList.Print("v");
}
