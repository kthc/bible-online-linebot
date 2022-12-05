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
    CarouselTemplate
)
import re, uuid
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
        self.pre_messages = ['完全忘記我這週要帶小組！到現在還沒想好要帶什麼信息和活動...']
        self.post_messages = []
        self.main_messages = [f'''這次範圍在馬太福音，你能幫幫我嗎？\n(請輸入｢可以啊｣開始遊戲)''']
        self.ans = '可以啊'
        self.reply_messages_correct = []
        self.reply_messages_wrong = ['''喔不! 原來你還沒準備好。沒關係，隨時輸入"GO"讓我知道可以開始囉!''']

    def get_main_message(self):
        return [
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title=f'{self.username}在嗎?',
                    text='Welcome',
                    actions=[
                        MessageTemplateAction(
                            label='在啊！怎麼了?',
                            text='在啊！怎麼了?'
                        ),
                        MessageTemplateAction(
                            label='不在，幹嘛?',
                            text='不在，幹嘛?'
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
            '''喔不! 原來你還沒準備好。沒關係，隨時輸入"可以啊"讓我知道可以開始囉!''']

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if force_correct:
            # force correct answer
            return True, []
        if ans == self.ans:
            return True, []
        return False, [TextSendMessage(text=msg) for msg in self.reply_messages_wrong]


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
            f'''好像是跟祖譜有關？看來要排出七代的順序...\n這種邏輯我超弱，求幫忙！\n(請自老到幼排序，並以中文逗號間隔人名)'''
        ]
        self.ans = '亞金，以律，以利亞撒，馬但，雅各，約瑟，耶穌'
        self.reply_messages_wrong = [
            "Hmm..我們是不是少寫了些人啊，這樣無法喚起我的記憶阿!!",
            "ㄟ不是，我們忘了用中文逗號分隔人名啦!",
            "怎麼感覺哪裡怪怪的，再想一下好了",
            "哩來亂! 你沒有輸入耶穌祖譜的相關人員!"
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        correct_ans_list = self.ans.split("，")
        pattern = r"[\s\W]"
        fixed_ans = re.sub(pattern, "，", ans)
        if force_correct:
            # force correct answer
            return True, [TextSendMessage(text=msg) for msg in self.post_messages]
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


class Question4(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 400
        self.story_name = '大衛的子孫'
        self.pre_messages = []
        self.post_messages = [
            '''不錯喔! 你竟然看的出來''']
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
            return True, [TextSendMessage(text=msg) for msg in self.post_messages]
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
        picture = [ImageSendMessage(original_content_url="https://img.onl/M2cPB3",
                                    preview_image_url="https://i.imgur.com/rvQwscy.png")]
        main_msg = [TextSendMessage(text=text) for text in self.main_messages]
        return picture + main_msg



class Question5(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 500
        self.story_name = '先知'
        self.pre_messages = [
            f'''沒啦，剛好才思泉湧，就做出來了''',
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
            ImageSendMessage(original_content_url = f"{APP_URL}/static/img/Q5_parables_prophet.png", preview_image_url = f"{APP_URL}/static/img/5_parables_prophet.png")
            ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if self.ans == ans or force_correct:
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
            '''答對了\n耶！''',
            '''但好像要解出第二小題才能真正看出秘密?'''
            ]
        self.main_messages = ''
        self.ans = 'yasha'
        self.reply_messages_wrong = ["怎麼感覺哪裡怪怪的，再想一下好了"]
    
    def get_main_message(self):
        return [
            ImageSendMessage(original_content_url = f"{APP_URL}/static/img/6_a_Hosannah_Com.png", preview_image_url = f"{APP_URL}/static/img/6_a_Hosannah_Com.png")
            ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if self.ans == ans.lower() or force_correct:
            return True, [TextSendMessage(text=msg) for msg in self.post_messages]
        else:
            return False, [TextSendMessage(text=msg) for msg in self.reply_messages_wrong]


class Question6_b(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 620
        self.q6_uuid = kwargs.get('q6_uuid', '')
        self.story_name = '拯救者(b)'
        self.pre_messages = [
            f'''強者同學竟然還做了兩個版本，可以選挑戰版還是正常版喔''']
        self.post_messages = ['選擇了正常版', '選擇了挑戰版']
        self.main_messages = []
        self.ans = ''
        self.reply_messages_wrong = [f'''選一下你要挑戰哪個版本吧!''']

    def get_main_message(self):
        return [
            TemplateSendMessage(
                alt_text='Q6b',
                template=CarouselTemplate(
                    columns=[
                        CarouselColumn(
                            title='正常版',
                            text='適合不想太燒腦的你',
                            thumbnail_image_url=img_dict.get('Q6_normal','')['url'],
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
                            thumbnail_image_url=img_dict.get('Q6_challeng','')['url'],
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
            return True, [TextSendMessage(text=self.post_messages[0])]
        elif ans == '挑戰版':
            STORY_GLOBAL[self.q6_uuid] = 2
            return True, [TextSendMessage(text=self.post_messages[1])]

class Question6_b_1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 621
        self.q6_uuid = kwargs.get('q6_uuid', '')
        self.story_name = '拯救者(b)'
        self.pre_messages = []
        self.post_messages = ['我問問看！嗯嗯他說答對了！']
        self.main_messages = []
        self.ans = ''
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
            return True, [TextSendMessage(text=msg, sender=None) for msg in self.post_messages]
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

class Ending(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 99
        self.story_name = 'Ending'
        self.pre_messages = ['''這些素材真是太可以了!\n周六的小組有救了!''']
        self.post_messages = []
        self.main_messages = [
            '''作為福利，我讓你搶先看週六小組的信息內容 (放牧師的講章連結)''',
            "{placeholder for 奉獻資訊?}\n{placeholder for next episode?}"
            ]
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = ['你已經闖關完畢囉!']

    def get_main_message(self):
        sticker = [StickerSendMessage(package_id=11537, sticker_id=52002745)]
        main_msg = [TextSendMessage(text=text) for text in self.main_messages]
        return sticker + main_msg
    
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
