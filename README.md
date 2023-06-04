# Tetris
大二python作业
用pygame实现俄罗斯方块小游戏
#代码逻辑

首先导入所需的模块和库：pygame和random。

定义一些常量和变量，包括游戏窗口的尺寸、游戏区域的尺寸、方块尺寸和颜色等。

初始化Pygame并创建游戏窗口。

Block（方块类）：
__init__(self, x, y, shape, color) 方法是类的构造函数，用于初始化方块对象的属性。它接受四个参数：

x 和 y 表示方块的左上角在游戏窗口中的位置坐标。
shape 是一个二维列表，表示方块的形状。列表中的元素为 0 或 1，0 表示方块的空白部分，1 表示方块的实心部分。
color 是一个 RGB 颜色元组，表示方块的颜色。

draw(self) 方法用于绘制方块。它使用嵌套的循环遍历方块的形状列表，根据每个元素的值判断是否绘制方块的实心部分。如果是实心部分，就创建一个矩形对象 rect，然后使用 pygame.draw.rect() 函数在游戏窗口上绘制这个矩形，颜色为方块的颜色。同时，还使用 pygame.draw.rect() 函数绘制一个白色的矩形框，用于突出显示方块的轮廓。

这样，每当需要在游戏窗口上绘制方块时，可以创建一个 Block 对象，并调用 draw() 方法进行绘制。

PlayArea（游戏区域类）：
__init__(self) 方法是类的构造函数，用于初始化游戏区域对象。它创建了一个二维列表 grid，表示游戏区域的网格。初始时，所有网格单元的颜色都被设置为黑色 (BLACK)。

draw(self) 方法用于绘制游戏区域。它使用嵌套的循环遍历游戏区域的网格列表，根据每个网格单元的颜色值，在游戏窗口上绘制一个与单元大小相等的矩形，颜色为网格单元的颜色。同时，还使用 pygame.draw.rect() 函数绘制一个白色的矩形框，用于突出显示网格单元的边界。

is_collision(self, block) 方法用于检查给定的方块对象是否与游戏区域的边界或已经放置的方块发生碰撞。它遍历方块的形状列表，并根据方块的位置和形状与游戏区域的网格进行对应。如果方块形状中的非空格与游戏区域中的非黑色网格单元相遇，或者方块的位置超出了游戏区域的边界，则返回 True，表示发生碰撞；否则返回 False，表示未发生碰撞。

can_moveleft(self, block) 方法用于检查给定的方块对象是否可以向左移动。它遍历方块的形状列表，并根据方块的位置和形状与游戏区域的网格进行对应。如果方块形状中的非空格的左侧格子超出了游戏区域的边界，或者左侧格子已经被其他方块占据，则返回 False，表示不能向左移动；否则返回 True，表示可以向左移动。

can_moveright(self, block) 方法用于检查给定的方块对象是否可以向右移动。它遍历方块的形状列表，并根据方块的位置和形状与游戏区域的网格进行对应。如果方块形状中的非空格的右侧格子超出了游戏区域的边界，或者右侧格子已经被其他方块占据，则返回 False，表示不能向右移动；否则返回 True，表示可以向右移动。

add_block(self, block) 方法用于将给定的方块对象加入到游戏区域的网格中。它遍历方块的形状列表，并根据方块的位置和形状与游戏区域的网格进行对应。对于方块形状中的非空格，将其对应的网格单元的颜色设置为方块的颜色。

remove_complete_rows(self, score) 方法用于移除已经填满的完整行，并更新得分。它遍历游戏区域的网格列表，对于每一行，如果该行所有网格单元的颜色不是黑色 (BLACK)，则将该行的索引添加到 complete_rows 列表中，并将得分增加 10 分。接着，对于 complete_rows 中的每一行索引，从游戏区域的网格列表中删除该行，并在游戏区域的顶部插入一行新的黑色网格单元。最后，返回更新后的得分。

Tetris（俄罗斯方块类）：
__init__(self) 方法是类的构造函数，用于初始化游戏对象。它初始化了当前方块 (current_block) 和下一个方块 (next_block)，创建了游戏区域对象 (play_area)，设置了初始得分 (score)、上次方块下落时间 (last_fall_time) 和下落速度 (speed)。

