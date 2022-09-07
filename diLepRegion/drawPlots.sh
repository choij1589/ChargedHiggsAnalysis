#!/bin/sh
ERAs=( 2016preVFP 2016postVFP 2017 2018 )

for ERA in "${ERAs[@]}"
do
	echo drawing plots for ${ERA}...
	mkdir -p plots/${ERA}/MuonIDSFOnly
	python drawPlots.py -e ${ERA} -v diMuon/pt		-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v diMuon/eta		-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v diMuon/phi		-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v diMuon/mass	-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v muons/1/pt		-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v muons/1/eta	-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v muons/1/phi	-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v muons/2/pt		-c DiMu/DrellYanEnriched
    python drawPlots.py -e ${ERA} -v muons/2/eta	-c DiMu/DrellYanEnriched
    python drawPlots.py -e ${ERA} -v muons/2/phi	-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v jets/1/pt		-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v jets/1/eta		-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v jets/1/phi		-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v jets/2/pt		-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v jets/2/eta		-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v jets/2/phi		-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v jets/size		-c DiMu/DrellYanEnriched
	python drawPlots.py -e ${ERA} -v jets/HT		-c DiMu/DrellYanEnriched
    python drawPlots.py -e ${ERA} -v muons/1/pt     -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v muons/1/eta    -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v muons/1/phi    -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v muons/2/pt     -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v muons/2/eta    -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v muons/2/phi    -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v jets/1/pt      -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v jets/1/eta     -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v jets/1/phi     -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v jets/2/pt      -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v jets/2/eta     -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v jets/2/phi     -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v jets/size      -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v jets/HT        -c DiMu/TTbarEnriched
	python drawPlots.py -e ${ERA} -v bjets/1/pt      -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v bjets/1/eta     -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v bjets/1/phi     -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v bjets/2/pt      -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v bjets/2/eta     -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v bjets/2/phi     -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v bjets/size      -c DiMu/TTbarEnriched
    python drawPlots.py -e ${ERA} -v bjets/HT        -c DiMu/TTbarEnriched
done

