#!/usr/bin/env bash

echo "making fixtures from directory: $1 WILL REMOVE EXISTING ENTWINED FIXTURES"

if [[ ! -d $1 ]]
then
        echo "directory does not exist, try again"
        exit
fi

mkdir -p ~/Chromatik/Fixtures/Entwined
rm ~/Chromatik/Fixtures/Entwined/*
rm ~/Chromatik/Projects/entwined.lxp
rm ~/Chromatik/autoplay.lxr


echo "building LXF files from JSON descriptions"
python fairy_circle.py --config $1/fairy_circles.json --fixtures_folder ~/Chromatik/Fixtures/Entwined
python shrub.py --config $1/shrubs.json --fixtures_folder ~/Chromatik/Fixtures/Entwined
python tree.py --tree_config $1/trees.json --branch_config $1/tree_branches.csv --fixtures_folder ~/Chromatik/Fixtures/Entwined
python bench.py --config $1/bench.json --fixtures_folder ~/Chromatik/Fixtures/Entwined
cp $1/entwined.lxp ~/Chromatik/Projects/
cp $1/autoplay.lxr ~/Chromatik/
sudo systemctl restart chromatik
