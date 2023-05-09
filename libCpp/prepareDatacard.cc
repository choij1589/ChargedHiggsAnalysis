#include <iostream>
#include <map>
#include <vector>
#include <TFile.h>
#include <TTree.h>
#include <TH1D.h>
#include <TString.h>
#include <TObjArray.h>
#include <TObjString.h>
using namespace ROOT;

//==== C++ functions for the preparation of inputs for datacards
//==== Argument explanation:
//==== SIGNAL: datacard is signal mass hypothesis dependent (mass window, scores)
//==== systType: set of samples - group with the samples that share the same systematics
//==== cardType: CNC or shape / NOTE: CNC is not supported yet

map<TString, vector<TString>> map_sample = {
        {"nonprompt", {"nonprompt"}},
        {"diboson", {"WZTo3LNu_amcatnlo","ZZTo4L_powheg"}},
        {"conversion", {"DYJets", "DYJets10to50_MG", "ZGToLLG"}},
        {"ttX", {"ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"}},
        {"others", {"WWW", "WWZ", "WZZ", "ZZZ", "TTG", "tZq", "tHq", "TTTT", "VBF_HToZZTo4L", "GluGluHToZZTo4L"}}
};


map<TString, vector<TString>> map_systematics = {
        {"prompt", {"Central", "MuonIDSFUp", "MuonIDSFDown", "DblMuTrigSFUp", "DblMuTrigSFDown",
                               "JetEnUp", "JetEnDown", "JetResUp", "JetResDown"}},
        {"nonprompt", {"Central", "NonpromptUp", "NonpromptDown"}},
        {"conversion", {"Central", "ConversionUp", "ConversionDown"}}
};

// function declarations
TH1D* makeHisto1D(const TString ERA,
                  const TString CHANNEL,
                  const TString SIGNAL,
                  const TString NETWORK,
                  const TString sampleKey,
                  const pair<double, double> score,
                  const pair<double, double> convsf_lowpt,
                  const pair<double, double> convsf_highpt,
                  const TString syst);

TH1D* makeHisto1DSingle(const TString filePath,
                        const TString SIGNAL,
                        const TString sampleName,
                        const pair<double, double> score,
                        const pair<double, double> convsf_lowpt,
                        const pair<double, double> convsf_highpt,
                        const TString syst);

// Loop over sample, fix systematics
TH1D* makeHisto1D(const TString ERA,
                  const TString CHANNEL,
                  const TString SIGNAL,
                  const TString NETWORK,
                  const TString sampleKey,
                  const pair<double, double> score,
                  const pair<double, double> convsf_lowpt,
                  const pair<double, double> convsf_highpt,
                  const TString syst) {

    const vector<TString> sampleList = map_sample[sampleKey];
    TH1D *out = nullptr;
    for (const auto &sampleName : sampleList) {
        // construct filepath from the inputs
        TString filePath = static_cast<TString>(std::getenv("WORKDIR"))+"/data/"; 
        if (sampleName.Contains(SIGNAL))
            filePath += "PromptUnbinned/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/PromptUnbinned_TTToHcToWAToMuMu_"+sampleName+".root";
        else if (sampleName.Contains("nonprompt"))
            filePath += "MatrixUnbinned/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/DATA/MatrixUnbinned_SkimTree_SS2lOR3l_DoubleMuon.root";
        else if (sampleName.Contains("TTTT") || sampleName.Contains("tHq") || sampleName.Contains("WWG"))
            filePath += "PromptUnbinned/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/PromptUnbinned_" + sampleName+".root";
        else
            filePath += "PromptUnbinned/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/PromptUnbinned_SkimTree_SS2lOR3l_"+sampleName+".root";
        TH1D *h = makeHisto1DSingle(filePath, SIGNAL, sampleName, score, convsf_lowpt, convsf_highpt, syst);

        if (!out) out = static_cast<TH1D*>(h->Clone(sampleKey+"_"+syst));
        else      out->Add(h);
        delete h;
    }
    return out;
}



