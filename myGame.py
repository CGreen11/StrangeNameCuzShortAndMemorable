import random

'''
游戏规则;
1:至少两个玩家；
2:每个玩家5张牌：
3:牌有1<2，2<3,3<1，每张牌数量未知
4:比大小，（1）比拼牌归位，（2）胜者可交换点数以内任意牌，（3）败者获得胜者手中一张牌并弃一张牌
5:两人以上胜利条件：手牌先清空；平局：手牌均相等
6：两人：手牌均大于对方；可理解为上帝视角不换能赢，因为只要换就有随机性，帮助玩家确认应不应该换
'''


class Card():
    card_type = [1, 2, 3]

    def __init__(self):
        self.card_type = card_type[get_random_int(len(card_type))]
        pass

    # 初始化手牌
    @classmethod
    def init_hand_cards(cls, card_num, default_card_type):
        hand_cards = []
        for i in range(card_num):
            card = default_card_type[get_random_int(len(default_card_type))]
            hand_cards.append(card)
        return hand_cards

    # 手牌比较 1 大于， 0 相等， -1 小于
    @classmethod
    def compare_card(cls, card_a, card_b):
        if card_a == card_type[-1] and card_b == card_type[0]:
            return -1
        elif card_a == card_type[0] and card_b == card_type[-1]:
            return 1
        elif card_a > card_b:
            return 1
        elif card_a < card_b:
            return -1
        else:
            return 0

    # 手牌整理
    @classmethod
    def sort_cards(cls, cards):
        # my_print("洗牌前=%s" % cards)
        cards = sorted(cards)
        # my_print("洗牌后=%s" % cards)
        # 冒泡 3 < -1
        # for i in range(len(cards)):
        #     for j in range(i, len(cards)):
        #         if compare_card(cards[i], cards[j]) == cards[i]:
        #             t = cards[j]
        #             cards[j] = cards[i]
        #             cards[i] = t
        return cards

    # 从cards中获得num个任意手牌
    @classmethod
    def get_card_by_num(cls, num, cards):
        num = num if num < len(cards) else len(cards)
        cards = cls.wash_cards(cards)
        # print("num=%s, cards=%s" % (num, cards))
        return cards[:num], cards[num:]

    # 手牌打乱
    @classmethod
    def wash_cards(cls, cards):
        # my_print("打乱前=%s" % cards)
        # 1/n 的概率出现在某一位置上
        card_index_list = random_index_list(len(cards))
        # 利用随机下标打乱手牌
        for i in range(len(card_index_list)):
            card_index_list[i] = cards[card_index_list[i]]
        # my_print("打乱后=%s" % card_index_list)
        return card_index_list

    # 手牌替换，并返回获取结果，即替换结果 外部需要保证wait_switch_cards <= target_switch_cards
    @classmethod
    def switch_cards(cls, wait_switch_cards, target_switch_cards):
        switched_cards, target_switch_cards = cls.get_card_by_num(len(wait_switch_cards), target_switch_cards)
        target_switch_cards.extend(wait_switch_cards)
        return switched_cards, target_switch_cards

    # 手牌检查 1代表胜利 0代表继续 -1代表平局 -2代表失败
    @classmethod
    def check_cards_state(cls, cards_a, cards_b):
        # and len(cards_a) > 1
        # 基本思路：手牌没有就是赢
        if not cards_a:
            return GAME_WIN
        if not cards_b:
            return GAME_LOSE
        # 上帝视角协助玩家判断思路：不换牌即可赢
        # 当场上有全种类的牌，不换牌不一定赢
        total_cards = []
        total_cards.extend(cards_a)
        total_cards.extend(cards_b)
        if set(total_cards) >= set(card_type):
            return GAME_GO_ON
        # 双方整理手牌
        cards_a = cls.sort_cards(cards_a)
        cards_b = cls.sort_cards(cards_b)
        # 双方清一色手牌
        if cls.compare_card(cards_a[0], cards_a[-1]) == 0 \
                and cls.compare_card(cards_b[0], cards_b[-1]) == 0:
            # 清一色 一样
            if cls.compare_card(cards_a[0], cards_b[0]) == 0:
                return GAME_BALANCE
            # 清一色 小张
            elif cls.compare_card(cards_a[0], cards_b[0]) == -1:
                return GAME_LOSE
            # 清一色 大张
            else:
                return GAME_WIN
        # 存在清一色,类似套被单，抓住两角，抖动之后即可平整
        if cls.compare_card(cards_a[0], cards_a[-1]) == 0 or cls.compare_card(cards_b[0], cards_b[-1]) == 0:
            # 两角不小于
            if cls.compare_card(cards_a[0], cards_b[0]) != -1 and cls.compare_card(cards_a[-1], cards_b[-1]) != -1:
                return GAME_WIN
            # 两角不大于
            if cls.compare_card(cards_a[0], cards_b[0]) != 1 and cls.compare_card(cards_a[-1], cards_b[-1]) != 1:
                return GAME_LOSE
        return GAME_GO_ON


