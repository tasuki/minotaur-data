# Minotaur Data

This repo contains some data-based stuff for the Minotaur project.

There's ~200k games downloaded from BGA in `data/bga-games-info.json`. The
various directories contain various ways of manipulating them.

## Install

Create a `virtualenv` or something. This might be non-standard. I can't Python.

    virtualenv -p /usr/bin/python3.5 env
    source env/bin/activate

Then install everything:

    pip install -r requirements.txt

## Scrape

This has been done already (see the `scrape` dir). The results are in
`/home/vita/data/prog/minotaur-data`.

## Analysis

There's a jupyter notebook analysing the data. Run `jupyter notebook` and
navigate to `analysis/Quoridor-BGA-stats.ipynb`.

## Munch

Before training anything, the data needs to be munched. Cd to `munch` and run
`bash process_games.sh`.

## NN

Here be dragons.

## Server

Run `python run_server.py` to cerwate a http interface for the quoridor nn.
