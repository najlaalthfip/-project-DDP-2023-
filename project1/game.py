import tkinter as tk
import random
import ttkbootstrap as tb
from PIL import Image, ImageTk

#Pengaturan window dan root tkinter juga ttkbootstrap
window = tk.Tk()
root = tb.Window(themename="morph")
window.title('Snake Game')

#Mengganti logo icon
window.iconbitmap('C:\\xampp\htdocs\ddp\project1\icon.ico') #Sesuaikan file direktori gambar icon

#Pengaturan gambar background
background_image = Image.open('C:\\xampp\htdocs\ddp\project1\gamebackground.png')  #Sesuaikan file direktori background
#Resize gambar background tkinter
bg_image_tk = ImageTk.PhotoImage(background_image)

#Buat label sebagai latar belakang dengan gambar
background_label = tk.Label(window, image=bg_image_tk)
background_label.place(relwidth=1, relheight=1) 

#Pengaturan Default
GAME_WIDTH = 800
GAME_HEIGHT = 700
SPEED = 300
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

#Kelas untuk mengatur ular (snake)
class Snake:
    #Metode konstruktor sebagai parent class atau kelas yang diwarisi atau kelas dasar dari ularnya
    def __init__(self):
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []
        
        #Pengaturan awal titik awal ular berada
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        #Membuat bentuk ular persegi
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

#Kelas untuk mengatur makanan ular
class Food:
    #Metode konstruktor sebagai parent class atau kelas yang diwarisi atau kelas dasar dari makanan ularnya
    def __init__(self):
        #Menentukan titik acak untuk makanan ularnya
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE)-1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x, y]

        #Membuat makanan ular berbentuk oval
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

#Fungsi untuk langkah selanjutnya dalam permainan
def next_turn(snake, food):
    global direction

    x, y = snake.coordinates[0]

    #Memperbarui titik berdasarkan arah pergerakan
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    #Memperbarui titik ular
    snake.coordinates.insert(0, (x, y))

    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)

    snake.squares.insert(0, square)

    #Menangani interaksi ular dengan makanan
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 50
        label.config(text="Your Score Snake Game:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        #Jika ular tidak makan makanan, ular bergerak tanpa penambahan panjang
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    #Memeriksa tabrakan ular dengan dinding atau tubuhnya sendiri
    if check_collisions(snake):
        game_over()
    else:
        window.after(SPEED, next_turn, snake, food)

#Fungsi untuk mengubah arah gerak ular
def change_direction(new_direction):
    global direction

    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction
    elif new_direction == 'right':
        if direction != 'left':
            direction = new_direction
    elif new_direction == 'up':
        if direction != 'down':
            direction = new_direction
    elif new_direction == 'down':
        if direction != 'up':
            direction = new_direction

#Fungsi untuk memeriksa tabrakan ular
def check_collisions(snake):
    x, y = snake.coordinates[0]

    if x < 0 or x >= GAME_WIDTH:
        return True
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

#Fungsi untuk menampilkan game over
def game_over():
    canvas.delete(tk.ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")

#Pengaturan awal skor dan arah gerak
score = 0
direction = 'down'

#Membuat label untuk menampilkan skor
label = tk.Label(window, text="Your Score Snake Game:{}".format(score), font=('consolas', 20))
label.pack()

#Membuat canvas untuk game
canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

#Mendapatkan dimensi jendela dan layar untuk penempatan jendela di tengah layar
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

#Menempatkan jendela di tengah layar
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

#Mengikat tombol keyboard dengan arah gerak ular
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

#Memulai snake game
snake = Snake()
food = Food()
next_turn(snake, food)

#Menjalankan aplikasi
window.mainloop()
