# MeasFakeRateV4.1
- Updated Loose ID for electron, the value for MVANoIso / miniRelIso / SIP3D have been changed
- Using the same code as MeasFakeRateV4.

# How To
```bash
python parseIntegral.py --era $ERA --measure $MEASURE
python measFakeRate.py --era $ERA --measure $MEASURE
```

## parseIntegral.py
It reads the root file and save the integral results in ZEnriched region. It will be used to measure the prompt scale in QCDEnriched region.

## measFakeRate.py
Fake rate is defined as
$$ \mathrm{fake rate} = \mathrm{N(pass tight ID | nonprompt)} / \mathrm{N(pass loose ID | nonprompt)} $$
Even if we defined QCD Enriched region, we don't know the source of the lepton: The prompt leptons should be subtracted. The prompt normalization scale is measured in Z-enriched region. The code will calculate the prompt normalization scale and measure the fake rate from the data.
