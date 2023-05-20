# Data we need to build/train a model:
# Our cards and their values, so our model can base hitting/standing on our total
# The dealer's up card
# Winning or losing - we can pair this to every possible situation (eg. hitting on a total of x when the up card is y)
# Use classification rather than regression? (win/lose/tie)

# Architecture:
# Agent knows starting hand (must be hand, not total, because of aces) and dealer's up card
# Agent hits or stands (for now) and records the hit or the stand in temporary memory
# Once the agent loses or wins (the dealer plays his hand out) the temporary data is put into the dataset
#   - This could be a multidimensional matrix to handle all inputs (cards, dealer's card, hitting/standing, win/lose)
#   - Run an algorithm to build a classification model on this data, and the agent will then make choices depending
# Repeat and hope it works



# # caller.py

# import subprocess

# # Spawn the terminal process
# terminal_process = subprocess.Popen(['C:/Users/Jesse Palmer/AppData/Local/Programs/Python/Python311/python.exe', 'c:/Users/Jesse Palmer/Documents/Projects/Casino Games/blackjackAI.py'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

# # Send input to the terminal process
# input_str = "bob\n" # Hardcoded input with a newline character
# terminal_process.stdin.write(input_str.encode())
# terminal_process.stdin.flush()

# # Read output from the terminal process
# output_str = terminal_process.stdout.readline().decode().strip()
# print(output_str) # Output: Hello, bob!
