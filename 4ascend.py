import tkinter ,pdb ,cProfile ,time ,sys ,random
from functools import partial

# sys.setrecursionlimit(1500)

class Chess_pieces():
    '''棋子类'''
    id = 0
    status = 0 # 0空 1有棋子 
    color = 0 # 0黑 1白
    my_Damage = 1 # 伤害

    def __init__(self, id = 0, status = 0, color = 0, my_Damage = 1):
        self.id = id
        self.status = status
        self.color = color
        self.my_Damage = my_Damage


class five_in_five(Chess_pieces):
    """四子棋类"""
    title = ""
    width = 0
    height = 0
    root = None 
    """主窗口"""
    canvas = None 
    """画布"""
    time = 0
    """记步器"""
    backdrop_color = "#888888"
    """背景颜色"""
    pieces_sum = []
    """所有位置"""
    Be_on_the_spot = []
    """在棋盘上的棋子ID"""
    acquiesce_HP = 6
    """默认血量"""
    black_HP = acquiesce_HP
    """黑子血量"""
    white_HP = acquiesce_HP
    """白子血量"""
    black_position_HP = None
    """黑子血量位置"""
    white_position_HP = None
    """白子血量位置"""
    attack_id = []
    """攻击的棋子位置id"""
    defend_id = []
    """防守的棋子位置id"""
    attack_sum = []
    """攻击的所有棋子id"""
    warfare = False 
    """是否处于战斗状态"""
    in_animation = False
    """是否处于动画状态"""
    variable_count = 0
    """变数计数器"""
    variable_sum = {}
    """所有变数"""
    recursion_situation_points = []
    """递归的局面分数"""

    def __init__(self,ming = '4ascend',width = 800,height = 600):
        self.title = ming
        self.width = width
        self.height = height

    def main(self):
        """主函数""" 
        self.root = tkinter.Tk()
        self.root.title(self.title)
        self.root.geometry(str(self.width) + "x" + str(self.height))
        self.canvas = tkinter.Canvas(self.root, width=self.width, height=self.height, bg=self.backdrop_color, bd=0, highlightthickness=0)
        self.canvas.pack()
        self.initialize() 
        self.main_ui()
        self.root.mainloop()
        pass


    def main_ui(self):
        """UI界面"""
        for n in range(0, 9):
            self.canvas.create_line(125, 50 + 62.5 * n, 675, 50 + 62.5 * n, tags="Chess_grid")
            self.canvas.create_line(150 + 62.5 * n, 25, 150 + 62.5 * n, 575, tags="Chess_grid")
        self.canvas.tag_lower("Chess_grid")
        self.black_position_HP = self.canvas.create_text(65, 40, text="HP:" + str(self.black_HP), font=("Arial", 20), fill="black")
        self.white_position_HP = self.canvas.create_text(740, 40, text="HP:" + str(self.white_HP), font=("Arial", 20), fill="white")
        tkinter.Button(self.root, text="退出", command=self.root.quit).pack() 


    def initialize(self):
        """初始化棋子"""
        for id in range(1, 82):
            position = self.my_id(id)
            canvas_id =  self.canvas.create_oval(position[0], position[1], position[2], position[3], fill="", width=2, outline="")
            self.canvas.tag_bind(canvas_id, '<Button-1>',partial(self.pieces,canvas_id))
            self.canvas.tag_bind(canvas_id, '<Enter>', partial(self.handle_enter,canvas_id))
            self.canvas.tag_bind(canvas_id, '<Leave>', partial(self.handle_leave,canvas_id))
            self.pieces_sum.append(Chess_pieces(id))


    def pieces(self, canvas_id, event):
        """改变棋子的状态"""
        if not self.in_animation:
            subscript = canvas_id - 1
            if self.pieces_sum[subscript].status==1:
                return
            elif self.time%2==0:
                print(f"黑子ID:{subscript}")
                self.Be_on_the_spot.append(canvas_id) 
                self.pieces_sum[subscript].color=0
                self.pieces_sum[subscript].status=1
                self.canvas.itemconfig(canvas_id, fill="black")
                self.check_win(canvas_id)
            else:
                print(f"白子ID:{subscript}")
                self.Be_on_the_spot.append(canvas_id)
                self.pieces_sum[subscript].color=1
                self.pieces_sum[subscript].status=1
                self.canvas.itemconfig(canvas_id, fill="white")
                self.check_win(canvas_id)
            print(f"time:{self.time}")
            self.time+= 1


    def handle_enter(self, canvas_id, event):
        if self.pieces_sum[canvas_id-1].status==1:
            # print(f"Enter event: canvas_id={canvas_id}")
            self.canvas.itemconfig(canvas_id,outline="blue")


    def handle_leave(self, canvas_id, event):
        if self.pieces_sum[canvas_id-1].status==1:
            # print(f"Leave event: canvas_id={canvas_id}")
            self.canvas.itemconfig(canvas_id,outline="")


    def my_id(self,id):
        """返回棋子的位置"""
        id -= 1
        position = [130, 30, 170, 70]
        position[0] += 62.5 * (id % 9)
        position[1] += 62.5 * (id // 9)
        position[2] += 62.5 * (id % 9)
        position[3] += 62.5 * (id // 9)
        return position


    def nearby_id(self,id):
        """计算附近棋子的id"""
        x , y ,x1, y1 ,x2 , y2= 3, 3, 3, 3, 0, 0
        Nearby_id = {i + id for i in range(-27, 28, 9) if 0 < i + id <= 81}
        Nearby = list(Nearby_id)
        Nearby.sort()
        gps_id = Nearby.index(id)
        if id%9<4 and id%9!=0:
            x1 = x = id%9-1
        if id%9>6:
            y1 = y = 9-id%9
        if id%9==0:
            y1 = y = 0
        Nearby_id.update(id + i for i in range(-x, y + 1))
        x = min(x, gps_id)
        y = min(y, gps_id)
        for i in Nearby:
            if i<id:
                if x>0 and i==Nearby[gps_id-x]:
                    Nearby_id.add(i-x)
                    x -= 1
                if y>0 and i==Nearby[gps_id-y]:
                    Nearby_id.add(i+y)
                    y -= 1
            elif i>id:
                if x1>0:
                    x2 += 1
                    Nearby_id.add(i-x2)
                    x1 -= 1
                if y1>0:
                    y2 += 1
                    Nearby_id.add(i+y2)
                    y1 -= 1
        return list(Nearby_id)


    def check_win(self,id):
        """判断是否获胜"""
        continuous , all_id = self.check_continuous(id,self.nearby_id(id))
        # print(f"Damage:{Damage}")
        if self.warfare:
            for canvas_id in self.attack_sum:
                if canvas_id != id :
                    self.canvas.itemconfig(canvas_id,fill="")
            self.ANIMATIONS_start(all_id)
            Damage = self.Injury_calculation(continuous, id, all_id)
            self.delete_variables(all_id)
            if len(all_id) != 1:
                self.produce_variables(True)
            for i in self.attack_sum + all_id:
                self.Be_on_the_spot.remove(i)
            if self.pieces_sum[id-1].color==0:
                if Damage <= 0:
                    self.white_HP += Damage
                else:
                    self.black_HP -= Damage
                print(f"白子血量:{self.white_HP}")
                print(f"黑子血量:{self.black_HP}")
                self.canvas.itemconfig(self.black_position_HP, text="HP:" + str(self.black_HP))
                self.canvas.itemconfig(self.white_position_HP, text="HP:" + str(self.white_HP))
            else:
                if Damage <= 0:
                    self.black_HP += Damage
                else:
                    self.white_HP -= Damage
                print(f"白子血量:{self.white_HP}")
                print(f"黑子血量:{self.black_HP}")
                self.canvas.itemconfig(self.black_position_HP, text="HP:" + str(self.black_HP))
                self.canvas.itemconfig(self.white_position_HP, text="HP:" + str(self.white_HP))
            if self.black_HP<=0:
                print("白胜！")
            elif self.white_HP<=0:
                print("黑胜！")
            return
        if continuous != 0:
            self.ANIMATIONS_start(all_id)
        self.produce_variables()
        self.variable_count += 1


    def check_continuous(self, id, nearby_id):
        """判断是否进攻或防守情况"""
        color = self.pieces_sum[id-1].color
        all_id = [id]
        Switch = False
        continuous = 0 #计数

        def check_direction(id, direction, nearby_id):
            count = 0
            step = directions[direction]
            for i in range(1, 4):
                next_id = id + i * step
                subscript = next_id - 1
                # print(f"next_id:{next_id}", end=" ")
                if 0 < next_id <= 81 and next_id in nearby_id and self.pieces_sum[subscript].status == 1 and self.pieces_sum[subscript].color == color:
                    if Switch:
                        all_id.append(next_id)
                        continue
                    count += 1
                else:
                    break
            return count
        
        directions = {
            'left': 1,
            'right': -1,
            'up_left': 10,
            'down_right': -10,
            'up': 9,
            'down': -9,
            'up_right': 8,
            'down_left': -8
        }
        opposites = {
            'left': 'right',
            'right': 'left',
            'up_left': 'down_right',
            'down_right': 'up_left',
            'up': 'down',
            'down': 'up',
            'up_right': 'down_left',
            'down_left': 'up_right'
        }
        
        for key in ['left', 'up_left', 'up', 'up_right']:
            total = check_direction(id, key, nearby_id) + check_direction(id, opposites[key], nearby_id)
        # print(f"{key}:{total}", end=" ")
            if total > 2:
                continuous += total
                Switch = True
                check_direction(id, key, nearby_id)
                check_direction(id, opposites[key], nearby_id)
                Switch = False

        if self.warfare and not continuous:
            return 1 ,all_id

        return continuous + 1 if continuous > 0 else 0 ,all_id


    def ANIMATIONS_start(self, all_id):
        """动画效果-开始"""
        def move_shapes(canvas_id, move_x, move_y, end, step=0):
            if step < 100:
                self.canvas.move(canvas_id, move_x, move_y)
                self.root.after(4, move_shapes, canvas_id, move_x, move_y, end, step + 1)
            elif end:
                self.in_animation = False
                # print(f"动画结束:{self.in_animation}")
                if self.defend_id:
                    self.ANIMATIONS_end()

        def move_piece(id, color, position):
            coordinate = self.my_id(id)
            canvas_id = self.canvas.create_oval(coordinate[0], coordinate[1], coordinate[2], coordinate[3], fill=color, width=0)
            canvas_all.append(canvas_id)
            end = (id == all_id[-1] or len(all_id) == 1)
            move_shapes(canvas_id, 
                        (position[0] - (coordinate[0] + coordinate[2]) / 2) / 100,
                        (position[1] - (coordinate[1] + coordinate[3]) / 2) / 100,
                        end)

        self.in_animation = True
        print(all_id)
        if len(all_id) == 1:
            piece = self.pieces_sum[all_id[0] - 1]
            color = "black" if piece.color == 0 else "white"
            position = [740, 92.5] if piece.color == 0 else [65, 92.5]
            canvas_all = self.defend_id
            self.warfare = False
            self.canvas.itemconfig(all_id[0], outline="")
            move_piece(all_id[0], color, position)
            return 

        first_piece = self.pieces_sum[all_id[0] - 1]
        color = "black" if first_piece.color == 0 else "white"
        position = [65, 92.5] if first_piece.color == 0 else [740, 92.5]

        if not self.warfare:
            canvas_all = self.attack_id
            self.attack_sum = all_id
            self.warfare = True
            for canvas_id in all_id:
                self.canvas.itemconfig(canvas_id, fill=self.backdrop_color)
        else:
            canvas_all = self.defend_id
            self.warfare = False

        for id in all_id:
            piece = self.pieces_sum[id - 1]
            piece.status = 0
            if not self.warfare:
                self.canvas.itemconfig(id, fill="")
            self.canvas.itemconfig(id, outline="")
            move_piece(id, color, position)

        canvas_all.append(self.canvas.create_text(position[0], position[1], text="x" + str(len(all_id)), font=("Arial", 20), fill="black" if color == "white" else "white"))
        # print(f"攻击方:{self.attack_id},防守方:{self.defend_id}")


    def ANIMATIONS_end(self):
        """动画效果-结束"""
        def move_shapes(canvas_id, move_x, end, step=0):
            if step < 100:
                self.canvas.move(canvas_id, move_x, 0)
                self.root.after(4, move_shapes, canvas_id, move_x, end, step+1)
            else:
                self.canvas.delete(canvas_id)
                self.in_animation = end

        if not self.in_animation and self.attack_id:
            self.in_animation = True
            if len(self.defend_id) != 1:
                position = [402.5, 92.5]
                coordinate = self.canvas.coords(self.attack_id[0])
                coordinate = position[0] - coordinate[0]
                move_x = coordinate / 100
                for canvas_id in self.attack_id:
                    move_shapes(canvas_id, move_x, True)
                move_x = - move_x
                for canvas_id in self.defend_id:
                    move_shapes(canvas_id, move_x, False)
            else:
                for canvas_id in self.attack_id:
                    self.canvas.delete(canvas_id)
                self.canvas.delete(self.defend_id[0])
                self.in_animation = False
            self.attack_id.clear()
            self.defend_id.clear()
 

    def Injury_calculation(self, continuous, id, all_id):
        """伤害计算"""
        attack_damages = [self.pieces_sum[i - 1].my_Damage for i in self.attack_sum]
        all_damages = [self.pieces_sum[i - 1].my_Damage for i in all_id]
        if continuous==1:
            if id in self.attack_sum:
                id_sum =  sum(attack_damages) - attack_damages[self.attack_sum.index(id)]
            else:
                id_sum = sum(attack_damages) - 1
        else:
            id_sum = sum(attack_damages) - sum(all_damages)

        for i in self.attack_sum + all_id:
            self.pieces_sum[i - 1].my_Damage = 1
        return id_sum


    def possibly_variables(self, all_id = []):
        """变数可能在的位置"""
        location_variables = []
        Excessive = []

        for id in self.Be_on_the_spot:
            k = id % 9
            Excessive.append(id)
            if k != 1 and self.pieces_sum[id - 2].status == 0:
                Excessive.append(id - 1)
            if k and self.pieces_sum[id].status == 0:
                Excessive.append(id + 1)
            
            for n in Excessive:
                k = n+9
                if k <= 81 and self.pieces_sum[n + 8].status == 0:
                    location_variables.append(k)
                k = n-9
                if k >= 1 and self.pieces_sum[n - 10].status == 0:
                    location_variables.append(k)

            Excessive.remove(id)
            location_variables = list(set(location_variables + Excessive + all_id))

        return location_variables


    def produce_variables(self, Switch = False):
        """生成变数"""
        k = len(self.Be_on_the_spot)/81

        if k <= 0.25:
            intensity = 10
            number = 2
        elif k <= 0.50:
            intensity = 8
            number = 2
        elif k <= 0.70:
            intensity = 6
            number = 3
        else:
            intensity = 2
            number = 4

        if Switch or self.variable_count >= intensity:
            self.variable_count = 0
            variables_sum = []

            if Switch:
                location_variables = self.possibly_variables(self.attack_sum)
                self.variable_count = 0
            else: 
                location_variables = self.possibly_variables()
            
            variables_sum = random.sample(location_variables, number)
            print("可能变数:",location_variables)
            print("\n生成变数:",variables_sum)

            for my in variables_sum:
                print("已生成变数:",my)
                self.pieces_sum[my - 1].my_Damage = 2
                coordinate = self.my_id(my)
                canvas_id = self.canvas.create_oval(coordinate[0], coordinate[1], coordinate[2], coordinate[3], fill="", width=8,outline="purple")
                self.variable_sum[str(my)] = canvas_id


    def delete_variables(self,all_id):
        """删除变数"""
        if len(all_id) == 1:
            delete_variables = [ x for x in self.attack_sum if x not in all_id]
        else:
            delete_variables = self.attack_sum + all_id
        for canvas_id in delete_variables:
            if str(canvas_id) in self.variable_sum:
                self.canvas.delete(self.variable_sum[str(canvas_id)])
                del self.variable_sum[str(canvas_id)]
                self.pieces_sum[canvas_id - 1].my_Damage = 1


    def Evaluation_function(self, scene_lists):
        """评估函数，返回评估值"""
        def convert_coordinates(id):
            """ID转换成坐标"""
            return (id - 1)//9,(id - 1)%9
        
        def convert_id(x,y):
            """坐标转换成ID"""
            return x*9 + y + 1
        
        def defend(nearby_id, color):
            """防守堵棋/进攻分数"""
            continuous = 0 #计数
            all_id = []
            Switch = False

            def check_direction(id, direction, nearby_id):
                count = 0
                step = directions[direction]
                for i in range(1, 4):
                    next_id = id + i * step
                    subscript = next_id - 1
                    if 0 < next_id <= 81 and next_id in nearby_id and pieces_sum[subscript].status == 1 and pieces_sum[subscript].color == color:
                        if Switch:
                            all_id.append(next_id)
                            continue
                        count += 1
                    else:
                        break
                return count
            
            directions = {
                'left': 1,
                'right': -1,
                'up_left': 10,
                'down_right': -10,
                'up': 9,
                'down': -9,
                'up_right': 8,
                'down_left': -8
            }
            opposites = {
                'left': 'right',
                'right': 'left',
                'up_left': 'down_right',
                'down_right': 'up_left',
                'up': 'down',
                'down': 'up',
                'up_right': 'down_left',
                'down_left': 'up_right'
            }

            for key in ['left', 'up_left', 'up', 'up_right']:
                total = check_direction(id, key, nearby_id) + check_direction(id, opposites[key], nearby_id)
                if total > 1:
                    continuous += total
                    Switch = True
                    check_direction(id, key, nearby_id)
                    check_direction(id, opposites[key], nearby_id)
                    Switch = False

            return continuous + 1 if continuous > 0 else 0 ,all_id

        def Search_continuity(color):
            """搜索连续"""
            Blacklist = [{(1, 0), (0, 1)}, {(1, 1), (0, 2), (2, 0)}, {(0, 7), (1, 8)}, {(1, 7), (0, 6), (2, 8)}, {(7, 0), (8, 1)}, {(8, 2), (7, 1), (6, 0)}, {(8, 7), (7, 8)}, {(6, 8), (7, 7), (8, 6)}]
            consecutive_two = []
            consecutive_three = []

            for i,j in [(0,1),(1,0),(1,1),(1,-1)]:#可优化把对角线的分开提升效率,但是麻烦
                for n in Be_on_the_spot:
                        x, y = convert_coordinates(n)
                        if pieces_sum[convert_id(x,y) - 1].status == 1 and pieces_sum[convert_id(x,y) - 1].color == color:
                            consecutive_indices = [(x,y)]

                            for r in range(1,3):
                                continuity_x = x + i * r
                                continuity_y = y + j * r

                                if 0 <= continuity_x < 9 and 0<= continuity_y < 9  and pieces_sum[convert_id(continuity_x,continuity_y) - 1].status == 1 and self.pieces_sum[convert_id(continuity_x,continuity_y) - 1].color == color:
                                    consecutive_indices.append((continuity_x,continuity_y))
                                else:
                                    break

                            if len(consecutive_indices) > 1:
                                Switch = True

                                for r in Blacklist:
                                    if consecutive_indices.issubset(r):
                                        Switch = False
                                        break

                                for r in consecutive_three:
                                    if consecutive_indices.issubset(r):
                                        Switch = False
                                        break

                                if Switch:
                                    if len(consecutive_indices) == 2:
                                        consecutive_two.append(consecutive_indices)
                                    elif len(consecutive_indices) == 3:
                                        consecutive_three.append(consecutive_indices)

            return consecutive_two,consecutive_three

        color, black_HP, white_HP, pieces_sum, Be_on_the_spot, attack_sum, warfare = scene_lists
        overall_mark = 0 #分数
        centrally = [31,32,33,40,41,42,49,50,51] #中心区域
        consecutive_two, consecutive_three = Search_continuity(color)
        consecutive_one = [] #单个棋子
        my_sum = [] #我的棋子
        enemy_sum = [] #敌方棋子

        for i in Be_on_the_spot:
            if pieces_sum[i - 1].color == color:
                my_sum.append(i)
                consecutive_one.append(convert_coordinates(i))
            else:
                enemy_sum.append(i)

        for i in consecutive_two+consecutive_three:
            for j in i:
                if j in consecutive_one:
                    del consecutive_one[consecutive_one.index(j)]

        if warfare: #防守模式
            max_mark = 0
            for n in my_sum:
                Nearby_id = self.nearby_id(n)
                my, all_id = defend(Nearby_id, color)
                if my > 3:
                    for n1 in all_id:
                        mark += pieces_sum[n1 - 1].my_Damage
                    if mark > max_mark:
                        max_mark = mark
            if max_mark > 0:
                overall_mark += 100 * max_mark
            else:
                for n in attack_sum:
                    if pieces_sum[n - 1].my_Damage > 1:
                        overall_mark += 15 

        overall_mark += len(consecutive_two)*25 + len(consecutive_three)*40 #连续两个和三个的分数
        enemy_color = 0 if color == 1 else 1 #敌方颜色

        for x,y in consecutive_one: #计算单个棋子的分数
            my_id = convert_id(x,y) 
            Nearby_id = self.nearby_id(my_id)
            if pieces_sum[my_id - 1].my_Damage > 1:    #变数的加分
                overall_mark += 15
            if my_id in centrally: #中心区域的加分
                overall_mark += 1
            overall_mark += defend(Nearby_id, enemy_color)[0] * 10   #防守堵棋分数

            
        overall_mark += (black_HP - white_HP) * 100 if color == 0 else (white_HP - black_HP) * 100#HP分数

        if color == 0:  #黑白棋子的胜负分
            if white_HP <= 0:
                overall_mark += 100000
            elif black_HP <= 0:
                overall_mark -= 100000
        elif color == 1:
            if  black_HP <= 0:
                overall_mark += 100000
            elif white_HP <= 0:
                overall_mark -= 100000

        return overall_mark, color, black_HP, white_HP, pieces_sum, Be_on_the_spot, attack_sum, warfare
    

    def Decision_making(self, color):
        """决策函数"""
        def Renewal(id, scene_lists):
            """更新棋盘"""

            color = scene_lists[1]
            black_HP = scene_lists[2]
            white_HP = scene_lists[3]
            pieces_sum = scene_lists[4]
            Be_on_the_spot = scene_lists[5]
            attack_sum = scene_lists[6]
            warfare = scene_lists[7]

            def Injury_calculation(continuous, id, all_id, pieces_sum, attack_sum):
                """伤害计算"""
                attack_damages = [pieces_sum[i - 1].my_Damage for i in attack_sum]
                all_damages = [pieces_sum[i - 1].my_Damage for i in all_id]
                if continuous==1:
                    if id in attack_sum:
                        Damage_sum =  sum(attack_damages) - attack_damages[attack_sum.index(id)]
                    else:
                        Damage_sum = sum(attack_damages) - 1
                else:
                    Damage_sum = sum(attack_damages) - sum(all_damages)

                for i in attack_sum + all_id:
                    pieces_sum[i - 1].my_Damage = 1
                return Damage_sum            

            def check_continuous(id, nearby_id, color):
                """判断是否进攻"""
                all_id = [id]
                Switch = False
                continuous = 0 

                def check_direction(id, direction, nearby_id):
                    count = 0
                    step = directions[direction]
                    for i in range(1, 4):
                        next_id = id + i * step
                        subscript = next_id - 1
                        if 0 < next_id <= 81 and next_id in nearby_id and pieces_sum[subscript].status == 1 and pieces_sum[subscript].color == color:
                            if Switch:
                                all_id.append(next_id)
                                continue
                            count += 1
                        else:
                            break
                    return count
                
                directions = {
                    'left': 1,
                    'right': -1,
                    'up_left': 10,
                    'down_right': -10,
                    'up': 9,
                    'down': -9,
                    'up_right': 8,
                    'down_left': -8
                }
                opposites = {
                    'left': 'right',
                    'right': 'left',
                    'up_left': 'down_right',
                    'down_right': 'up_left',
                    'up': 'down',
                    'down': 'up',
                    'up_right': 'down_left',
                    'down_left': 'up_right'
                }
                
                for key in ['left', 'up_left', 'up', 'up_right']:
                    total = check_direction(id, key, nearby_id) + check_direction(id, opposites[key], nearby_id)
                    if total > 2:
                        continuous += total
                        Switch = True
                        check_direction(id, key, nearby_id)
                        check_direction(id, opposites[key], nearby_id)
                        Switch = False

                return continuous + 1 if continuous > 0 else 0 ,all_id

            if warfare: #防守
                warfare = False
                continuous, all_id = check_continuous(id, self.nearby_id(id), color)
                Damage = Injury_calculation(continuous, id, all_id, pieces_sum, attack_sum)

                if color==0:
                    if Damage <= 0:
                        white_HP += Damage
                    else:
                        black_HP -= Damage
                else:
                    if Damage <= 0:
                        black_HP += Damage
                    else:
                        white_HP -= Damage

                for i in all_id:
                    Be_on_the_spot.remove(i)
                    pieces_sum[i - 1].my_Damage = 1
                for i in attack_sum:
                    pieces_sum[i - 1].my_Damage = 1

                attack_sum.clear()

            else:
                continuous, all_id = check_continuous(id, self.nearby_id(id), color)

                if continuous >= 4:
                    warfare = True
                    attack_sum.extend(all_id)
                    for i in all_id:
                        pieces_sum[i - 1].status = 0
                        Be_on_the_spot.remove(i)
                else:
                    my = pieces_sum[id - 1]
                    my.status, my.color = 1, color
                    Be_on_the_spot.append(id)

            color = 0 if color == 1 else 1 #切换颜色
            scene_lists = [color, black_HP, white_HP, pieces_sum, Be_on_the_spot, attack_sum, warfare]
            return scene_lists

        def max_damage(color):
            """最高伤害棋子"""
            max_mark = 0
            max_id = 0
            for n in self.pieces_sum:
                my = self.pieces_sum[n - 1]
                if my.status == 0:
                    my.color = color
                    continuous, all_id = self.check_continuous(n , self.nearby_id(n))
                    if continuous >= 4:
                        for n1 in all_id:
                            mark += self.pieces_sum[n1 - 1].my_Damage
                        if mark > max_mark:
                            max_mark = mark
                            max_id = n
            return max_id, max_mark
        
        if color == 1:
            enemy_color = 0
            enemy_HP = self.white_HP
        else:
            enemy_color = 1
            enemy_HP = self.black_HP

        if enemy_HP - (max_damage(color) - max_damage(enemy_color)) <= 0: #判断是否一锤定音
            return max_damage(color)[0]
        
        scene_lists = [color, self.white_HP, self.black_HP, self.pieces_sum, self.Be_on_the_spot, self.attack_sum, self.warfare] #当前场上的情况


        def maxmin_algorithm(scene_lists_depth, enemy_ourselves, alpha_beta = [float('-inf'), float('inf')], Recursive_depth = 5):
            """maxmin算法和alpha_beta剪枝优化"""
            mark_sum = []

            for chess_position in scene_lists_depth[3]:
                if chess_position not in scene_lists_depth[4]:
                    mark = self.Evaluation_function(scene_lists)
                    if enemy_ourselves: 
                        if mark > alpha_beta[1]:
                            alpha_beta[1] = mark
                        if mark > overall_mark:
                            overall_mark = mark
                        if mark > alpha_beta[0]:
                            alpha_beta[0] = mark
                        if mark < alpha_beta[1]:
                            break
                        enemy_ourselves = False
                    else:
                        if mark < alpha_beta[0]:
                            alpha_beta[0] = mark
                        if mark < overall_mark:
                            overall_mark = mark
                        if mark < alpha_beta[1]:
                            break
                        enemy_ourselves = True
                    mark_sum.append([mark,chess_position]) #分数和位置
                    scene_lists_after = Renewal(chess_position, scene_lists_depth)
                    if Recursive_depth == 0 or overall_mark > 90000:
                        break
                    maxmin_algorithm(scene_lists_after, enemy_ourselves, alpha_beta, Recursive_depth - 1)
                    
            
            
            self.recursion_situation_points.append(mark_sum) #记录每一步和分数





qwq = five_in_five("四子棋", 800, 600)
qwq.main()

