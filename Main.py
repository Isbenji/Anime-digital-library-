import sqlite3
import bcrypt

# Database connection and setup
conn = sqlite3.connect("anime_library.db")
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users 
             (id INTEGER PRIMARY KEY, username TEXT NOT NULL, password TEXT NOT NULL)''')

c.execute('''CREATE TABLE IF NOT EXISTS anime 
             (id INTEGER PRIMARY KEY, title TEXT NOT NULL, genre TEXT NOT NULL, episodes INTEGER NOT NULL)''')
conn.commit()


class Anime:
    def __init__(self, title, genre, episodes):
        self.title = title
        self.genre = genre
        self.episodes = episodes

    def __str__(self):
        return f"{self.title} - {self.genre} - {self.episodes} episodes"


class AnimeLibrary:
    def add_anime(self, anime):
        with conn:
            c.execute("INSERT INTO anime (title, genre, episodes) VALUES (?, ?, ?)",
                      (anime.title, anime.genre, anime.episodes))

    def view_library(self):
        c.execute("SELECT * FROM anime")
        anime_list = c.fetchall()

        if not anime_list:
            print("Anime library is empty.")
            return

        print("Anime Library:")
        for anime in anime_list:
            print(f"{anime[1]} - {anime[2]} - {anime[3]} episodes")

    def search_anime(self, keyword):
        c.execute("SELECT * FROM anime WHERE title LIKE ?", ('%' + keyword + '%',))
        anime_list = c.fetchall()
        return [Anime(title, genre, episodes) for _, title, genre, episodes in anime_list]

    def update_anime(self, anime_id, new_title, new_genre, new_episodes):
        with conn:
            c.execute("UPDATE anime SET title = ?, genre = ?, episodes = ? WHERE id = ?",
                      (new_title, new_genre, new_episodes, anime_id))

    def delete_anime(self, anime_id):
        with conn:
            c.execute("DELETE FROM anime WHERE id = ?", (anime_id,))


class UserAuthentication:
    @staticmethod
    def create_user(username, password):
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        with conn:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, hashed_password))

    @staticmethod
    def authenticate_user(username, password):
        c.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = c.fetchone()

        if result and bcrypt.checkpw(password.encode("utf-8"), result[0]):
            return True
        else:
            return False


def main():
    print("Welcome to the Anime Library!")

    while True:
        print("\n===== Anime Library Menu =====")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")
        choice = input("Enter your choice (1/2/3): ")

        if choice == "1":
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            UserAuthentication.create_user(username, password)
            print("User created successfully!")

        elif choice == "2":
            username = input("Enter your username: ")
            password = input("Enter your password: ")

            if UserAuthentication.authenticate_user(username, password):
                library = AnimeLibrary()

                while True:
                    print("\n===== Anime Library Menu =====")
                    print("1. Add Anime")
                    print("2. View Library")
                    print("3. Search Anime")
                    print("4. Update Anime")
                    print("5. Delete Anime")
                    print("6. Log Out")
                    sub_choice = input("Enter your choice (1/2/3/4/5/6): ")

                    if sub_choice == "1":
                        title = input("Enter anime title: ")
                        genre = input("Enter anime genre: ")
                        episodes = int(input("Enter the number of episodes: "))
                        anime = Anime(title, genre, episodes)
                        library.add_anime(anime)
                        print(f"{title} has been added to the library!")

                    elif sub_choice == "2":
                        library.view_library()

                    elif sub_choice == "3":
                        keyword = input("Enter the keyword to search: ")
                        search_results = library.search_anime(keyword)
                        if search_results:
                            print("\nSearch Results:")
                            for anime in search_results:
                                print(anime)
                        else:
                            print("No anime found with the given keyword.")

                    elif sub_choice == "4":
                        anime_id = int(input("Enter the ID of the anime to update: "))
                        new_title = input("Enter the new anime title: ")
                        new_genre = input("Enter the new anime genre: ")
                        new_episodes = int(input("Enter the new number of episodes: "))
                        library.update_anime(anime_id, new_title, new_genre, new_episodes)
                        print("Anime information updated successfully!")

                    elif sub_choice == "5":
                        anime_id = int(input("Enter the ID of the anime to delete: "))
                        library.delete_anime(anime_id)
                        print("Anime deleted successfully!")

                    elif sub_choice == "6":
                        print("Logging out.")
                        break

                    else:
                        print("Invalid choice. Please try again.")

            else:
                print("Invalid username or password. Please try again.")

        elif choice == "3":
            print("Exiting the Anime Library.")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
