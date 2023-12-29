from project.chess_agents.MonteCarloAgent import MonteCarloChessAgent
from project.chess_utilities.enhanced_utility import EnhancedUtility
from project.chess_engines.uci_engine import UciEngine

if __name__ == "__main__":
    # Create your utility
    utility = EnhancedUtility()
    # Create your agent
    agent = MonteCarloChessAgent(utility, 5.0, 1.41)
    # Create the engine
    engine = UciEngine("Monte Carlo Agent", "SB", agent)
    # Run the engine (will loop until the game is done or exited)
    engine.engine_operation()
