import turtle
import random
import time

# 初始化Turtle
screen = turtle.Screen()
screen.setup(width=800, height=600)
screen.bgcolor("black")
screen.title("分形树动画")

# 初始化画笔
pen = turtle.Turtle()
pen.speed(0)
pen.color("green")
pen.hideturtle()
pen.left(90)
pen.up()
pen.goto(0, -250)
pen.down()

# 绘制分形树函数
def draw_tree(branch_length, pen):
    if branch_length > 5:
        pen.forward(branch_length)
        angle = random.randint(15, 45)
        pen.right(angle)
        draw_tree(branch_length - random.randint(10, 20), pen)
        pen.left(2 * angle)
        draw_tree(branch_length - random.randint(10, 20), pen)
        pen.right(angle)
        pen.backward(branch_length)

# 动态绘制函数
def draw_dynamic_tree(branch_length, pen):
    if branch_length > 5:
        pen.forward(branch_length)
        angle = random.randint(15, 45)
        pen.right(angle)
        draw_dynamic_tree(branch_length - random.randint(10, 20), pen)
        pen.left(2 * angle)
        draw_dynamic_tree(branch_length - random.randint(10, 20), pen)
        pen.right(angle)
        pen.backward(branch_length)
        time.sleep(0.02)  # 延迟以显示动画效果

# 主函数
def main():
    draw_dynamic_tree(100, pen)
    screen.mainloop()

if __name__ == "__main__":
    main()

