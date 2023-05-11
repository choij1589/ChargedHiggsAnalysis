void printLimit() {
    const TString ERA = "2018";
    const TString CHANNEL = "Skim3Mu";
    const TString MASSPOINT = "MHc-130_MA-90";
    const TString BASEDIR = "results/"+ERA+"/"+CHANNEL+"__/"+MASSPOINT+"/";

    TFile *f = nullptr;
    TTree *limit = nullptr;
    double value;
   
    cout << "[Grid]\t0.025\t0.160\t0.500\t0.840\t0.975\tobserved" << endl;

    // asymptotic limits
    f = new TFile(BASEDIR+"higgsCombineTest.AsymptoticLimits.mH120.root");
    limit = static_cast<TTree*>(f->Get("limit"));
    limit->SetBranchAddress("limit", &value);
    
    cout << "[Asymptotic limits]\t";
    for (unsigned int i=0; i<limit->GetEntries(); i++) {
        limit->GetEntry(i);
        cout << value*5 << "\t";
    }
    cout << endl;
    
    // hybridnew limits
    cout << "[HybridNew limits]\t";
   
    f = new TFile(BASEDIR+"higgsCombineTest.HybridNew.mH120.quant0.025.root");
    limit = static_cast<TTree*>(f->Get("limit"));
    limit->SetBranchAddress("limit", &value);
    limit->GetEntry(0);
    cout << value*5 << "\t";  

    f = new TFile(BASEDIR+"higgsCombineTest.HybridNew.mH120.quant0.160.root");
    limit = static_cast<TTree*>(f->Get("limit"));
    limit->SetBranchAddress("limit", &value);
    limit->GetEntry(0);
    cout << value*5 << "\t";

    f = new TFile(BASEDIR+"higgsCombineTest.HybridNew.mH120.quant0.500.root");
    limit = static_cast<TTree*>(f->Get("limit"));
    limit->SetBranchAddress("limit", &value);
    limit->GetEntry(0);
    cout << value*5 << "\t";

    f = new TFile(BASEDIR+"higgsCombineTest.HybridNew.mH120.quant0.840.root");
    limit = static_cast<TTree*>(f->Get("limit"));
    limit->SetBranchAddress("limit", &value);
    limit->GetEntry(0);
    cout << value*5 << "\t";

    f = new TFile(BASEDIR+"higgsCombineTest.HybridNew.mH120.quant0.975.root");
    limit = static_cast<TTree*>(f->Get("limit"));
    limit->SetBranchAddress("limit", &value);
    limit->GetEntry(0);
    cout << value*5 << "\t";

    f = new TFile(BASEDIR+"higgsCombineTest.HybridNew.mH120.root");
    limit = static_cast<TTree*>(f->Get("limit"));
    limit->SetBranchAddress("limit", &value);
    limit->GetEntry(0);
    cout << value*5 << endl;
}
