#!/bin/bash
CHANNEL=$1

python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-70_MA-15 >> logs/${CHANNEL}_MHc-70_MA-15.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-70_MA-40 >> logs/${CHANNEL}_MHc-70_MA-40.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-70_MA-65 >> logs/${CHANNEL}_MHc-70_MA-65.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-100_MA-15 >> logs/${CHANNEL}_MHc-100_MA-15.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-100_MA-60 >> logs/${CHANNEL}_MHc-100_MA-60.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-100_MA-95 >> logs/${CHANNEL}_MHc-100_MA-95.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-130_MA-15 >> logs/${CHANNEL}_MHc-130_MA-15.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-130_MA-55 >> logs/${CHANNEL}_MHc-130_MA-55.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-130_MA-90 >> logs/${CHANNEL}_MHc-130_MA-90.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-130_MA-125 >> logs/${CHANNEL}_MHc-130_MA-125.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-160_MA-15 >> logs/${CHANNEL}_MHc-160_MA-15.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-160_MA-85 >> logs/${CHANNEL}_MHc-160_MA-85.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-160_MA-120 >> logs/${CHANNEL}_MHc-160_MA-120.log &
python optimizeCuts.py --channel ${CHANNEL} --masspoint MHc-160_MA-155 >> logs/${CHANNEL}_MHc-160_MA-155.log &

