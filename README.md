# QUGA: Quality Guarantees of Autoencoders via Unsupervised Adversarial Attacks.
This repository contains Code and supplementary material for the ECMLPKDD2020 Paper [Quality Guarantees for Autoencoders via Unsupervised Adversarial Attacks](http://ls9-www.cs.tu-dortmund.de/publications/ECMLPKDD2020.pdf).


## Usage

```bash
git clone git://github.com/KDD-OpenSource/QUGA.git  
virtualenv venv -p /usr/bin/python3  
source venv/bin/activate  
pip install -r requirements.txt  
python3 main.py
```

## Reproduction of Experiments:
To reproduce the results of the sine-curve dataset replace the contents of objectCreator.py by the contents in FullSynthetic.py. Then run "python3 main.py".
Similarly to reproduce the experiments with the ECG5000 Dataset replace the contents of objectCreator.py by the contents in FullReal.py.

## Authors/Contributors
* [Benedikt Böing](https://github.com/bboeing)
* [Rajarshi Roy](https://github.com/rajarshi008)
* [Emmanuel Müller](https://github.com/emmanuel-mueller)
* [Daniel Neider](https://github.com/daniel-neider)
