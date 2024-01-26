import os
import chess
import chess.pgn
import numpy as np


def bit_encode(board: chess.Board):
    """
    Encodes a board state as a 774 "bitstring" which is an array of 1s or 0s.
    6 pieces * 64 squares * 2 colors = 768 + 6 bits for castling/to-move/en passant = 774 bits

    Args:
    - board (chess.Board): The board to be encoded.

    Returns:
    - List[int]: The encoded bitstring representing the board state.
    """

    bitstring = []  # Initialize an empty list to store the bits

    # Loop through each square on the chess board (64 squares in total)
    for num in range(64):
        if board.piece_at(num) is None:
            # If the square is empty, add 12 zeros to represent an empty square
            empty = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            bitstring += empty  # Concatenate the empty square bits to the bitstring
            continue

        # Define a mapping of chess piece symbols to binary representations
        bit_map = {
            "P": [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "N": [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "B": [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            "R": [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
            "Q": [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
            "K": [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],

            "p": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
            "n": [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
            "b": [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
            "r": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
            "q": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
            "k": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
        }

        temp = board.piece_at(num)  # Get the piece at the current square
        type_of_piece = temp.symbol()  # Get the symbol of the piece
        piece = bit_map[type_of_piece]  # Get the binary representation of the piece
        bitstring += piece  # Concatenate the piece bits to the bitstring

    # Add bits for castling rights, en passant, and side to move as additional info
    additional_info = [
        int(board.has_queenside_castling_rights(chess.WHITE)),
        int(board.has_kingside_castling_rights(chess.WHITE)),
        int(board.has_queenside_castling_rights(chess.BLACK)),
        int(board.has_kingside_castling_rights(chess.BLACK)),
        int(board.has_legal_en_passant()),
        int(board.turn == chess.WHITE)
    ]
    return bitstring, additional_info  # Return the final bitstring representing the board state and the additional info


def parse(testing_or_training: str):
    """d
    This function parses through the games (testing or training)
    and converts it into a numpy array of games and their results,
    that then saved into the respective data folder.

    Args:
    - testing_or_training (str): Which games folder to take the games from, testing or training.

    Returns:
    - None
    """

    # Initialize lists to store chess board positions (games), additional info and corresponding game outcomes (values)
    games = []
    values = []
    additional_info_list = []

    # Construct the path to the directory containing PGN files
    game_path = f"./{testing_or_training}_games"

    # Iterate over each PGN file in the specified directory
    for pgn_file in os.listdir(game_path):
        # Open the PGN file for reading
        with open(os.path.join(game_path, pgn_file)) as pgn:
            count = 0
            # Continue reading games until the end of the PGN file
            while True:
                try:
                    # Read the next game from the PGN file
                    sub_pgn = chess.pgn.read_game(pgn)
                except:
                    break  # Break out of the loop if there are no more games

                # Define a dictionary to map game outcomes to numerical values
                value_assign_dict = {'1-0': 1, '0-1': -1, '1/2-1/2': 0}

                try:
                    # Retrieve the outcome of the current game
                    game_value = value_assign_dict[sub_pgn.headers['Result']]
                except:
                    break  # Break out of the loop if the game outcome is not valid

                # Initialize a chess board for the current game
                temp_board = sub_pgn.board()

                count += 1
                print(f"Parsing {testing_or_training} game number {count}")

                # Iterate over the mainline moves of the current game
                for move in sub_pgn.mainline_moves():
                    # Update the chess board with the current move
                    temp_board.push(move)
                    # Encode the current board state using the bit_encode function
                    output, additional_info = bit_encode(temp_board)
                    # Separate the board representation and reshape it
                    board_representation = output[:768]  # First 768 elements are the board representation
                    reshaped_board = np.reshape(board_representation, (12, 8, 8))
                    games.append(reshaped_board)
                    # Handle the additional information separately in a separate list
                    additional_info_list.append(additional_info)
                    # Append the corresponding game outcome to the list of values
                    values.append(game_value)

    # Convert the lists to NumPy arrays for further processing
    games = np.array(games)
    values = np.array(values)
    additional_info_array = np.array(additional_info_list)

    # Ensure the directory exists before saving
    save_dir = f'data/{testing_or_training}/'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)  # This creates the directory and any parents if they don't exist

    # Save the encoded board positions and game outcomes to files
    np.save(f'{save_dir}positions.npy', games)
    np.save(f'{save_dir}results.npy', values)
    # Save the additional_info_array to files
    np.save(f'{save_dir}additional_info.npy', additional_info_array)

    # Print the number of games and values processed
    print(f"{testing_or_training}_games: {len(games)}")
    print(f"Values: {len(values)}")


def main():
    parse("training")
    parse("testing")


if __name__ == '__main__':
    main()
