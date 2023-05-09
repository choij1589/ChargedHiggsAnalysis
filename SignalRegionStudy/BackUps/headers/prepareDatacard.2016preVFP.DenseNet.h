#include <map>

//==== Sample list
map<TString, vector<TString>> map_sample = {
              {"nonprompt", {"nonprompt"}},
              {"diboson", {"WZTo3LNu_amcatnlo","ZZTo4L_powheg"}},
              {"conversion", {"DYJets", "DYJets10to50_MG", "ZGToLLG"}},
              {"ttX", {"ttWToLNu", "ttZToLLNuNu", "ttHToNonbb"}},
              {"others", {"WWW", "WWZ", "WZZ", "ZZZ", "TTG", "tZq", "VBF_HToZZTo4L", "GluGluHToZZTo4L"}}
            };

//==== Fitting results
map<TString, double> map_mA = { {"MHc-70_MA-15", 15.},
                                {"MHc-70_MA-40", 40.},
                                {"MHc-70_MA-65", 65.},
                                {"MHc-100_MA-15", 15.},
                                {"MHc-100_MA-60", 60.},
                                {"MHc-100_MA-95", 95.},
                                {"MHc-130_MA-15", 15.},
                                {"MHc-130_MA-55", 55.},
                                {"MHc-130_MA-90", 90.},
                                {"MHc-130_MA-125", 125.},
                                {"MHc-160_MA-15", 15.},
                                {"MHc-160_MA-85", 85.},
                                {"MHc-160_MA-120", 120.},
                                {"MHc-160_MA-155", 155.} 
                              };  
map<TString, double> map_sigma = { {"MHc-70_MA-15", 0.11033},
                                   {"MHc-70_MA-40", 0.182434},
                                   {"MHc-70_MA-65", 0.471047},
                                   {"MHc-100_MA-15", 0.0930342},
                                   {"MHc-100_MA-60", 0.344411},
                                   {"MHc-100_MA-95", 0.604872},
                                   {"MHc-130_MA-15", 0.117027},
                                   {"MHc-130_MA-55", 0.243583},
                                   {"MHc-130_MA-90", 0.718199},
                                   {"MHc-130_MA-125", 0.879492},
                                   {"MHc-160_MA-15", 0.120021},
                                   {"MHc-160_MA-85", 0.578887},
                                   {"MHc-160_MA-120", 1.00985},
                                   {"MHc-160_MA-155", 1.48121} 
                                 };  
map<TString, double> map_width = { {"MHc-70_MA-15", 0.134634},
                                   {"MHc-70_MA-40", 0.685245},
                                   {"MHc-70_MA-65", 0.979598},
                                   {"MHc-100_MA-15", 0.171075},
                                   {"MHc-100_MA-60", 0.965929},
                                   {"MHc-100_MA-95", 1.75398},
                                   {"MHc-130_MA-15", 0.111275},
                                   {"MHc-130_MA-55", 1.02639},
                                   {"MHc-130_MA-90", 1.18526},
                                   {"MHc-130_MA-125", 2.37517},
                                   {"MHc-160_MA-15", 0.119447},
                                   {"MHc-160_MA-85", 1.39002},
                                   {"MHc-160_MA-120", 1.84166},
                                   {"MHc-160_MA-155", 2.56311} 
                                 };

//==== Cut optimization results
map<TString, pair<double, double>> map_score = { {"MHc-70_MA-15", {0.88, 0.} },
                                                 {"MHc-70_MA-40", {0.8, 0.88} },
                                                 {"MHc-70_MA-65", {0.18, 0.} },
                                                 {"MHc-100_MA-15", {0.8, 0.1} },
                                                 {"MHc-100_MA-60", {0.98, 0.44} },
                                                 {"MHc-100_MA-95", {0.92, 0.72} },
                                                 {"MHc-130_MA-15", {0.94, 0.} },
                                                 {"MHc-130_MA-55", {0.9, 0.48} },
                                                 {"MHc-130_MA-90", {0.16, 0.48} },
                                                 {"MHc-130_MA-125", {0, 0.02} },
                                                 {"MHc-160_MA-15", {0.86, 0.02} },
                                                 {"MHc-160_MA-85", {0.22, 0.02} },
                                                 {"MHc-160_MA-120", {0.02, 0.06} },
                                                 {"MHc-160_MA-155", {0.06, 0.24} } 
                                              };

//==== Conversion SFs
map<TString, pair<double, double>> map_convsf_2016 = { {"LowPT3Mu", {0.906, 0.878}},
                                                       {"HighPT3Mu", {2.003, 0.739}}
                                                     };
map<TString, pair<double, double>> map_convsf_2017 = { {"LowPT3Mu", {0.901, 1.303}},
                                                       {"HighPT3Mu", {1.239, 0.464}},
                                                     };
map<TString, pair<double, double>> map_convsf_2018 = { {"LowPT3Mu", {0.628, 0.522}},
                                                       {"HighPT3Mu", {0.981, 0.412}}
                                                     };

// function declaration
TH1D *makeHisto1DSingle(const TString SIGNAL, const TString sampleName, const TString syst, const bool doCut);
TH1D *makeHisto1D(const TString SIGNAL, const TString sampleKey, const TString syst, const bool doCut);
