import random
import time

def load_words(file):
    with open(file, "r", encoding="UTF-8") as f:
        words = [word.strip() for word in f.readlines()]
    words.sort()
    return words

def pick_a_word(words, used_words):
    remaining_words = [word for word in words if word not in used_words]
    if not remaining_words:
        return None
    return random.choice(remaining_words)

def puncture_word(word, n):
    target = random.sample(word, n)
    result = "".join(["_" if s in target else s for s in word])
    return result, target

def guess(word, quiz, target, hint_count):
    while True:
        c = input(f'Guess a character (a-z), or type "hint" ({hint_count} hints left): ')
        if c == "hint":
            if hint_count > 0:
                hint_count -= 1
                revealed_letter = random.choice(target)
                target = [x for x in target if x != revealed_letter]
                quiz = "".join(["_" if s in target else s for s in word])
                return quiz, target, hint_count
            else:
                print("No hints left.")
        elif len(c) == 1 and c.islower() and c.isalpha():
            break
        else:
            print("Invalid input. Please enter a single lowercase letter or type 'hint'.")
    
    if c in target:
        target = [x for x in target if x != c]
        quiz = "".join(["_" if s in target else s for s in word])
    else:
        print("Incorrect letter.")
        
    return quiz, target, hint_count

def get_theme():
    themes = {1: "animals", 2: "fruits", 3: "countries"}
    while True:
        try:
            theme_choice = int(input("Choose a theme (1: Animal, 2: Fruits, 3: Countries): "))
            if theme_choice in themes:
                return themes[theme_choice]
            else:
                print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_difficulty():
    while True:
        try:
            difficulty = int(input("Select game difficulty (Easy = 1, Medium = 2, Hard = 3): "))
            if difficulty in [1, 2, 3]:
                return difficulty
            else:
                print("Please enter an integer between 1 and 3.")
        except ValueError:
            print("Invalid input. Please enter an integer.")

def update_score(current_score):
    try:
        with open("score.txt", "r") as file:
            high_score = int(file.read().strip())
    except FileNotFoundError:
        high_score = 0
    
    if current_score > high_score:
        print(f"New high score! Your score: {current_score}")
        with open("score.txt", "w") as file:
            file.write(str(current_score))
    else:
        print(f"Your score: {current_score}. High score: {high_score}")

def main():
    while True:
        theme = get_theme()
        sorted_words = load_words(f"{theme}.txt")
        
        used_words = set()
        total_score = 0
        start_time = time.time()
        
        difficulty = get_difficulty()
        
        hint_count = 2
        game_ended = False
        while True:
            picked_word = pick_a_word(sorted_words, used_words)
            if not picked_word:
                print("No more words available in this theme.")
                break
            used_words.add(picked_word)
            
            m = len(picked_word)
            if difficulty == 1:
                n = m // 3
            elif difficulty == 2:
                n = m // 2
            else:
                n = m
            
            quiz_word, target = puncture_word(picked_word, n)
            
            while target:
                print(quiz_word)
                quiz_word, target, hint_count = guess(picked_word, quiz_word, target, hint_count)
                print(f"Time elapsed: {int(time.time() - start_time)} seconds")
                
                if time.time() - start_time > 60:
                    print("Time's up! Game over.")
                    
                    game_ended = True
                    break

            if game_ended:
                break

            if not target:
                if difficulty == 1:
                    total_score += 1
                elif difficulty == 2:
                    total_score += 2
                else:
                    total_score += 3
                print(f"Congratulations! The correct word is '{picked_word}'. Your score: {total_score}")
        
        update_score(total_score)
        play_again = input("Do you want to play another round? (Y/N): ").strip().upper()
        if play_again != 'Y':
            break

if __name__ == "__main__":
    main()
