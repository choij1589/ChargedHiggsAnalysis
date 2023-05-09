#include <iostream>
#include <string>
#include <filesystem>
#include <ROOT/RDataFrame.hxx>
using namespace ROOT;

vector<double> optimize(const string ERA, 
                        const string CHANNEL,
                        const string NETWORK,
                        const string SIGNAL,
                        const double sigXsec, // in fb
                        const double mA, const double sigma, const double width) {
    const double window = sqrt(pow(sigma, 2) + pow(width, 2));
    const string WORKDIR = static_cast<string>(std::getenv("WORKDIR"));
    const string basePath = WORKDIR+"/SignalRegionStudy/"+ERA+"/"+CHANNEL+"__"+NETWORK+"__/"+SIGNAL+"/";
    vector<string> MCSamples = {"Nonprompt.root",
                                "DYJets.root", "ZGToLLG.root",
                                "WZTo3LNu_amcatnlo.root", "ZZTo4L_powheg.root",
                                "ttWToLNu.root", "ttZToLLNuNu.root", "ttHToNonbb.root",
                                "WWW.root", "WWZ.root", "WZZ.root", "ZZZ.root", 
                                "TTG.root", "tZq.root", "tHq.root", 
                                "VBF_HToZZTo4L.root", "GluGluHToZZTo4L.root",
                                "TTTT.root", "WWG.root"};
    vector<string> bkgSamples;
    for (const auto &sample: MCSamples) {
        auto samplePath = basePath+sample;
        // check whether the file exists
        if (! std::filesystem::exists(samplePath)) continue;
        bkgSamples.emplace_back(samplePath);
    }

    vector<double> out;

    // load trees
    RDataFrame *sigFrame = new RDataFrame("Events", basePath+SIGNAL+".root");
    RDataFrame *bkgFrame = new RDataFrame("Events", bkgSamples);
    
    // with only mass cut
    const string massStr = to_string(max(12., mA-window)) + " < Amass && Amass < " + to_string(mA+window);
    auto nSig = sigFrame->Filter(massStr).Sum("weight").GetValue() * (sigXsec/15.); 
    auto nBkg = bkgFrame->Filter(massStr).Sum("weight").GetValue();
    auto metric = sqrt(2*((nSig+nBkg)*log(1+nSig/nBkg)-nSig));
    out.emplace_back(metric);
    std::cout << "[" << SIGNAL << "] with only mass cut: " << metric << std::endl;

    double bestXcut = 0.;
    double bestYcut = 0.;
    double bestMetric = 0.;

    auto sigFiltered = sigFrame->Filter(massStr);
    auto bkgFiltered = bkgFrame->Filter(massStr);

    for (double i = 0.; i <= 1; i += 0.01) {
        for (double j = 0.; j <= 1; j += 0.01) {
            const string fakeStr = "score_ttFake >= " + to_string(i);
            const string ttXStr = "score_ttX >= " + to_string(j);
            const string filterStr = fakeStr + " && " + ttXStr;
            auto nSig = sigFiltered.Filter(filterStr).Sum("weight").GetValue() * (sigXsec/15.);
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
    out.emplace_back(bestMetric);
    out.emplace_back(bestXcut);
    out.emplace_back(bestYcut);
    std::cout << "[" << SIGNAL << "] " << bestXcut << "\t" << bestYcut << "\t" << bestMetric << std::endl;
    return out;
}

