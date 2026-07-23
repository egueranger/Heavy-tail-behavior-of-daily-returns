# Heavy-tail-behavior-of-daily-returns
This project analyzes the heavy‑tail behavior of daily log returns for the S&P500 index. We compute log returns, plot their distribution, and estimate the tail index for each stock.

Function histogram() plots the histogram of the empirical daily absolute log returns of the S&P500.

Function plot_tail() plots the empirical log-log tail against the Gaussian tail.

Function plot_qq() plots the QQ representation of both tails.

Function estimate_tail_index_ml() returns a tuple with the estimation of the tail index using a maximum-likelihood method. We only keep variations above threshold, typically 3 %. In our statistical model R1,...,Rn denote daily log returns above threshold, are independent and Pareto-distributed with scale parameters equal to the threshold, known, and shape parameter beta -tail index- is unknown. Such a model is justified by the Pickands-Balkema-De Haan theorem.