get_random_block(self) 方法用于随机选择并创建一个方块对象。它从预定义的方块形状列表中随机选择一个形状，并随机选择一个颜色。然后根据游戏区域的位置和偏移进行调整，并返回创建的方块对象。

draw_game_over(self) 方法用于在游戏结束时绘制 "Game Over" 的提示信息。它使用 pygame.font.Font 创建字体对象，并使用 render 方法创建包含提示文本的图像。然后使用 blit 方法将图像绘制到游戏窗口上。

change_speed(self, score) 方法用于根据得分调整方块下落的速度。它根据预定义的速度等级和对应的得分范围，选择合适的速度返回。

update(self) 方法用于更新游戏状态。它首先获取当前时间，然后根据速度和时间间隔判断是否应该让当前方块下落一格。如果方块可以下落，则更新方块的位置。如果方块发生碰撞，则将方块加入游戏区域并移除完整的行。如果方块加入游戏区域后导致碰撞发生，则游戏结束。最后，调用 draw 方法绘制游戏界面。

draw(self) 方法用于绘制游戏界面。它首先使用黑色 (BLACK) 填充游戏窗口。然后分别绘制游戏区域、当前方块、得分和下一个方块。使用 pygame.draw.rect 绘制游戏区域和侧边栏的矩形框，并使用 pygame.draw.line 绘制网格线。最后使用 pygame.display.update 更新显示。

draw_score(self) 方法用于绘制当前得分。它创建字体对象，并使用 render 方法创建包含得分信息的图像。然后使用 blit 方法将图像绘制到侧边栏上。

draw_next_block(self) 方法用于绘制下一个方块的预览。它首先绘制 "Next Block:" 的文本，然后使用方块的形状和颜色在侧边栏上绘制下一个方块的预览。

game_over(self) 方法用于处理游戏结束的情况。它首先调用 draw 方法绘制游戏界面，然后调用 draw_game_over 方法绘制 "Game Over" 的提示信息。最后使用 pygame.display.update 更新显示，延迟一段时间后退出游戏。

move_left(self)、move_right(self) 和 move_down(self) 方法用于处理方块的左移、右移和下移操作。它们首先检查方块是否可以移动，如果可以，则更新方块的位置，并调用 update 方法更新游戏状态。

rotate_block(self) 方法用于处理方块的旋转操作。它首先保存当前方块对象，然后根据旋转规则计算旋转后的方块形状。创建一个新的方块对象并设置旋转后的属性。接着检查旋转后的方块是否与边界或已停止的方块发生碰撞，如果没有发生碰撞，则更新为旋转后的方块。

游戏主循环

这是游戏的主循环部分。它使用一个无限循环来不断更新游戏状态，并处理用户的输入。

首先，创建一个 pygame.time.Clock 对象 clock，用于控制游戏循环的速度。
创建一个 Tetris 对象 tetris，用于管理游戏逻辑和交互。
在主循环中：

使用 pygame.event.get() 获取当前发生的所有事件。

遍历事件列表，对于每个事件：

如果事件的类型是 pygame.QUIT，表示用户关闭了游戏窗口，此时退出游戏。
如果事件的类型是 pygame.KEYDOWN，表示用户按下了键盘上的某个键：
如果按下的是左箭头键 (pygame.K_LEFT)，调用 tetris.move_left() 方法，使方块向左移动。
如果按下的是右箭头键 (pygame.K_RIGHT)，调用 tetris.move_right() 方法，使方块向右移动。
如果按下的是上箭头键 (pygame.K_UP)，调用 tetris.rotate_block() 方法，使方块进行旋转。
如果按下的是下箭头键 (pygame.K_DOWN)，调用 tetris.move_down() 方法，使方块加速下落。
调用 tetris.update() 方法更新游戏状态。

使用 clock.tick(60) 控制游戏循环以每秒最多运行 60 次。

通过这样的循环，游戏能够持续更新和处理用户输入，实现了一个完整的游戏循环。
