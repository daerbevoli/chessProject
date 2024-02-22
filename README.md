We developed the chess agent with the following methods, a Monte Carlo Tree Search and a convolution neural network. 
However, when the neural network failed to deliver results, we switched to use an handwritten evaluation function. 
Below we will explain each method, how it works, why we chose it, how we implemented it and what results that it delivered. 
The Monte Carlo Tree Search will be referred to using its initials MCTS, 
the neural network using CNN and the handwritten evaluation function using HEF for here on out.

<br>
**Monte Carlo Tree Search**
<br>
The MCTS is a heuristic search algorithm for decision processes, most notably those employed in software that plays board games. 
MCTS is a method that relies on intelligent tree search that balances exploration and exploitation. 
It performs random sampling in the form of simulations and stores the statistics of actions to make more educated choices 
in each subsequent iteration. This is the reason that it is a very effective search algorithm for games with large state spaces 
like chess and Go. The MCTS consists of four phases: selection, expansion, simulation and backpropagation, discussed below.
<br>
![image](https://github.com/daerbevoli/chessProject/assets/101348238/3afc7370-d0f1-469f-85ee-dca13fe9dce5)

