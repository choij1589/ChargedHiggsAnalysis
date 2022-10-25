from ROOT import TLorentzVector

# Base class for all objects
class Particle(TLorentzVector):
    def __init__(self, pt, eta, phi, mass):
        TLorentzVector.__init__(self)
        self.SetPtEtaPhiM(pt, eta, phi, mass)
        self.charge = 0
        self.is_muon = False
        self.is_electron = False
        self.is_jet = False
        self.chargedHadronFraction = 0.
        self.neutralHadronFraction = 0.
        self.chargedEmFraction = 0.
        self.neutralEmFraction = 0.
        self.muonFraction = 0.
        self.chargedMultiplicity = 0.
        self.neutralMultiplicity = 0.
        self.btagScore = 0.
        self.pileupJetId = 0.
        
    def IsMuon(self):
        return self.is_muon
    
    def IsElectron(self):
        return self.is_electron
    
    def IsJet(self):
        return self.is_jet
    
    def Charge(self):
        return self.charge
    
    def ChargedHadronFraction(self):
        return self.chargedHadronFraction

    def NeutralHadronFraction(self):
        return self.neutralHadronFraction

    def ChargedEmFraction(self):
        return self.chargedEmFraction

    def NeutralEmFraction(self):
        return self.neutralEmFraction

    def MuonFraction(self):
        return self.muonFraction

    def ChargedMultiplicity(self):
        return self.chargedMultiplicity

    def NeutralMultiplicity(self):
        return self.neutralMultiplicity

    def BtagScore(self):
        return self.btagScore

    def PileupJetId(self):
        return self.pileupJetId 

# Base class for electron / muon
class Lepton(Particle):
    def __init__(self, pt, eta, phi, mass):
        Particle.__init__(self, pt, eta, phi, mass)
        
    def SetCharge(self, charge):
        self.charge = charge
        
    def SetLepType(self, lepType):
        # LeptonType
        # 1: ewprompt
        # 2: signal muons, from A
        # 3: muons from tau
        # 6: from offshell W, i.e. directly from Hc
        # <0: fake leptons
        self.lepType = lepType
        
    def SetRelIso(self, relIso):
        self.relIso = relIso
    
    def SetMiniIso(self, miniIso):
        self.miniIso = miniIso
        
    def SetID(self, passTight, passLoose):
        self.passTight = passTight
        self.passLoose = passLoose
        
    def LepType(self):
        return self.lepType
    
    def RelIso(self):
        return self.relIso
    
    def MiniIso(self):
        return self.miniIso
    
    def PassID(self, idstring):
        if idstring == "tight":
            return self.passTight
        elif idstring == "loose":
            return self.passLoose
        else:
            print(f"[DataFormat::Lepton] Wrong ID string {idstring}")
            exit(1)


class Muon(Lepton):
    def __init__(self, pt, eta, phi, mass):
        Lepton.__init__(self, pt, eta, phi, mass)
        self.is_muon = True
        self.muonFraction = 1.
        self.chargedMultiplicity = 1.
        

class Electron(Lepton):
    def __init__(self, pt, eta, phi, mass):
        Lepton.__init__(self, pt, eta, phi, mass)
        self.is_electron = True
        self.electronEmFraction = 1.
        self.chargedMultiplicity = 1.

class Jet(Particle):
    def __init__(self, pt, eta, phi, mass):
        Particle.__init__(self, pt, eta, phi, mass)
        self.is_jet = True
        self.isBtagged = False
        
    def SetCharge(self, charge):
        self.charge = charge
    
    def SetHadronFraction(self, chargedFraction, neutralFraction):
        self.chargedHadronFraction = chargedFraction
        self.neutralHadronFraction = neutralFraction

    def SetEmFraction(self, chargedFraction, neutralFraction):
        self.chargedEmFraction = chargedFraction
        self.neutralEmFraction = neutralFraction

    def SetMuonFraction(self, muonFraction):
        self.muonFraction = muonFraction

    def SetMultiplicity(self, chargedMultiplicity, neutralMultiplicity):
        self.chargedMultiplicity = chargedMultiplicity
        self.neutralMultiplicity = neutralMultiplicity

    def SetPileupId(self, pileupId):
        self.pileupJetId = pileupId

    def SetBtagScore(self, btagScore):
        self.btagScore = btagScore

    def SetIsBtagged(self, isBtagged):
        self.isBtagged = isBtagged

    def SetPartonFlavour(self, partonFlavour):
        self.partonFlavour = partonFlavour

    def SetHadronFlavour(self, hadronFlavour):
        self.hadronFlavour = hadronFlavour

    def IsBtagged(self):
        return self.isBtagged

    def HadronFlavour(self):
        return self.hadronFlavour

    def PartonFlavour(self):
        return self.partonFlavour

