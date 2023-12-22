#!/usr/bin/python3
from project.chess_engines.uci_engine import UciEngine
from project.chess_engines.enhanced_uci_engine import ImprovedUciEngine

import chess
from project.chess_agents.example_agent import ExampleAgent
from project.chess_utilities.example_utility import ExampleUtility

from project.chess_agents.minimax_agent import MinimaxAgent  # Import your MinimaxAgent
from project.chess_utilities.utility import Utility  # Import your Utility

if __name__ == "__main__":
    # Create your utility
    utility = ExampleUtility()
    # Create your agent
    agent = ExampleAgent(utility, 1)
    # Create the engine
    engine = UciEngine("Example engine", "Arne", agent)
    # Run the engine (will loop until the game is done or exited)
    engine.engine_operation()

    # Example usage
    # utility = Utility()  # Instantiate your Utility
    # agent = MinimaxAgent(utility, 5.0, 3)  # Instantiate your MinimaxAgent with desired parameters
    # engine = UciEngine("Enhanced Uci Engine", "S R", agent)
    # engine.engine_operation()
