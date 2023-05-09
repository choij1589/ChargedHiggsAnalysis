#include <iostream>
using namespace ROOT;

void optimize() {
    EnableImplicitMT(4);

    const string signal = "MHc-160_MA-155";
    
    map<TString, double> map_mA = { {"MHc-70_MA-15", 15.},
                                    {"MHc-70_MA-40", 40.},
                                    {"MHc-70_MA-65", 64.9},
                                    {"MHc-100_MA-15", 15.},
                                    {"MHc-100_MA-60", 59.9},
                                    {"MHc-100_MA-95", 94.9},
                                    {"MHc-130_MA-15", 15.},
                                    {"MHc-130_MA-55", 54.9},
                                    {"MHc-130_MA-90", 89.9},
                                    {"MHc-130_MA-125", 125.},
                                    {"MHc-160_MA-15", 15.},
                                    {"MHc-160_MA-85", 84.9},
                                    {"MHc-160_MA-120", 120.},
                                    {"MHc-160_MA-155", 155.} 
                                  };
    map<TString, double> map_sigma = { {"MHc-70_MA-15", 0.100176},
                                       {"MHc-70_MA-40", 0.229418},
                                       {"MHc-70_MA-65", 0.465296},
                                       {"MHc-100_MA-15", 0.0943238},
                                       {"MHc-100_MA-60", 0.365484},
                                       {"MHc-100_MA-95", 0.776107},
                                       {"MHc-130_MA-15", 0.121217},
                                       {"MHc-130_MA-55", 0.321891},
                                       {"MHc-130_MA-90", 0.785362},
                                       {"MHc-130_MA-125", 1.10164},
                                       {"MHc-160_MA-15", 0.123096},
                                       {"MHc-160_MA-85", 0.638947},
                                       {"MHc-160_MA-120", 1.14469},
                                       {"MHc-160_MA-155", 1.61999} 
                                    };
    map<TString, double> map_width = { {"MHc-70_MA-15", 0.168247},
                                       {"MHc-70_MA-40", 0.636159},
                                       {"MHc-70_MA-65", 1.05443},
                                       {"MHc-100_MA-15", 0.172952},
                                       {"MHc-100_MA-60", 0.958266},
                                       {"MHc-100_MA-95", 1.45102},
                                       {"MHc-130_MA-15", 0.113796},
                                       {"MHc-130_MA-55", 0.929785},
                                       {"MHc-130_MA-90", 1.1627},
                                       {"MHc-130_MA-125", 2.16511},
                                       {"MHc-160_MA-15", 0.1244},
                                       {"MHc-160_MA-85", 1.34706},
                                       {"MHc-160_MA-120", 1.67321},
                                       {"MHc-160_MA-155", 2.59752} 
                                     };


    const double mA = map_mA[signal];
    const double sigma = map_sigma[signal];
    const double width = map_width[signal];
    const double window = sqrt(pow(sigma, 2) + pow(width, 2));
    vector<string> MCSamples = {"Nonprompt.root",
                                "DYJets.root", "ZGToLLG.root",
                                "WZTo3LNu_amcatnlo.root", "ZZTo4L_powheg.root",
                                "ttWToLNu.root", "ttZToLLNuNu.root", "ttHToNonbb.root",
                                "WWW.root", "WWZ.root", "WZZ.root", "ZZZ.root", 
                                "TTG.root", "tZq.root", "VBF_HToZZTo4L.root", "GluGluHToZZTo4L.root",
                                "TTTT.root", "WWG.root"};
    vector<string> bkgSamples;
    for (const auto &sample: MCSamples)
        bkgSamples.emplace_back(signal+"/"+sample);


    // load trees
    RDataFrame *sigFrame = new RDataFrame("Events", signal + "/" + signal+".root");
    RDataFrame *bkgFrame = new RDataFrame("Events", bkgSamples);
    
    // with only mass cut
    const string massStr = to_string(mA-window) + " < Amass && Amass < " + to_string(mA+window);
    auto nSig = sigFrame->Filter(massStr).Sum("weight").GetValue();
    auto nBkg = bkgFrame->Filter(massStr).Sum("weight").GetValue();
    auto metric = sqrt(2*((nSig+nBkg)*log(1+nSig/nBkg)-nSig));
    cout << "[" << signal << "] with only mass cut: " << metric << endl;

    double bestXcut = 0.;
    double bestYcut = 0.;
    double bestMetric = 0.;

    auto sigFiltered = sigFrame->Filter(massStr);
    auto bkgFiltered = bkgFrame->Filter(massStr);

    for (double i = 0.; i <= 1; i += 0.02) {
        for (double j = 0.; j < 1; j += 0.02) {
            //const string massStr = to_string(mA-window) + " < Amass && Amass < " + to_string(mA+window);
            const string fakeStr = "score_ttFake >= " + to_string(i);
            const string ttXStr = "score_ttX >= " + to_string(j);
            const string filterStr = fakeStr + " && " + ttXStr;
            auto nSig = sigFiltered.Filter(filterStr).Sum("weight").GetValue();
            auto nBkg = bkgFiltered.Filter(filterStr).Sum("weight").GetValue();
            if (nBkg == 0) continue;
            auto metric = sqrt(2*((nSig+nBkg)*log(1+nSig/nBkg)-nSig));

            if (bestMetric < metric) {
                bestXcut = i;
                bestYcut = j;
                bestMetric = metric;
            }
        }
    }
    cout << bestXcut << "\t" << bestYcut << "\t" << bestMetric << endl;
}

