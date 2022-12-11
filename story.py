from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    FollowEvent,
    UnfollowEvent,
    MessageEvent,
    TextMessage,
    TextSendMessage,
    StickerSendMessage,
    LocationMessage,
    LocationSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction,
    QuickReply,
    QuickReplyButton,
    PostbackAction,
    PostbackEvent,
    FollowEvent,
    DatetimePickerAction,
    MessageAction,
    CameraAction,
    CameraRollAction,
    LocationAction,
    AudioSendMessage,
    VideoSendMessage,
    ImageSendMessage,
    Sender,
    CarouselColumn,
    CarouselTemplate,
    FlexSendMessage
)
import re
import uuid
import random
from app_global import APP_URL
from story_data_collection import roles, audio_dict, video_dict, img_dict


STORY_GLOBAL = {}


class Story:
    def __init__(self, *args, **kwargs) -> None:
        self.username = ''
        self.story_name = ''
        self.id = -1
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = ''
        self.reply_messages_wrong = []

    def get_pre_message(self):
        return [TextSendMessage(text=text) for text in self.pre_messages]

    def get_main_message(self):
        return [TextSendMessage(text=text) for text in self.main_messages]

    def get_post_message(self):
        return [TextSendMessage(text=text) for text in self.post_messages]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if self.ans == ans or force_correct:
            return True, [TextSendMessage(text=msg, sender=None) for msg in self.post_messages]
        else:
            return False, [TextSendMessage(text=msg, sender=None) for msg in self.reply_messages_wrong]

    def show_ans_if_force_correct(self, messages=[], pre_text='正確答案是:'):
        '''if messages not given, it will send the correct ans and post_messages of this instance'''
        if len(messages) == 0:
            return True, [TextSendMessage(text=f'''{pre_text}{self.ans}''', sender=None)] + [TextSendMessage(text=msg, sender=None) for msg in self.post_messages]
        else:
            return True, messages