TH1D* makeHisto1DSingle(const TString filePath,
                        const TString SIGNAL,
                        const TString sampleName,
                        const pair<double, double> score,
                        const pair<double, double> convsf_lowpt,
                        const pair<double, double> convsf_highpt,
                        const TString syst) {
    TFile *f = new TFile(filePath, "read");
    TTree *tree = static_cast<TTree*>(f->Get("Events"));

    TString prefix;
    if (syst.Contains("Jet")) prefix = syst;
    else                      prefix = "Central";

    float pair1_mass; tree->SetBranchAddress(prefix+"_mass1", &pair1_mass);
    float pair2_mass; tree->SetBranchAddress(prefix+"_mass2", &pair2_mass);
    float score_ttFake; tree->SetBranchAddress(prefix+"_score_"+SIGNAL+"_vs_TTLL_powheg", &score_ttFake);
    float score_ttX;    tree->SetBranchAddress(prefix+"_score_"+SIGNAL+"_vs_ttX", &score_ttX);

    float w_norm, w_l1prefire, w_pileup, w_nonprompt;
    float sf_muonID, sf_dblmutrig, sf_btag;
    if (sampleName == "nonprompt") {
        if (syst == "NonpromptUp")        tree->SetBranchAddress("w_nonprompt_up", &w_nonprompt);
        else if (syst == "NonpromptDown") tree->SetBranchAddress("w_nonprompt_down", &w_nonprompt);
        else                              tree->SetBranchAddress("w_nonprompt", &w_nonprompt);
    }
    else {
        tree->SetBranchAddress("w_norm", &w_norm);
        tree->SetBranchAddress("w_l1prefire", &w_l1prefire);
        tree->SetBranchAddress("w_pileup", &w_pileup);

        if (syst == "MuonIDSFUp") tree->SetBranchAddress(prefix+"_sf_muonID_up", &sf_muonID);
        else if (syst == "MuonIDSFDown") tree->SetBranchAddress(prefix+"_sf_muonID_down", &sf_muonID);
        else                             tree->SetBranchAddress(prefix+"_sf_muonID", &sf_muonID);

        if (syst == "DblMuTrigSFUp") tree->SetBranchAddress(prefix+"_sf_dblmutrig_up", &sf_dblmutrig);
        else if (syst == "DblMuTrigSFDown") tree->SetBranchAddress(prefix+"_sf_dblmutrig_down", &sf_dblmutrig);
        else                                tree->SetBranchAddress(prefix+"_sf_dblmutrig", &sf_dblmutrig);

        tree->SetBranchAddress(prefix+"_sf_btag_central", &sf_btag);
    }

    pair<double, double> convsf;
    if (sampleName.Contains("DYJets")) convsf = convsf_lowpt;
    else if (sampleName.Contains("ZGToLLG")) convsf = convsf_highpt;
    else convsf = {1., 1.};

    // event loop
    TObjArray *tokens = SIGNAL.Tokenize("_");
    TString Astring = ((TObjString*) tokens->At(1))->GetString();
    tokens = Astring.Tokenize("-");
    TString mAstr = ((TObjString*) tokens->At(1))->GetString();
    const int mA = mAstr.Atoi();
    TH1D *out = (mA - 10 > 12) ? new TH1D(sampleName+"_"+syst, "", 200, mA-10., mA+10.) : new TH1D(sampleName+"_"+syst, "", 120, mA-3., mA+3.);
    for (unsigned int i = 0; i < tree->GetEntries(); i++) {
        tree->GetEntry(i);
        if (pair1_mass < 0. && pair2_mass < 0.) continue;
        if (! (score_ttFake > score.first && score_ttX > score.second)) continue;

        const double Amass = fabs(pair1_mass - mA) < fabs(pair2_mass - mA) ? pair1_mass : pair2_mass;
        double weight = 1.;
        if (sampleName == "nonprompt") weight = w_nonprompt;
        else                           weight = w_norm * w_l1prefire * w_pileup * sf_muonID * sf_dblmutrig * sf_btag;

        // Conversion SF
        if (sampleName.Contains("DYJets") || sampleName.Contains("ZGToLLG")) {
            if (syst == "ConversionUp")        weight *= (convsf.first + convsf.second);
            else if (syst == "ConversionDown") weight *= max(0., (convsf.first - convsf.second));
            else                               weight *= convsf.first;
        }
        out->Fill(Amass, weight);
    }
    out->SetDirectory(0);
    f->Close();

    return out;
}