class Gamer():
    def __init__(self, gamer_id, hand_cards):
        # 玩家标识
        self.gamer_id = gamer_id
        # 当前手牌
        self.hand_cards = hand_cards
        # 上次手牌
        self.history_hand_cards = []
        # 打出手牌
        self.show_card = -1

    # 上次手牌 通过热键监听触发手牌回溯
    def set_history_hand_cards(self, history_hand_cards):
        self.history_hand_cards = history_hand_cards
        pass

    # 打出手牌
    def set_show_card(self, show_card):
        self.set_history_hand_cards(self.hand_cards)
        self.show_card = show_card
        pass

    # 当前手牌
    def set_hand_cards(self, hand_cards):
        self.hand_cards = hand_cards
        pass


# 随机下标
def random_index_list(num):
    index_list = []
    while len(index_list) != num:
        index_random = get_random_int(num)
        if not (index_random in index_list):
            index_list.append(index_random)
    return index_list


# [0, num)
def get_random_int(num):
    return random.randint(0, num - 1)


GAME_WIN = 1
GAME_GO_ON = 0
GAME_BALANCE = -1
GAME_LOSE = -2

# 牌的种类
card_type = [1, 2, 3]
# 初始牌数目
hand_card_num = 5
# 灯笼
lamp = "**********"
# 是否明牌
game_visible = False


# 加灯笼
def my_print(print_content=None):
    if print_content:
        print(lamp + print_content + lamp)
    else:
        print(lamp + lamp + lamp)
    pass


# 是否是数字
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False


# 交换手牌，gamer_type 1：代表胜者为机器人， -1：败者为机器人 0：双方均为玩家
def switch_cards_by_gamer(gamer_win, gamer_lose, gamer_type):
    # 交换上限：胜者出牌点数、手牌数，败者手牌数
    switch_len = gamer_win.show_card if gamer_win.show_card < len(gamer_lose.hand_cards) else len(gamer_lose.hand_cards)
    switch_len = switch_len if switch_len < len(gamer_win.hand_cards) else len(gamer_win.hand_cards)
    # 待换手牌下标
    wait_switch_index_list = []
    if gamer_type != 1:
        switch_card_index_list = input('请在%s中选择%s个以内的交换的牌下标（英文逗号分割）：' % (gamer_win.hand_cards, switch_len))
        if switch_card_index_list:
            switch_card_index_list = "".join(switch_card_index_list.split()).replace("，", ",")
            if switch_card_index_list.__contains__(","):
                switch_card_index_list = switch_card_index_list.split(",")
            else:
                switch_card_index_list = [switch_card_index_list]
            # print("待换手牌输入=%s" % switch_card_index_list)
            # 实际交换数量
            switch_len = switch_len if switch_len < len(switch_card_index_list) else len(switch_card_index_list)
            for i in range(switch_len):
                wait_switch_index = int(switch_card_index_list[i])
                if wait_switch_index < len(gamer_win.hand_cards):
                    wait_switch_index_list.append(wait_switch_index)
    else:
        wait_switch_num = get_random_int(switch_len)
        wait_switch_index_list = random_index_list(len(gamer_win.hand_cards))[:wait_switch_num]
    # 从后往前删除
    wait_switch_index_list = sorted(wait_switch_index_list)[::-1]
    # print("待换手牌下标=%s" % wait_switch_index_list)
    # 待换手牌
    wait_switch_cards = []
    for i in range(len(wait_switch_index_list)):
        wait_switch_cards.append(gamer_win.hand_cards.pop(wait_switch_index_list[i]))
    # 胜者换牌
    if len(wait_switch_cards) > 0:
        switched_cards, target_switch_cards = Card.switch_cards(wait_switch_cards, gamer_lose.hand_cards)
        gamer_win.hand_cards.extend(switched_cards)
        gamer_win.set_hand_cards(Card.sort_cards(gamer_win.hand_cards))
        gamer_lose.set_hand_cards(Card.sort_cards(target_switch_cards))
        print("胜者待换牌=%s，换牌获得=%s" % (wait_switch_cards, switched_cards))
    else:
        print("胜者放弃换牌")
    # 明牌
    if gamer_type != 1 or game_visible:
        print("胜者当前手牌=%s" % gamer_win.hand_cards)
    # 败者拿牌、弃牌
    take_card = gamer_win.hand_cards.pop(get_random_int(len(gamer_win.hand_cards)))
    gamer_lose.hand_cards.append(take_card)
    gamer_lose.set_hand_cards(Card.sort_cards(gamer_lose.hand_cards))
    if gamer_type != -1:
        while True:
            throw_card_index = input('请在%s中选择1个丢弃的牌下标：' % gamer_lose.hand_cards)
            if is_number(throw_card_index) and int(throw_card_index) < len(gamer_lose.hand_cards):
                throw_card_index = int(throw_card_index)
                break
    else:
        throw_card_index = get_random_int(len(gamer_lose.hand_cards))
    throw_card = gamer_lose.hand_cards.pop(throw_card_index)
    print("败者弃牌=[%s]， 拿牌=[%s]" % (throw_card, take_card))
    gamer_lose.set_hand_cards(Card.sort_cards(gamer_lose.hand_cards))
    # 明牌
    if gamer_type != -1 or game_visible:
        print("败者当前手牌=%s" % gamer_lose.hand_cards)
    return gamer_win, gamer_lose


