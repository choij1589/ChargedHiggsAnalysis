#!/bin/sh
python checkMVATightWP.py --era 2016preVFP --region EB1 &
python checkMVATightWP.py --era 2016preVFP --region EB2 &
python checkMVATightWP.py --era 2016preVFP --region EE &

python checkMVATightWP.py --era 2016postVFP --region EB1 &
python checkMVATightWP.py --era 2016postVFP --region EB2 &
python checkMVATightWP.py --era 2016postVFP --region EE &

python checkMVATightWP.py --era 2017 --region EB1 &
python checkMVATightWP.py --era 2017 --region EB2 &
python checkMVATightWP.py --era 2017 --region EE &

python checkMVATightWP.py --era 2018 --region EB1 &
python checkMVATightWP.py --era 2018 --region EB2 &
python checkMVATightWP.py --era 2018 --region EE &
