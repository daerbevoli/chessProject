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

  1. Selection<br>
  Starting from the root node of the game tree, the algorithm traverses down the tree by selecting nodes based on the Upper Confidence   Bound formula, depicted in the figure below. The first term vi is the exploitation term. The second term, which is the square-root     of log N/ni is the exploration term. This formula balances exploration and exploitation by considering the two values mentione
  above.

  ![image](https://github.com/daerbevoli/chessProject/assets/101348238/3afc7370-d0f1-469f-85ee-dca13fe9dce5)

  3. Expansion<br>
  Once we reach a promising node, we expand it by adding child nodes corresponding to the possible moves from the current game state.

  4. Simulation <br>
  From the expanded node, the algorithm preforms simulations to assess the node’s value. These simulation involve making random moves   until a terminal state is reached (win, lose or draw). The outcome of the simulations is used as an estimate of our node’s value.
  
  5. Backpropagation <br>
  In this phase, we backpropagate and update the result we found in the simulation phase to all the nodes in the random path we          traversed and up till the root node. This sets the value vi which is then used in the selection phase of the formula.

  ![image](https://github.com/daerbevoli/chessProject/assets/101348238/a148e2c6-0997-45c0-a735-d2fef3e78a24)

<br>
The algorithm differs in our case at the simulation phase. Since we have a certain time limit, the simulation stops before a           terminal state is reached. To evaluate the node that we reached up until that point, we used a CNN or a HEF. 
They are each discussed below.
<br><br>

**Evaluation function**
<br>
The HEF is a function that takes in a chess board and by taking into account the dynamic aspects of the game such as tactics and future moves, it assign a numerical value to the chessboard known as its utility. For the calculation of the utility, we used the following factors: material score, piece mobility, kings safety, pawn structure and pawns square tables. All of these factors and how they are implemented are discusses below. We assume from here on out that agent is the white player and the opponent is the black player. This means that the white pieces deliver positive utility values while black pieces deliver negative utility values. The utility of the board is the difference of the respective color utilities.
<br>

The material score refers to the score of the pieces left on the board. Each piece is assigned a value and the calculation is done by multiplying the amount of pieces of a type with its material value and summing up the products. For the implementation, we make a dictionary with the piece type as the key and its material value as the respective value. Then we just loop through the chessboard and add the value of the respective pieces to a variable.
<br>

The second factor is piece mobility. This is the ability of a chess piece to move around the board and control different squares. A piece with high mobility is generally considered more powerful and flexible, as it can reach a greater number of squares and contribute to various aspects of the game, such as controlling key central squares, attacking the opponent's pieces, or supporting strategic plans. A piece’s mobility influences its effectiveness and overall contribution to the game, the greater its mobility, the better. The implementation is as follows: penalize bishops with the amount of pawns on the same color (which reduces the bishops mobility, because the pawns block it), penalize the knights if they are too close to the edge and finally assign a higher weight to capturing moves and moves that control the center
<br>

The third factor is king’s safety. This refers to the safety of the king and is dependent on the following factors: pawn structure, how the pawn are structured around the king, castling rights, switching positions with the rook, open files and diagonals, that the king is not in the sight of a direct attack of a bishop or rook and timing of the kings movements. In the implementation, we evaluate the pawn structure by checking the row ahead of the king for pawns. The open files and diagonals are checked by checking the surrounding eight squares for attacks, the proximity of enemy pieces is calculated using the Manhatten distance and whether the king has castled is also checked.
<br>

The next factor is pawn structure. This refers to how the pawns are structured on the board and that can have an impact on the overall dynamics of the game. The implementation consists of three factors influencing the utility score for the pawn structure function, one positive and two negative. The first one is pawn chains, a pawn in a horizontal line that give a +1 utility, an isolated pawn where there are no pawns on either horizontal side and a doubled pawn, two pawns back to back in a column. The latter two factors give an utility of -1.
<br>

Finally we have the piece square table. The table assign positional values to each square on the board for a specific piece type. The overall positional score of the board is the summation of the piece types and their score in the table. The table that we used was from the Simplified Evaluation Function page on the chess programming wiki. Analyzing the table, we can conclude that it encourages pawns to move forward, knight and bishops to go to the center, rooks to avoid the side columns and queens avoid the borders.
All the result of the separate evaluations are weighted depending on the phase of the game. The phase is determined by the amount of pieces left on the board. With this you can choose on what evaluation to put more weight depending on what is important per phase.
The result of the HEF were not much better than the CNN. It won every game against itself if it was the first one to make a move. Against the ExampleAgent it never lost but always drew in extraordinary fashion, losing every piece except the king. This probably had to do with the fact that our agent cannot play endgames well. Against the Stockfish engine, it lost every game every time in about 20 total moves (so 10 halfmoves). Hypertuning the weights, the exploration value or any other factor did not change eventual results of the games.
<br>

Unfortunately, we did not get the result that we desired. The best way to improve going forward would be the neural network. We have looked at various implementation of a chess agent online that all implemented a neural network. We could also try an approach on combining the HEF and the CNN like recent version of the Stockfish engine. We do not believe that only the HEF as utility would deliver a better than decent chess AI, but decent is not yet reached either.