class SimplePostbackStory(Story):
    def __init__(self, id, *args, msg='', button_label='', text_after_clicked='', sender_name='', **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.data = '$Pass'
        self.label = button_label
        self.display_text = text_after_clicked
        self.main_messages = msg
        self.sender_name = sender_name

    def get_main_message(self):
        if self.display_text == '' or self.display_text is None:
            self.display_text = self.label
        return [
            TextSendMessage(
                text=self.main_messages,
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None)
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class AudioStory(Story):
    def __init__(self, id, *args, audio_name='', sender_name='', button_label='', text_after_clicked='',  **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = sender_name
        self.audio_name = audio_name
        self.label = button_label
        self.display_text = text_after_clicked

    def get_main_message(self):
        audio = audio_dict.get(self.audio_name, None)
        if audio_dict.get(self.audio_name, None) is None:
            audio = audio_dict.get('not_found', None)
        print(audio)
        return [
            AudioSendMessage(
                original_content_url=audio['url'],
                duration=audio['duration'],
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class VideoStory(Story):
    def __init__(self, id, *args, video_name='', sender_name='', button_label='', text_after_clicked='',  **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = sender_name
        self.video_name = video_name
        self.label = button_label
        self.display_text = text_after_clicked

    def get_main_message(self):
        video = video_dict.get(self.video_name, None)
        return [
            VideoSendMessage(
                original_content_url=video['url'],
                preview_image_url=video['preview'],
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class ImageStory(Story):
    def __init__(self, id, *args, image_name='', sender_name='', button_label='', text_after_clicked='',  **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = id
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = sender_name
        self.image_name = image_name
        self.label = button_label
        self.display_text = text_after_clicked

    def get_main_message(self):
        image = img_dict.get(self.image_name, None)
        return [
            ImageSendMessage(
                original_content_url=image['url'],
                preview_image_url=image['preview'],
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label=self.label, text=self.display_text)
                        )
                    ]
                ),
                sender=roles.get(self.sender_name, None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Welcome(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 0
        self.story_name = 'Welcome2'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '可以啊'
        self.reply_messages_correct = []
        self.reply_messages_wrong = []

    def get_main_message(self):
        return [
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title=f'{self.username}在嘛？',
                    text='\t',
                    actions=[
                        MessageTemplateAction(
                            label='在啊！怎麼了？',
                            text='在啊！怎麼了？'
                        ),
                        MessageTemplateAction(
                            label='不在，幹嘛？',
                            text='不在，幹嘛？'
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Welcome2(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 1
        self.story_name = 'Welcome2'
        self.pre_messages = ['完全忘記我這週要帶小組！到現在還沒想好要帶什麼信息和活動...']
        self.post_messages = []
        self.main_messages = [f'''這次範圍在馬太福音，你能幫幫我嗎？\n(請輸入｢可以啊｣開始遊戲)''']
        self.ans = '可以啊'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''喔不！ 原來你還沒準備好。沒關係，隨時輸入"可以啊"讓我知道可以開始囉！''']

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if force_correct:
            # force correct answer
            return True, []
        if ans == self.ans:
            return True, []
        return False, [TextSendMessage(text=msg) for msg in self.reply_messages_wrong]


class P7(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 16
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '可以啊'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''喔不！ 原來你還沒準備好。沒關係，隨時輸入"可以啊"讓我知道可以開始囉！''']

    def get_main_message(self):
        if self.display_text == '' or self.display_text is None:
            self.display_text = self.label
        return [
            TextSendMessage(
                text=f'欸？對欸，好險有你幫忙，我去找一下營隊手冊'
            ),
            TextSendMessage(
                text='我找到了！剛好營隊有很多內容也在馬太福音呢！',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='那我就幫你到這', text='那我就幫你到這，接下來就靠你自己吧！')
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Question1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 100
        self.story_name = '枝子題'
        self.pre_messages = [
            f'''所以才需要一起想啊！拜託啦~''']
        self.post_messages = []
        self.main_messages = [
            f'''上面有一大堆歪七扭八的線，不過旁邊有手冊的內容，它說...\n- 約瑟是耶穌的父親\n- 馬但是耶穌的祖父或曾祖父\n- 亞金不是以律的兒子\n- 雅各比以利亞撒晚出生\n- 亞金是馬但的長輩\n- 以利亞撒是亞金的孫子\n- 雅各不是耶穌的曾祖父''',
            f'''好像是跟祖譜有關？看來要排出七代的順序...''',
            '''這種邏輯我超弱，求幫忙！\n(請自老到幼排序，並以逗號間隔人名)'''
        ]
        self.ans = '亞金，以律，以利亞撒，馬但，雅各，約瑟，耶穌'
        self.reply_messages_wrong = [
            "Hmm..我們是不是少寫了些人啊，這樣無法喚起我的記憶阿！！",
            "ㄟ不是，我們忘了用逗號分隔人名啦！",
            "怎麼感覺哪裡怪怪的，再想一下好了",
            "哩來亂！你沒有輸入耶穌祖譜的相關人員！"
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        correct_ans_list = self.ans.split("，")
        pattern = r"[\s\W]"
        fixed_ans = re.sub(pattern, "，", ans)
        if force_correct:
            # force correct answer
            return self.show_ans_if_force_correct()
        if type(ans) is str:
            ans_list = fixed_ans.split("，")
            if len(ans_list) != 7:
                # handle if the number of names not equal to 7
                has_matched_ans = False
                for a in ans_list:
                    if a in correct_ans_list:
                        has_matched_ans = True
                        break
                if not has_matched_ans:
                    # not matched any of ans
                    return False, [TextSendMessage(text=self.reply_messages_wrong[3])]
                else:
                    # some matched, some not
                    return False, [TextSendMessage(text=self.reply_messages_wrong[0])]

            # check if the name not containing all the ans names
            existed_name = set()
            for a in ans_list:
                if (a in existed_name) or (a not in correct_ans_list):
                    return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
                existed_name.add(a)

            # check if order are exactly the same
            for a, correct_ans in zip(ans_list, correct_ans_list):
                if a != correct_ans:
                    return False, [TextSendMessage(text=self.reply_messages_wrong[2])]

            # correct answer
            return True, [TextSendMessage(text=msg) for msg in self.post_messages]
        return False, [TextSendMessage(text=self.reply_messages_wrong[3])]


class P12(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 45
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '可以啊'
        self.reply_messages_correct = []
        self.reply_messages_wrong = [
            '''喔不！ 原來你還沒準備好。沒關係，隨時輸入"可以啊"讓我知道可以開始囉！''']

    def get_main_message(self):
        if self.display_text == '' or self.display_text is None:
            self.display_text = self.label
        return [
            TextSendMessage(
                text=f'你等我講完，答案是聖經裡的一個名詞'
            ),
            TextSendMessage(
                text='我還留著當時的題目！翻到了！痾不過，沒有答案欸🤪',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='.....又來！', text='你的筆記要不是看不懂，就是缺漏...')
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Question2(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 200
        self.story_name = '伯利恆題'
        self.pre_messages = [
            f'''別這樣啦！你人最好了''',
            f'''我記得需要用到Goolge Map''']
        self.post_messages = [
            '''Wow！神隊友呀你！！！''']
        self.main_messages = [
            f'''題目長這樣:\n「跟著蔣渭水的腳步往南走了47公里，又餓又累，不得不去找東西吃，但是附近只有好像你家的地方。而且讓我一度懷疑我有任意門，如果能再有張床的話一切就太完美了！」'''
        ]
        self.ans = '伯利恆'
        self.reply_messages_wrong = [
            "怎麼感覺哪裡怪怪的，再想一下好了",
            "不是啦，這個詞沒出現在聖經過，是不是多打了些甚麼字呢？",
            "誒等下，我看到在題目旁邊還有隻雞被關在籠子裡的小插圖，不知道對你有沒有幫助？"
        ]

    def get_pre_message(self):
        location = [LocationSendMessage(title='Google maps', address='100台北市中正區和平西路二段15號',
                                        latitude=25.02840541918362, longitude=121.51382485320154)]
        pre_messages = [TextSendMessage(text=text)
                        for text in self.pre_messages]
        return pre_messages + location

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if force_correct:
            # force correct answer
            return self.show_ans_if_force_correct()
        if ans == self.ans or force_correct:
            return True, [TextSendMessage(text=msg) for msg in self.post_messages]
        elif retry_count == 3:
            return False, [TextSendMessage(text=self.reply_messages_wrong[2])]
        elif ans == "伯利恆之星":
            # some matched, some not
            return False, [TextSendMessage(text=self.reply_messages_wrong[1])]
        else:
            # not matched any of ans
            return False, [TextSendMessage(text=self.reply_messages_wrong[0])]


class Question3(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 300
        self.story_name = '新生王'
        self.pre_messages = [
            f'''是一個數獨的題目，看看你能不能解開天使的暗號''']
        self.post_messages = [
            '''不愧是我朋友，跟我一樣聰明😁''']
        self.main_messages = []
        self.ans = '榮耀歸於新生王'
        self.reply_messages_wrong = [
            "答案沒有陷阱，真的只是一般字串啦~",
            "怎麼感覺哪裡怪怪的，再想一下好了",
            "好像有點眉目了！再接著想想",
            "不是啦，這個不是天使說的暗號吧？再想想"
        ]

    def get_main_message(self):
        return [ImageSendMessage(original_content_url=f"{APP_URL}/static/img/3_New_born_king_sudoku.png", preview_image_url=f"{APP_URL}/static/img/3_New_born_king_sudoku.png")]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty lst if ans is correct, otherwise need to throw error message to reply to linbot'''
        if force_correct:
            # force correct answer
            return self.show_ans_if_force_correct()

        if type(ans) is str:
            # replace Chinese character for the same meaning
            if ("于" in ans or "予" in ans or "與" in ans):
                ans = ans.replace('于', '於')
                ans = ans.replace('予', '於')
                ans = ans.replace('與', '於')
            if (ans == self.ans):
                # correct answer
                return True, [TextSendMessage(text=msg) for msg in self.post_messages]
            # is almost ready to get the correct ans
            elif "聽啊天使高聲唱" in ans:
                return False, [TextSendMessage(text=self.reply_messages_wrong[3])]
            # some match the keyword
            elif ("聽啊" in ans or "天使" in ans or "高聲唱" in ans):
                return False, [TextSendMessage(text=self.reply_messages_wrong[2])]
            else:
                # is still far way from correct ans
                return False, [TextSendMessage(text=self.reply_messages_wrong[1])]
        return False, [TextSendMessage(text=self.reply_messages_wrong[0])]


class P17(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 55
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = []

    def get_main_message(self):
        if self.display_text == '' or self.display_text is None:
            self.display_text = self.label
        return [
            TextSendMessage(
                text=f'怎麼可能，講章太像上課一定沒人理我😤'
            ),
            TextSendMessage(
                text='我打算仿造之前玩過的解謎，讓大家動動腦',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='好啊！', text='設計完傳給我')
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Question4(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 400
        self.story_name = '大衛的子孫'
        self.pre_messages = []
        self.post_messages = [
            '''不錯喔！ 你竟然看的出來''']
        self.main_messages = [
            f'''字裡行間的顏色都有意義，看你能不能破解？'''
        ]
        self.ans = '大衛的子孫耶穌'
        self.reply_messages_wrong = [
            "怎麼感覺哪裡怪怪的，再想一下好了",
            "是不是少了點什麼",
            "很接近了，但字的順序好像怪怪的诶",
            "好像有頭緒了，但還差一點"
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        check_sequence = 0
        check_Str = 0
        for a in range(len(ans)):
            if ans.find(self.ans[a]) > 0:
                check_Str += 1
            if ans.find(self.ans[a]) == a:
                check_sequence += 1
        if force_correct:
            # force correct answer
            return self.show_ans_if_force_correct()
        if type(ans) is str:
            if ans == self.ans:
                return True, [TextSendMessage(text=msg) for msg in self.post_messages]
            elif check_sequence > 3 and check_sequence < len(self.ans) and check_Str > 5:
                return False, [TextSendMessage(text=self.reply_messages_wrong[2])]
            elif check_Str > 3:
                return False, [TextSendMessage(text=self.reply_messages_wrong[3])]
            elif check_Str <= 3 and check_Str > 0:
                return False, [TextSendMessage(text=self.reply_messages_wrong[1])]
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[0])]

    def get_main_message(self):
        picture = [ImageSendMessage(original_content_url=f"{APP_URL}/static/img/4_ba_fu.png",
                                    preview_image_url=f"{APP_URL}/static/img/4_ba_fu.png")]
        main_msg = [TextSendMessage(text=text) for text in self.main_messages]
        return picture + main_msg


class Question5(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 500
        self.story_name = '先知'
        self.pre_messages = [
            f'''沒啦，剛好才思泉湧，就做出來了😎''',
            f'''你再幫我檢查看看有沒有bug'''
        ]
        self.post_messages = []
        self.main_messages = ''
        self.ans = '以力殺'
        self.reply_messages_wrong = [
            "為了防止猜題的可能，請輸入實際解出的國字唷",
            "怎麼感覺哪裡怪怪的，再想一下好了"
        ]

    def get_main_message(self):
        return [
            ImageSendMessage(original_content_url=f"{APP_URL}/static/img/5_parables_prophet.png",
                             preview_image_url=f"{APP_URL}/static/img/5_parables_prophet.png")
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if force_correct:
            # force correct answer
            return self.show_ans_if_force_correct()
        if self.ans == ans:
            return True, [TextSendMessage(text=msg) for msg in self.post_messages]

        elif ans == '以利沙':
            return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        else:
            return False, [TextSendMessage(text=self.reply_messages_wrong[1])]


class Question6_a(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 600
        self.story_name = '拯救者(a)'
        self.pre_messages = [
            f'''不愧是我同學，竟然有兩個小題！''',
            f'''同學表示：背景是在耶穌進城的當下，群眾呼喊著“和散那”。而題組就藏著“和散那”的秘密！ (答案非英文單字)'''
        ]
        self.post_messages = [
            '''答對了耶！''',
            '''但好像要解出第二小題才能真正看出秘密？'''
        ]
        self.main_messages = ''
        self.ans = 'yasha'
        self.reply_messages_wrong = ["怎麼感覺哪裡怪怪的，再想一下好了"]

    def get_main_message(self):
        return [
            ImageSendMessage(original_content_url=f"{APP_URL}/static/img/6_a_Hosannah_Com.png",
                             preview_image_url=f"{APP_URL}/static/img/6_a_Hosannah_Com.png")
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if force_correct:
            # force correct answer
            return self.show_ans_if_force_correct()
        if self.ans == ans.strip().lower():
            return True, [TextSendMessage(text=msg) for msg in self.post_messages]
        else:
            return False, [TextSendMessage(text=msg) for msg in self.reply_messages_wrong]


class P31(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 95
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = []

    def get_main_message(self):
        if self.display_text == '' or self.display_text is None:
            self.display_text = self.label
        return [
            TextSendMessage(
                text=f'😥對啊！我都解崩潰了，還是沒頭緒'
            ),
            TextSendMessage(
                text='我覺得可以來收尾了！',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='對阿！', text='已經有不少素材了！')
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Question6_b(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 620
        self.q6_uuid = kwargs.get('q6_uuid', '')
        self.story_name = '拯救者(b)'
        self.pre_messages = [
            f'''強者同學竟然還做了兩個版本，可以選挑戰版還是正常版喔''']
        self.post_messages = []
        self.main_messages = []
        self.ans = ''
        self.reply_messages_wrong = [f'''選一下你要挑戰哪個版本吧！''']

    def get_main_message(self):
        return [
            TemplateSendMessage(
                alt_text='Q6b',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            title='正常版',
                            text='適合不想太燒腦的你',
                            thumbnail_image_url=img_dict.get(
                                'Q6_normal', '')['url'],
                            actions=[
                                MessageAction(
                                    label='正常版',
                                    text='正常版'
                                )
                            ]
                        ),
                        CarouselColumn(
                            title='挑戰版',
                            text='來挑戰看看吧',
                            thumbnail_image_url=img_dict.get(
                                'Q6_challeng', '')['url'],
                            actions=[
                                MessageAction(
                                    label='挑戰版',
                                    text='挑戰版'
                                )
                            ]
                        )
                    ],
                    image_aspect_ratio='rectangle',
                    image_size='contain',
                )

            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        global STORY_GLOBAL
        if force_correct:
            # force correct answer
            return False, [TextSendMessage(text=msg) for msg in self.reply_messages_wrong]
        if ans != '正常版' and ans != '挑戰版':
            STORY_GLOBAL[self.q6_uuid] = 0
            return False, [TextSendMessage(text=msg) for msg in self.reply_messages_wrong]
        elif ans == '正常版':
            STORY_GLOBAL[self.q6_uuid] = 1
            return True, []
        elif ans == '挑戰版':
            STORY_GLOBAL[self.q6_uuid] = 2
            return True, []


class Question6_b_1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 621
        self.q6_uuid = kwargs.get('q6_uuid', '')
        self.story_name = '拯救者(b)'
        self.pre_messages = []
        self.post_messages = ['我問問看！嗯嗯他說答對了！']
        self.main_messages = []
        self.ans = 'Anna'
        self.reply_messages_wrong = [
            "怎麼感覺哪裡怪怪的，再想一下好了",
            "如果後悔了想更改挑戰模式的話，可以重選喔！",
            "很接近了，但字的順序好像怪怪的诶",
            "好像有頭緒了，但還差一點"
        ]

    def get_main_message(self):
        global STORY_GLOBAL
        if STORY_GLOBAL[self.q6_uuid] == 1:
            return [
                ImageSendMessage(original_content_url=img_dict.get('Q6_normal_grid')[
                                 'url'], preview_image_url=img_dict.get('Q6_normal_grid')['url'])
            ]
        elif STORY_GLOBAL[self.q6_uuid] == 2:
            return [
                ImageSendMessage(original_content_url=img_dict.get('Q6_challeng_grid')[
                                 'url'], preview_image_url=img_dict.get('Q6_challeng_grid')['url'])
            ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        global STORY_GLOBAL
        if force_correct:
            # force correct answer
            return self.show_ans_if_force_correct()
        if ans == 'anna' or ans == 'Anna':
            return True, [TextSendMessage(text=msg, sender=None) for msg in self.post_messages]
        if retry_count >= 5:
            return False, [
                TextSendMessage(text=self.reply_messages_wrong[1],
                                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(
                                label='重新選擇吧', data='$Q6_reset', display_text='如果後悔了想更改挑戰模式的話，可以重選喔！')
                        )
                    ]
                ),
                )
            ]
        if ans != 'anna' and ans != 'Anna':
            return False, [TextSendMessage(text=self.reply_messages_wrong[0])]
        return False, [TextSendMessage(text=self.reply_messages_wrong[0])]


class Question7(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 700
        self.story_name = '出賣'
        self.pre_messages = []
        self.post_messages = ['真是太感謝你了！']
        self.main_messages = [
            '我想想…用這個結尾如何？既然耶穌是主角，就要找到耶穌在客西馬尼園禱告的位置！', '(請根據地圖上的標示輸入相同的文字)']
        self.ans = '2'
        self.reply_messages_wrong = [
            "怎麼感覺哪裡怪怪的，再想一下好了"
        ]

    def get_main_message(self):
        return [
            TextSendMessage(text=self.main_messages[0]),
            ImageSendMessage(original_content_url=f"{APP_URL}/static/img/7_betray_word_puzzle_combine.png",
                             preview_image_url=f"{APP_URL}/static/img/7_betray_word_puzzle_combine.png"),
            ImageSendMessage(original_content_url=f"{APP_URL}/static/img/7_betray_map_combine.png",
                             preview_image_url=f"{APP_URL}/static/img/7_betray_map_combine.png"),
            TextSendMessage(text=self.main_messages[1])
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if force_correct:
            # force correct answer
            return self.show_ans_if_force_correct()
        if ans == self.ans:
            return True, [TextSendMessage(text=msg, sender=None) for msg in self.post_messages]
        return False, [TextSendMessage(text=self.reply_messages_wrong[0])]


class Ending(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 990
        self.story_name = 'Ending'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = ['你已經闖關完畢囉！']

    # def get_main_message(self):
    #     sticker = [StickerSendMessage(package_id=11537, sticker_id=52002745)]
    #     main_msg = [TextSendMessage(text=text) for text in self.main_messages]
    #     images = [
    #         ImageSendMessage(original_content_url = f"{APP_URL}/static/img/info.jpg", preview_image_url = f"{APP_URL}/static/img/info.jpg")
    #         ]
    #     return sticker + main_msg

    def get_main_message(self):
        contents = {
            "type": "carousel",
            "contents": [
                {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "週六小組裡到底分享了甚麼信息呢？ 點選下小組信息就可以看囉。中間在哪一題卡住了嗎？點選解題思路，看看各題的解題辦法！",
                                "wrap": True
                            }
                        ],
                        "height": "150px",
                        "alignItems": "center",
                        "justifyContent": "flex-end"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "小組訊息",
                                    "text": "https://drive.google.com/file/d/1mQhwBJ1_uX4WPmyS9uIgXeRjjorZrYkW/view?usp=share_link"
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "解題思路",
                                    "text": "https://drive.google.com/file/d/1D7Ysl2IS_fTzHvCxvxpQoU59TwN6Rz5J/view?usp=share_link"
                                }
                            }
                        ],
                        "position": "relative"
                    },
                    "styles": {
                        "header": {
                            "separatorColor": "#dbdbdb",
                            "separator": True
                        },
                        "hero": {
                            "separator": True,
                            "separatorColor": "#b0b0b0"
                        },
                        "body": {
                            "separator": True,
                            "separatorColor": "#b0b0b0"
                        }
                    }
                },
                {
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "text",
                                "text": "歡迎點選以下連結更了解我們團隊，若您願意奉獻，也可參考奉獻資訊。",
                                "wrap": True
                            }
                        ],
                        "height": "150px",
                        "alignItems": "center",
                        "justifyContent": "flex-end"
                    },
                    "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "團隊介紹",
                                    "text": "我們是一群來自台北古亭聖教會的社青和青年。我們熱衷解謎，從某一青年就讀的高中設計了linebot解謎，促發這次活動的設計。歷經5個月的技術課程和題目劇情的討論，終於在今年底正式推出！"
                                }
                            },
                            {
                                "type": "button",
                                "action": {
                                    "type": "message",
                                    "label": "奉獻資訊",
                                    "text": '''感謝您的擺上，奉獻資訊如下，煩請於備註中填寫"Line"，以利司庫同工辨認。 第一銀行(銀行代碼：007)：172-10-115645，若您需要奉獻收據，請填寫以下表單。https://docs.google.com/forms/d/1H0WvivuNyGX4RnSz3nuiJ9MUvd8PlykM74d7VpcoQOI/edit'''
                                }
                            }
                        ],
                        "position": "relative"
                    },
                    "styles": {
                        "header": {
                            "separatorColor": "#dbdbdb",
                            "separator": True
                        },
                        "hero": {
                            "separator": True,
                            "separatorColor": "#b0b0b0"
                        },
                        "body": {
                            "separator": True,
                            "separatorColor": "#b0b0b0"
                        }
                    }
                }
            ]
        }
        sticker = [StickerSendMessage(package_id=11537, sticker_id=52002745)]
        # main_msg = [TextSendMessage(text=text) for text in self.main_messages]
        main_msg2 = [
            TextSendMessage(text='''這些素材真是太可以了！'''),
            StickerSendMessage(package_id=11537, sticker_id=52002745),
            TextSendMessage(text='''作為福利，我讓你搶先看週六小組的信息內容'''),
            FlexSendMessage(alt_text='flex_contents', contents=contents),
            # TemplateSendMessage(
            #     alt_text='Buttons template',
            #     template=ButtonsTemplate(
            #         title='關於我們',
            #         text='想更深入了解我們團隊嗎？請點選下面按鈕',
            #         actions=[
            #             MessageTemplateAction(
            #                 label='搶先看週六小組的信息內容',
            #                 text=f'搶先看週六小組的信息內容:(牧師講章)'
            #             ),
            #             MessageTemplateAction(
            #                 label='解題思路',
            #                 text=f'解題思路:TBD'
            #             ),
            #             MessageTemplateAction(
            #                 label='團隊介紹',
            #                 text=f'團隊介紹:TBD'
            #             ),
            #             MessageTemplateAction(
            #                 label='奉獻資訊',
            #                 text=f'奉獻資訊:TBD'
            #             ),
            #         ]
            #     )
            # )
        ]
        return sticker + main_msg2

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return False, [TextSendMessage(text=msg) for msg in self.reply_messages_wrong]


def simple_msg_maker(id, msg='', button_label='', text_after_clicked='', sender_name=''):
    return SimplePostbackStory(id, msg=msg, button_label=button_label, text_after_clicked=text_after_clicked, sender_name=sender_name)


def simple_audio_maker(id, audio_name='', sender_name='', button_label='', text_after_clicked='',):
    return AudioStory(id, audio_name=audio_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)


def simple_video_maker(id, video_name='', sender_name='', button_label='', text_after_clicked='',):
    return VideoStory(id, video_name=video_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)


def simple_image_maker(id, image_name='', sender_name='', button_label='', text_after_clicked='',):
    return ImageStory(id, image_name=image_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)