# 人机作战
def game_start(robot_num):
    gamer_a = Gamer(888, Card.sort_cards(Card.init_hand_cards(hand_card_num, card_type)))
    gamer_robot = Gamer("robot", Card.sort_cards(Card.init_hand_cards(hand_card_num, card_type)))
    # gamer_robot_list = []
    # # 生成robot
    # for i in range(robot_num):
    #     gamer_robot = Gamer(i + 1, sort_cards(init_hand_cards(hand_card_num, card_type)))
    #     gamer_robot_list.append(gamer_robot)
    game_round = 1
    # 游戏继续
    while True:
        cards_state = Card.check_cards_state(gamer_a.hand_cards, gamer_robot.hand_cards)
        game_quit = True
        if cards_state == GAME_WIN:
            my_print()
            my_print("本局 %s 胜出" % gamer_a.gamer_id)
        elif cards_state == GAME_BALANCE:
            my_print()
            my_print("本局平局")
        elif cards_state == GAME_LOSE:
            my_print()
            my_print("本局 %s 胜出" % gamer_robot.gamer_id)
        else:
            my_print("本局第 %s 回合开始" % game_round)
            game_quit = False

        print("玩家=%s的牌面：%s" % (gamer_a.gamer_id, gamer_a.hand_cards))
        if game_quit or game_visible:
            print("robot=%s的牌面：%s" % (gamer_robot.gamer_id, gamer_robot.hand_cards))
        #   退出游戏
        if game_quit:
            my_print()
            break

        # 玩家出牌
        while True:
            show_card_index = input('%s 中出牌下标：' % gamer_a.hand_cards)
            if is_number(show_card_index) and int(show_card_index) < len(gamer_a.hand_cards):
                gamer_a.set_show_card(gamer_a.hand_cards[int(show_card_index)])
                break
        # # robot出牌
        # for i in range(robot_num):
        #     show_card_index_robot = get_random_int(len(gamer_robot_list[i].hand_cards))
        #     gamer_robot_list[i].set_show_card(gamer_robot_list[i].hand_cards[show_card_index_robot])
        show_card_index_robot = get_random_int(len(gamer_robot.hand_cards))
        gamer_robot.set_show_card(gamer_robot.hand_cards[show_card_index_robot])
        print("玩家出牌=[%s]，robot出牌=[%s]" % (gamer_a.show_card, gamer_robot.show_card))

        # 比拼
        compare_result = Card.compare_card(gamer_a.show_card, gamer_robot.show_card)
        # 胜者可交换点数以内任意牌，败者获得胜者手中一张牌并弃一张牌
        if compare_result == 1:
            print("此回合 %s 胜出" % gamer_a.gamer_id)
            gamer_a, gamer_robot = switch_cards_by_gamer(gamer_a, gamer_robot, -1)
        elif compare_result == -1:
            print("此回合 %s 胜出" % gamer_robot.gamer_id)
            gamer_robot, gamer_a = switch_cards_by_gamer(gamer_robot, gamer_a, 1)
        else:
            print("此回合平局")
        game_round = game_round + 1


if __name__ == '__main__':
    while True:
        print("游戏规则："
              + "\n1:玩家=888， 机器人=robot；"
              + "\n2:每个玩家5张牌："
              + "\n3:牌有1<2，2<3,3<1，每张牌数量未知"
              + "\n4:比大小，（1）比拼牌归位，（2）胜者可交换点数以内任意牌，（3）败者获得胜者手中一张牌并弃一张牌"
              + "\n5:两人以上胜利条件：手牌先清空；平局：手牌均相等"
              + "\n6：两人：手牌均大于对方；可理解为上帝视角不换能赢，因为只要换就有随机性，帮助玩家确认应不应该换")
        restart = input(lamp + '回车代表输入完成，明牌：o，盖牌（默认）：c， 中止游戏：n，其余键开始游戏' + lamp)
        if restart == "o":
            game_visible = True
        elif restart == "c":
            game_visible = False
        if restart == "n":
            print("游戏中止")
            break
        game_start(1)
