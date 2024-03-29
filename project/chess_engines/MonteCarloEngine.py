from project.chess_agents.MonteCarloAgent import MonteCarloChessAgent
from project.chess_utilities.nnUtility import nnUtility
from project.chess_engines.uci_engine import UciEngine

if __name__ == "__main__":
    # Create your utility
    utility = nnUtility()
    # Create your agent
    agent = MonteCarloChessAgent(5.0, 1.41, utility)
    # Create the engine
    engine = UciEngine("Monte Carlo Agent", "SB", agent)
    # Run the engine (will loop until the game is done or exited)
    engine.engine_operation()