# object collection generators
def get_muons(evt, momentum_shift=0):
    muons = []
    if momentum_shift == 1:
        muons_zip = zip(evt.MuonPtColl_MomentumShiftUp,
                        evt.MuonEtaColl,
                        evt.MuonPhiColl,
                        evt.MuonMassColl,
                        evt.MuonChargeColl,
                        evt.MuonLepTypeColl,
                        evt.MuonRelIsoColl,
                        evt.MuonMiniRelIsoColl,
                        evt.MuonPassTightColl,
                        evt.MuonPassLooseColl)
    elif momentum_shift == -1:
        muons_zip = zip(evt.MuonPtColl_MomentumShiftDown,
                        evt.MuonEtaColl,
                        evt.MuonPhiColl,
                        evt.MuonMassColl,
                        evt.MuonChargeColl,
                        evt.MuonLepTypeColl,
                        evt.MuonRelIsoColl,
                        evt.MuonMiniRelIsoColl,
                        evt.MuonPassTightColl,
                        evt.MuonPassLooseColl)
    else:   # central
        muons_zip = zip(evt.MuonPtColl,
                        evt.MuonEtaColl,
                        evt.MuonPhiColl,
                        evt.MuonMassColl,
                        evt.MuonChargeColl,
                        evt.MuonLepTypeColl,
                        evt.MuonRelIsoColl,
                        evt.MuonMiniRelIsoColl,
                        evt.MuonPassTightColl,
                        evt.MuonPassLooseColl)
        
    for pt, eta, phi, mass, charge, lepType, relIso, miniIso, pTight, pLoose in muons_zip:
        this_muon = Muon(pt, eta, phi, mass)
        this_muon.SetCharge(charge)
        this_muon.SetLepType(lepType)
        this_muon.SetRelIso(relIso)
        this_muon.SetMiniIso(miniIso)
        this_muon.SetID(pTight, pLoose)
        muons.append(this_muon)
    
    assert evt.nMuons == len(muons)
    return muons

def get_electrons(evt, en_shift=0, res_shift=0):
    electrons = []
    if en_shift == 1:
        electrons_zip = zip(evt.ElectronPtColl_EnShiftUp,
                            evt.ElectronEtaColl,
                            evt.ElectronPhiColl,
                            evt.ElectronMassColl,
                            evt.ElectronChargeColl,
                            evt.ElectronLepTypeColl,
                            evt.ElectronRelIsoColl,
                            evt.ElectronMiniRelIsoColl,
                            evt.ElectronPassTightColl,
                            evt.ElectronPassLooseColl)
    elif en_shift == -1:
        electrons_zip = zip(evt.ElectronPtColl_EnShiftDown,
                            evt.ElectronEtaColl,
                            evt.ElectronPhiColl,
                            evt.ElectronMassColl,
                            evt.ElectronChargeColl,
                            evt.ElectronLepTypeColl,
                            evt.ElectronRelIsoColl,
                            evt.ElectronMiniRelIsoColl,
                            evt.ElectronPassTightColl,
                            evt.ElectronPassLooseColl)
    elif res_shift == 1:
        electrons_zip = zip(evt.ElectronPtColl_ResShiftUp,
                            evt.ElectronEtaColl,
                            evt.ElectronPhiColl,
                            evt.ElectronMassColl,
                            evt.ElectronChargeColl,
                            evt.ElectronLepTypeColl,
                            evt.ElectronRelIsoColl,
                            evt.ElectronMiniRelIsoColl,
                            evt.ElectronPassTightColl,
                            evt.ElectronPassLooseColl)
    elif res_shift == -1:
        electrons_zip = zip(evt.ElectronPtColl_ResShiftDown,
                            evt.ElectronEtaColl,
                            evt.ElectronPhiColl,
                            evt.ElectronMassColl,
                            evt.ElectronChargeColl,
                            evt.ElectronLepTypeColl,
                            evt.ElectronRelIsoColl,
                            evt.ElectronMiniRelIsoColl,
                            evt.ElectronPassTightColl,
                            evt.ElectronPassLooseColl)
    else:   # central
        electrons_zip = zip(evt.ElectronPtColl,
                            evt.ElectronEtaColl,
                            evt.ElectronPhiColl,
                            evt.ElectronMassColl,
                            evt.ElectronChargeColl,
                            evt.ElectronLepTypeColl,
                            evt.ElectronRelIsoColl,
                            evt.ElectronMiniRelIsoColl,
                            evt.ElectronPassTightColl,
                            evt.ElectronPassLooseColl)
        
    for pt, eta, phi, mass, charge, lepType, relIso, miniIso, pTight, pLoose in electrons_zip:
        this_electron = Electron(pt, eta, phi, mass)
        this_electron.SetCharge(charge)
        this_electron.SetLepType(lepType)
        this_electron.SetRelIso(relIso)
        this_electron.SetMiniIso(miniIso)
        this_electron.SetID(pTight, pLoose)
        electrons.append(this_electron)
    
    assert evt.nElectrons == len(electrons)
    return electrons

