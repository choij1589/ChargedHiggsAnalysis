void rate() {
    
    double mass, weight;

    TFile *f = new TFile("diboson.root");
    TTree *tree = (TTree*)f->Get("diboson_Central");
    tree->Print();

    tree->SetBranchAddress("mass", &mass);
    tree->SetBranchAddress("weight", &weight);

    TH1D *h = new TH1D("mass", "", 60, 10, 70);
    for (int entry=0; entry < tree->GetEntries(); entry++) {
        tree->GetEntry(entry);
        h->Fill(mass, weight);
    }
    cout << h->Integral() << endl;
}
