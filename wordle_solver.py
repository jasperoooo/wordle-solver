from collections import Counter

def load_words(file_path):
    with open(file_path, 'r') as file:
        return [line.strip().lower() for line in file]
    
def filter_words(words, correct, contained, incorrect):
    filtered_words = []
    for word in words:
        word_counter = Counter(word)
        if all(word[i] == ch for i, ch in correct.items()) and \
           all(word_counter[ch] >= count for ch, count in contained.items()) and \
           not any(ch in word for ch in incorrect):
            filtered_words.append(word)
    return filtered_words

def update_constraints(guess, feedback, correct, contained, incorrect):
    temp_contained = Counter() # Temporary counter to track 'y' feedback for this guess

    for i, (ch, fb) in enumerate(zip(guess, feedback)):
        if fb == 'g':   # Green - correct letter, correct position
            correct[i] = ch
        elif fb == 'y': # Yellow - correct letter, wrong position
            temp_contained[ch] += 1
        elif fb == 'b': # Black - letter not in word
            incorrect.add(ch)
        
    # Update the global 'contained' counter based on this guess's feedback
    for ch, count in temp_contained.items():
        if ch not in contained:
            contained[ch] = 0

        if contained[ch] < count:
            contained[ch] = count

def wordle_solver(file_path):
    words = load_words(file_path) # Load potential words from file
    correct, contained, incorrect = {}, Counter(), set()  # Initialize constraints

    while True:
        guess = input("Enter your guess: ").lower()  # User inputs their guess
        # Check if the guess is not exactly 5 letters
        if len(guess) != 5:
            print("Error: Guess must be exactly 5 letters. Please try again.")
            continue  # Skip the rest of the loop and prompt for input again

        feedback = input("Enter feedback as a 5 letter string, for example 'gyybg'. (g=green, y=yellow, b=black): ").lower()  # User inputs feedback for each letter of the guess
        # Check if the guess is not exactly 5 letters
        if len(guess) != 5:
            print("Error: Guess must be exactly 5 letters. Please try again.")
            continue  # Skip the rest of the loop and prompt for input again

        update_constraints(guess, feedback, correct, contained, incorrect)  # Update constraints based on feedback
        words = filter_words(words, correct, contained, incorrect)  # Filter words based on updated constraints

        # Check if the word has been guessed or if further refinement is possible
        if len(words) == 1:
            print(f"The word is: {words[0]}")
            break  # Exit loop if the word has been identified
        elif not words:
            print("No words found. Please check the inputs and try again.")
            break  # Exit loop if no words match the criteria (likely due to incorrect feedback)
        else:
            print(f"Possible words: {', '.join(words)}")  # Show remaining possible words

if __name__ == "__main__":
    test_variable = "Hello"
    wordle_solver(r'.\words.txt')