Bootstrap: docker
From: continuumio/miniconda3

%files
    board.py
    main.py
    config

%post
    conda install -y numpy
    pip install neat-python

%exec
    python main.py