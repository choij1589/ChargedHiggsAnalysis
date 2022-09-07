#include <iostream>
#include <string>
#include <TFile.h>
#include <TTree.h>
using namespace std;

int main(int argc, char** argv) {

    const TString inputfile = (TString)argv[1];
    const unsigned int nfiles = stoi(argv[2]);

    cout << "@@@@ inputfile: " << inputfile << endl;
    cout << "@@@@ split into: " << nfiles << endl;

    TFile *f = new TFile(inputfile);
    TTree *oldtree = (TTree*)f->Get("Events");
    const unsigned int  nEntries = oldtree->GetEntries();

    const unsigned int whole = nEntries / nfiles;
    const unsigned int remainder = nEntries % nfiles;

    cout << "@@@@ nEntries: " << nEntries << endl;
    cout << "@@@@ each file contains " << whole << " events" << endl;
    cout << "@@@@ the last file contains " << whole+remainder << " events" << endl;

    for (unsigned int i = 0; i < nfiles; i++) {
        TString outfile_name = inputfile;
        TString s_replace = "_"+TString::Itoa(i, 10)+".root";
        outfile_name.ReplaceAll(".root", s_replace);
        
        TFile* newfile = new TFile(outfile_name, "recreate");
        TTree* newtree = oldtree->CloneTree(0);

        // decide entries
        unsigned int first_entry = i*whole;
        unsigned int last_entry = (i+1)*whole;
        if (i == nfiles-1)  // last file
            last_entry += remainder;
        
        for (unsigned int entry = first_entry; entry < last_entry; entry++) {
            oldtree->GetEntry(entry);
            newtree->Fill();
        }
        newfile->cd();
        newtree->Write();

        cout << "@@@@ copied " << newtree->GetEntries() << " events to " << outfile_name << endl;
        newfile->Close();
    }
    f->Close();
    
    return 0;
}