def get_jets(evt, en_shift=0, res_shift=0):
    jets = []
    if en_shift == 1:
        jets_zip = zip(evt.JetPtColl_EnShiftUp,
                       evt.JetEtaColl,
                       evt.JetPhiColl,
                       evt.JetMassColl,
                       evt.JetChargeColl,
                       evt.JetChargedHadronEnergyFractionColl,
                       evt.JetNeutralHadronEnergyFractionColl,
                       evt.JetChargedEmEnergyFractionColl,
                       evt.JetNeutralEmEnergyFractionColl,
                       evt.JetMuonEnergyFractionColl,
                       evt.JetChargedMultiplicityColl,
                       evt.JetNetralMultiplicityColl,
                       evt.JetPileupIdColl,
                       evt.JetBtagScoreColl,
                       evt.JetIsBtaggedColl,
                       evt.JetPartonFlavourColl,
                       evt.JetHadronFlavourColl
                       )
    elif en_shift == -1:
        jets_zip = zip(evt.JetPtColl_EnShiftDown,
                       evt.JetEtaColl,
                       evt.JetPhiColl,
                       evt.JetMassColl,
                       evt.JetChargeColl,
                       evt.JetChargedHadronEnergyFractionColl,
                       evt.JetNeutralHadronEnergyFractionColl,
                       evt.JetChargedEmEnergyFractionColl,
                       evt.JetNeutralEmEnergyFractionColl,
                       evt.JetMuonEnergyFractionColl,
                       evt.JetChargedMultiplicityColl,
                       evt.JetNetralMultiplicityColl,
                       evt.JetPileupIdColl,
                       evt.JetBtagScoreColl,
                       evt.JetIsBtaggedColl,
                       evt.JetPartonFlavourColl,
                       evt.JetHadronFlavourColl
                       )
    elif res_shift == 1:
        jets_zip = zip(evt.JetPtColl_ResShiftUp,
                       evt.JetEtaColl,
                       evt.JetPhiColl,
                       evt.JetMassColl,
                       evt.JetChargeColl,
                       evt.JetChargedHadronEnergyFractionColl,
                       evt.JetNeutralHadronEnergyFractionColl,
                       evt.JetChargedEmEnergyFractionColl,
                       evt.JetNeutralEmEnergyFractionColl,
                       evt.JetMuonEnergyFractionColl,
                       evt.JetChargedMultiplicityColl,
                       evt.JetNetralMultiplicityColl,
                       evt.JetPileupIdColl,
                       evt.JetBtagScoreColl,
                       evt.JetIsBtaggedColl,
                       evt.JetPartonFlavourColl,
                       evt.JetHadronFlavourColl
                       )
    elif res_shift == -1:
        jets_zip = zip(evt.JetPtColl_ResShiftDown,
                       evt.JetEtaColl,
                       evt.JetPhiColl,
                       evt.JetMassColl,
                       evt.JetChargeColl,
                       evt.JetChargedHadronEnergyFractionColl,
                       evt.JetNeutralHadronEnergyFractionColl,
                       evt.JetChargedEmEnergyFractionColl,
                       evt.JetNeutralEmEnergyFractionColl,
                       evt.JetMuonEnergyFractionColl,
                       evt.JetChargedMultiplicityColl,
                       evt.JetNetralMultiplicityColl,
                       evt.JetPileupIdColl,
                       evt.JetBtagScoreColl,
                       evt.JetIsBtaggedColl,
                       evt.JetPartonFlavourColl,
                       evt.JetHadronFlavourColl
                       )
    else:   # central
        jets_zip = zip(evt.JetPtColl,
                       evt.JetEtaColl,
                       evt.JetPhiColl,
                       evt.JetMassColl,
                       evt.JetChargeColl,
                       evt.JetChargedHadronEnergyFractionColl,
                       evt.JetNeutralHadronEnergyFractionColl,
                       evt.JetChargedEmEnergyFractionColl,
                       evt.JetNeutralEmEnergyFractionColl,
                       evt.JetMuonEnergyFractionColl,
                       evt.JetChargedMultiplicityColl,
                       evt.JetNetralMultiplicityColl,
                       evt.JetPileupIdColl,
                       evt.JetBtagScoreColl,
                       evt.JetIsBtaggedColl,
                       evt.JetPartonFlavourColl,
                       evt.JetHadronFlavourColl
                       )

    for pt, eta, phi, mass, charge, cH, nH, cE, nE, muonE, cM, nM, pileupId,  btagScore, isBtagged, pFlav, hFlav in jets_zip:
        this_jet = Jet(pt, eta, phi, mass)
        this_jet.SetCharge(charge)
        this_jet.SetHadronFraction(cH, nH)
        this_jet.SetEmFraction(cE, nE)
        this_jet.SetMuonFraction(muonE)
        this_jet.SetMultiplicity(cM, nM)
        this_jet.SetPileupId(pileupId)
        this_jet.SetBtagScore(btagScore)
        this_jet.SetIsBtagged(isBtagged)
        this_jet.SetPartonFlavour(pFlav)
        this_jet.SetHadronFlavour(hFlav)
        jets.append(this_jet)

    # PT ordering
    assert evt.nJets == len(jets)
    jets.sort(key=lambda x: x.Pt(), reverse=True)
    bjets = list(filter(lambda x: x.IsBtagged(), jets))

    return jets, bjets
