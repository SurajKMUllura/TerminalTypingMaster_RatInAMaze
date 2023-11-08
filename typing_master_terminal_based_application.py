import json
import random
import time
import keyboard
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def update_leaderboard(username, wpm, category):
    # Load existing leaderboard
    try:
        with open('_internal/leaderboard.json', 'r') as file:
            leaderboard = json.load(file)
    except FileNotFoundError:
        leaderboard = []

    # Add new entry and sort the leaderboard
    leaderboard.append({"username": username, "wpm": wpm, "category": category})
    leaderboard = sorted(leaderboard, key=lambda x: x['wpm'], reverse=True)

    # Update the JSON file
    with open('_internal/leaderboard.json', 'w') as file:
        json.dump(leaderboard, file, indent=4)

def show_leaderboard():
    try:
        with open('_internal/leaderboard.json', 'r') as file:
            leaderboard = json.load(file)
            print("Leaderboard:")
            for idx, entry in enumerate(leaderboard, start=1):
                print(f"{idx}. {entry['username']} - {entry['wpm']} WPM in {entry['category']}")
    except FileNotFoundError:
        print("Leaderboard is empty.")

def load_words_from_json():
    # Load words from a JSON file
    with open('words.json', 'r') as file:
        words_data = json.load(file)
        return words_data['words']

def load_categories_from_json():
    with open('_internal/word_categories.json', 'r') as file:
        return json.load(file)

def main():
    print("Welcome to the Typing Test Game!")
    username = input("Enter your username: ")

    categories = load_categories_from_json()

    print("Press 'Ctrl + Q' at any time to quit the game.")

    while True:
        print("\nOptions:")
        print("1. Start Typing Test")
        print("2. Show Leaderboard")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")
        
        clear_screen()
        if choice == '1':
            # Randomly select a category
            for category in categories:
                print(category)
        
            selected_category = input("Enter the category you want to play: ")
            
            if selected_category in categories:
                print(f"\nCategory: {selected_category}")
                words = categories[selected_category]
                random.shuffle(words)

                start_time = time.time()
                end_time = start_time + random.uniform(30, 60)  # Set the test duration to 45 seconds

                current_word_index = 0
                correct_words = 0
                totalentry=0
                print("\nGame Duration: 30-60 seconds.\nType the following word:")
                while time.time() < end_time and current_word_index < len(words):
                    test_text = words[current_word_index]
                    print("\n")
                    print(test_text)


                    while True:
                        totalentry+=1
                        if keyboard.is_pressed('ctrl+q'):
                            print("\nExiting the Typing Test. Goodbye!")
                            return
                        
                        user_input = input()

                        if user_input == test_text:
                            current_word_index += 1
                            correct_words += 1
                            break

                        try:
                            user_input = keyboard.read_event().name
                        except KeyboardInterrupt:
                            break

                typing_duration = time.time() - start_time
                wpm = (correct_words / typing_duration) * 60 if typing_duration > 0 else 0

                print("\nEnd of the test.")
                print(f"Words Typed Correctly: {correct_words}")
                print(f"Accuracy: {(correct_words/totalentry)*100:.2f}%")
                print(f"Your Typing Speed: {wpm:.2f} WPM")

                update_leaderboard(username, wpm, category)
            else:
                print("Category Not Found")

        elif choice == '2':
            clear_screen()
            show_leaderboard()

        elif choice == '3':
            print("Exiting the Typing Test. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a valid option.")

if __name__ == "__main__":
    main()
