import streamlit as st
import numpy as np
import random

# 游戏参数
GRID_SIZE = 13  # 网格大小
SNAKE_SIZE = 1

# 表情符号定义
EMPTY = "⬛"  # 空地（黑色小方块）
SNAKE_HEAD = "🐍"  # 蛇头
SNAKE_BODY = "🟩"  # 蛇身
FOOD = "🍎"   # 食物

# 初始化游戏状态
if 'snake' not in st.session_state:
    st.session_state.snake = [[5, 5], [5, 4], [5, 3]]  # 贪吃蛇初始位置
    st.session_state.direction = 'RIGHT'  # 初始方向
    st.session_state.food = [0, 0]  # 食物位置
    st.session_state.score = 0  # 得分
    st.session_state.game_over = False  # 游戏状态
    st.session_state.food = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]  # 生成食物

# 显示游戏状态
def draw_game():
    grid = np.full((GRID_SIZE, GRID_SIZE), EMPTY)  # 初始化为 empty
    for index, segment in enumerate(st.session_state.snake):
        grid[segment[0], segment[1]] = SNAKE_HEAD if index == 0 else SNAKE_BODY
    grid[st.session_state.food[0], st.session_state.food[1]] = FOOD  # 食物部分
    return grid

# 生成新的食物位置
def generate_food(snake):
    while True:
        new_food = [random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1)]
        if new_food not in snake:  # 确保食物不生成在蛇身上
            return new_food

# 控制贪吃蛇的移动
def move_snake():
    if st.session_state.game_over:
        return

    head = st.session_state.snake[0]
    new_head = head.copy()

    direction_moves = {
        'UP': (-SNAKE_SIZE, 0),
        'DOWN': (SNAKE_SIZE, 0),
        'LEFT': (0, -SNAKE_SIZE),
        'RIGHT': (0, SNAKE_SIZE)
    }

    move = direction_moves[st.session_state.direction]
    new_head[0] += move[0]
    new_head[1] += move[1]

    # 检查游戏结束条件
    if (new_head[0] < 0 or new_head[0] >= GRID_SIZE or
        new_head[1] < 0 or new_head[1] >= GRID_SIZE or
        new_head in st.session_state.snake):
        st.session_state.game_over = True
        return

    # 移动贪吃蛇
    st.session_state.snake.insert(0, new_head)  # 添加新头部
    if new_head == st.session_state.food:  # 吃到食物
        st.session_state.score += 1
        st.session_state.food = generate_food(st.session_state.snake)  # 生成新的食物
    else:
        st.session_state.snake.pop()  # 移除尾部

# 控制方向
def set_direction(new_direction):
    opposite_directions = {
        'UP': 'DOWN',
        'DOWN': 'UP',
        'LEFT': 'RIGHT',
        'RIGHT': 'LEFT'
    }
    if new_direction != opposite_directions[st.session_state.direction]:
        st.session_state.direction = new_direction

# Streamlit 入口
st.title("贪吃蛇游戏")
if st.button("开始游戏") or st.session_state.game_over:
    st.session_state.snake = [[5, 5], [5, 4], [5, 3]]
    st.session_state.direction = 'RIGHT'
    st.session_state.score = 0
    st.session_state.game_over = False
    st.session_state.food = generate_food(st.session_state.snake)  # 生成新的食物

# 添加 JavaScript 代码来捕获键盘事件
st.markdown("""
    <script>
    document.onkeydown = function(e) {
        if (e.key == 'w') {
            document.getElementById("up").click();
        } else if (e.key == 's') {
            document.getElementById("down").click();
        } else if (e.key == 'a') {
            document.getElementById("left").click();
        } else if (e.key == 'd') {
            document.getElementById("right").click();
        }
    };
    </script>
""", unsafe_allow_html=True)

# 设置方向
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("上", key="up"):
        set_direction('UP')
with col2:
    if st.button("下", key="down"):
        set_direction('DOWN')
with col3:
    if st.button("左", key="left"):
        set_direction('LEFT')
with col4:
    if st.button("右", key="right"):
        set_direction('RIGHT')

# 移动贪吃蛇
move_snake()

# 显示游戏状态
game_grid = draw_game()
st.write(f"得分: {st.session_state.score}")
st.write("游戏状态:")
st.write(game_grid)

if st.session_state.game_over:
    st.write("游戏结束！请点击开始游戏重新开始。")
