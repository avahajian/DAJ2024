# DAJ2024

These codes are used to get the near optimal fixed lot size, reorder point, and time length. The simulation and optimization codes for fixed size lot are available provided in FixedLotCode and Opt_FL01 respectively. For fixed time lot the codes are provided in FT01 and Opt_FT01 respectively.

Optimization algorithmThe optimization code provides optimized values of Q, T, and r that minimizes the long-run average cost by utilizing a hybrid greedy and random walk algorithm. This hybrid algorithm is designed to reduce the chance that the solution found is not a local minima.

The search boundaries are selected for Q, T, and r by utilizing classical EOQ closed form results and outcomes from preliminary simulation runs. From the search boundaries, a random combination of Q or T, and r is generated and treated as candidate solution. The optimization algorithmcode provides input (candidate solution parameters) to the simulation model, and the simulation model provides an estimate of the long-run average cost and service level for the candidate solution.

If customer specified service level is obtained, the candidate solution is accepted as a best candidate solution, otherwise the algorithmcode keeps generating random combinations and runs the simulation model until the service level is obtained. From the best candidate solution the neighboring solutions are explored for a better solution. To search the neighborhood for a better solution, the best candidate solution is mutated, and the long-run average cost and service level is obtained. This is repeated until a better solution is obtained.

If a new candidate solution has a better long-run average cost than the current best candidate solution, it then becomes the best candidate solution. After n neighborhood searches with no improvement, a large random jump away from the best candidate solution is made. This ensures the search moves out of the region of a possible local minima and extends the search into other regions. After each random jump, m neighborhoods of the randomly generated parameters are searched for a better solution. The random jumps and m neighborhood search continues until no better solution is obtained.

The simulation optimization ends after a pre-defined number of search iterations are complete. At this time the best solution is reported. A pre-existing data set is used to validate the optimization algorithmcode.

Regrads,
Tiwari et al. (2024)
https://doi.org/10.1016/j.dajour.2024.100513
