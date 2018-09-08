Protein Alignment using Minimum Edit Distance
==============================================

The project on protein alignment was tasked upon us by our coursework in advanced algorithms during the 1st semester of the master's in machine learning. The project led us to define six main approaches for finding the minimum edit distances between randomly generated strings; Dynamic, Recursive, K-strip, Greedy, 'branch and bound' and 'divide and conquer' approaches. Having successfully realized the same, we proceeded on to employing the computationally and spatially efficient K-strip (with a linear predictor for the k value) approach in combination with a random forest classifier to classify 4000 protein strings with an accuracy of 88%.

File Descriptions 
------------------

- BranchBound.py - Branch and Bound Algorithm
- GreedyMy.py - Greedy Algorithm
- KstripModel.py - K-strip algorithm 
- LinearSpace.py - Linear Space version of dynamic programming algorithm
- EditDistanceDP_OOP.py - Classic dynamic programming algorithm
- Recursive.py - Pure recursive algorithm
- RunningTime.ipynb - Script for measuring the running time af the algorithms and plotting results. Should be run using IPython notebooks.
- report.pdf - group report for the project
- misc - folder for the additional files:
	- LinearmodelforoptimalK.py - script for Linear model which used to find optimal K in K-strip algorithm 
        - ProteinDatabaseModelandprocessing.ipynb - script for processing the protein database and classification model.
        

