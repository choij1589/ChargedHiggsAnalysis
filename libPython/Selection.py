#### Channel definition
## 1E2Mu
# 1. Should pass triggers and safe cuts
# 2. 1E2Mu
# 3. Exist OS muon pair with M(mumu) > 12 GeV
# 4. Nj >= 2, Nb >= 1
## 3Mu
# 1. Should pass triggers and safe cuts
# 2. 3Mu
# 3. At least one muon pair should have opposite charge, i.e. abs(charge sum) == 1
# 4. All OS muon pairs' mass > 12 GeV
# 5. Nj >= 2, Nb >= 1
## Loose
# No charge condition
# No Nb condition

def pass_baseline(channel, evt, muons, electrons, idstring, isTraining=False):
    # check arguments
    if not channel in ["1E2Mu", "3Mu"]:
        print(f"[Selection::pass_baseline] Wrong channel {channel}")
        exit(1)
    
    # get loose leptons
    muons = list(filter(lambda x: x.PassID(idstring), muons))
    electrons = list(filter(lambda x: x.PassID(idstring), electrons))
    
    if channel == "1E2Mu":
        if not (len(muons) == 2 and len(electrons) == 1): return False
        if not abs(muons[0].Charge()+muons[1].Charge()) == 0: return False

        if not isTraining:
            pass_safecut = (muons[0].Pt() > 10. and electrons[0].Pt() > 25.) or (muons[0].Pt() > 25. and electrons[0].Pt() > 15.)
            if not evt.PassEMuTrigs: return False
            if not pass_safecut: return False

            if not (muons[0]+muons[1]).M() > 12.: return False
    else:   # 3Mu
        if not (len(muons) == 3 and len(electrons) == 0): return False
        if not abs(muons[0].Charge()+muons[1].Charge()+muons[2].Charge()) == 1: return False
        
        if not isTraining:
            pass_safecut = (muons[0].Pt() > 20. and muons[1].Pt() > 10. and muons[2].Pt() > 10.) 
            if not evt.PassDblMuTrigs: return False
            if not pass_safecut: return False
        
            if (muons[0].Charge() + muons[1].Charge() == 0) and (not (muons[0]+muons[1]).M() > 12.): return False
            if (muons[0].Charge() + muons[2].Charge() == 0) and (not (muons[0]+muons[2]).M() > 12.): return False
            if (muons[1].Charge() + muons[2].Charge() == 0) and (not (muons[1]+muons[2]).M() > 12.): return False
        
    return True

def select(channel, evt, muons, electrons, jets, bjets, idstring):
    if not pass_baseline(channel, evt, muons, electrons, jets, bjets, idstring):
        return None

    if channel == "1E2Mu":
        if len(bjets) >= 1:
            if len(jets) >= 2:
                return "SignalRegion"
        else:   # Control Regions
            if ((muons[0]+muons[1]).M() - 91.2) < 10.:
                return "ZFakeRegion"
            elif abs((muon[0]+muons[1]+muons[2]).M() - 91.2) < 10.:
                return "ZGammaRegion"
            else:
                return None
    else:   # 3Mu
        if len(bjets) >= 1:
            if len(jets) >= 2:
                return "SignalRegion"
        else:   # Control Regions
            isOnZ = False
            if (muons[0].Charge() + muons[1].Charge() == 0) and (abs((muons[0]+muons[1]).M() - 91.2) < 10.): isOnZ = True
            if (muons[0].Charge() + muons[2].Charge() == 0) and (abs((muons[0]+muons[2]).M() - 91.2) < 10.): isOnZ = True
            if (muons[1].Charge() + muons[2].Charge() == 0) and (abs((muons[1]+muons[2]).M() - 91.2) < 10.): isOnZ = True

            if isOnZ:
                return "ZFakeRegion"
            elif abs((muons[0]+muons[1]+muons[2]).M() - 91.2) < 10.:
                return "ZGammaRegion"
            else:
                return None
