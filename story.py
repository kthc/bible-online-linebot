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
    Sender
)
import re
import random
from app_global import APP_URL
from story_data_collection import roles, audio_dict, video_dict, img_dict


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
        self.story_name = 'Welcome'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = [
            f'''請用手機進行遊戲，並點選螢幕下方浮現的按鈕來推進劇情，若無按鈕請輸入答案。錄音中的雜訊純屬遊戲效果。卡關時輸入sos可跳關、輸入reset可重新開始''']
        self.ans = 'go'
        self.reply_messages_correct = []
        self.reply_messages_wrong = ['''喔不! 原來你還沒準備好。沒關係，隨時輸入"GO"讓我知道可以開始囉!''']

    def get_main_message(self):
        return [
            TextSendMessage(text=self.main_messages[0]),
            TextSendMessage(
                text='Hi 小古，你準備好了嗎？',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(
                                data='$Welcom_Bypass', label='準備好了', display_text='奇怪，怎麼那麼久都沒到啦？')
                        )
                    ]
                )
            )
        ]


    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if self.ans == ans.lower() or force_correct or ans == '$Welcom_Bypass':
            return True, [TextSendMessage(text=msg) for msg in self.post_messages]
        else:
            if retry_count == 3:
                return False, [TextSendMessage(text='你來搞亂的喔，GO會不會寫啊，會寫就趕快開始阿!')]
            elif retry_count > 3:
                return False, [TextSendMessage(text='你真的不適合這個遊戲!不理你了，除非你打GO這個通關密碼....')]
            return False, [TextSendMessage(text=msg) for msg in self.reply_messages_wrong]


class Question1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 90
        self.story_name = '找店鋪'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '西，3'
        self.reply_messages_wrong = [
            "要跟我說方位和數字喔",
            "輸入格式好像怪怪的!",
            "方位好像不太正確",
            "好像不是這家店!",
            "好像怪怪的!"
        ]

    def get_main_message(self):
        return [
            TextSendMessage(
                text='https://youtu.be/pNme8J4FCN8',
                # original_content_url=video_dict['Q1']['url'], preview_image_url=video_dict['Q1']['preview'], sender=roles.get(
                #     "BG", None),
                sender=roles.get("BG", None),
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='筆記', text='還好我有做筆記')
                        )
                    ]
                )),
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Question1_1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 901
        self.story_name = '找店鋪'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '2'
        self.reply_messages_wrong = [
            "好像不是這家店!"
        ]

    def get_main_message(self):
        return [
            ImageSendMessage(
                original_content_url=img_dict['Q1']['url'], preview_image_url=img_dict['Q1']['preview'], sender=roles.get("BG", None)),
            TextSendMessage(text='請找出雜貨店的位置!',
                            sender=roles.get("BG", None)),
            TextSendMessage(
                text='(答案格式：位置 1~8 請擇一輸入)', sender=roles.get("BG", None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        if force_correct:
            # force correct answer
            return True, [TextSendMessage(text=f'''解出來了，正確答案是{self.ans}''')]
        elif ans == '2':
            return True, []
        else:
            return False, [TextSendMessage(text=self.reply_messages_wrong[0])]


class OneHourLater(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        '''simple_video_maker(10, video_name='OneHourLater', button_label='不知名來電？', text_after_clicked='又一通不知名來電？難不成又是小亭？', sender_name="BG"),'''
        self.id = 902
        self.story_name = ''
        self.pre_messages = []
        self.post_messages = []
        self.ans = ''
        self.reply_messages_wrong = []
        self.main_messages = []
        self.sender_name = "BG"
        self.video_name = 'OneHourLater'
        self.label = '不知名來電？'
        self.display_text = '又一通不知名來電？難不成又是小亭？'

    def get_main_message(self):
        video = video_dict.get(self.video_name, None)
        return [
            TextSendMessage(text='1小時後',
                            sender=roles.get("BG", None)),
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


class Question2(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 91
        self.story_name = '英文信'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '龍口'
        self.reply_messages_wrong = [
            "好像怪怪的!",
            "不對呢，再試試看"
        ]

    def get_main_message(self):
        return [
            TextSendMessage(
                # original_content_url=video_dict['Q2']['url'],
                # preview_image_url=video_dict['Q2']['preview'],
                text='https://youtu.be/PdOlA0FZ2Io',
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=MessageAction(
                                label='讀信', text='這是首詩嗎？')
                        )
                    ]
                ),
                sender=roles.get("BG", None)),
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []


class Question2_1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 911
        self.story_name = '英文信'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '龍口'
        self.reply_messages_wrong = [
            "好像怪怪的!",
            "不對呢，再試試看"
        ]

    def get_main_message(self):
        return [
            ImageSendMessage(
                original_content_url=img_dict['Q2']['url'], preview_image_url=img_dict['Q2']['preview'], sender=roles.get("BG", None)),
            TextSendMessage(text='請輸入信中隱藏的地點',
                            sender=roles.get("BG", None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        rnd = random.random()
        rnd_reply_idx = 1 if rnd > 0.5 else 0
        if force_correct:
            # force correct answer
            return True, [TextSendMessage(text=f'''找到了，正確答案是{self.ans}''')]
        if type(ans) is str:
            if ans in ['龍口', '龍口市場']:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]
        return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]


class Question3(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 92
        self.story_name = '語言題'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '62元'
        self.reply_messages_wrong = [
            "好像怪怪的!",
            "不對呢，再試試看"
        ]

    def get_main_message(self):
        return [
            # VideoSendMessage(
            #     original_content_url=video_dict['Q3']['url'], preview_image_url=video_dict['Q3']['preview'], sender=roles.get(
            #         "BG", None)
            # ),
            TextSendMessage(
                text='https://youtu.be/LocFySbWcQA',
                sender=roles.get("BG", None)
            ),
            TextSendMessage(text='牛肉麵____元？請輸入',
                            sender=roles.get("BG", None),
                            quick_reply=QuickReply(
                                items=[
                                    QuickReplyButton(
                                        action=PostbackAction(
                                            data='$Q3_Bypass', label='快來算算看', display_text='''- 一碗陽春麵的錢可以買三碗豆花\n- 牛肉麵今天漲了2元\n- 2顆肉圓和一碗肉燥飯一樣，都是10元\n- 原本三碗肉燥飯、一碗陽春麵、一碗豆花，再加上兩顆肉圓的錢，剛好可以買一碗牛肉麵\n- 兩碗陽春麵的錢可以買2碗肉燥飯、一顆肉圓和一碗豆花''')
                                    )
                                ]
                            ))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        rnd = random.random()
        rnd_reply_idx = 1 if rnd > 0.5 else 0
        if force_correct:
            # force correct answer
            return True, [TextSendMessage(text=f'''沒想到，正確答案是{self.ans}''')]
        if type(ans) is str:
            if ans in ['62', '62元']:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]
        return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]


class Question4(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 93
        self.story_name = '千禧蟲問題'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = 'present'
        self.reply_messages_wrong = [
            "好像怪怪的!",
            "不對呢，再試試看"
        ]

    def get_main_message(self):
        return [
            TextSendMessage(text='''prank=昏倒\nsralt=吞了\nsrure=推往\n荒唐的=_____''',
                            sender=roles.get("BG", None))
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        rnd = random.random()
        rnd_reply_idx = 1 if rnd > 0.5 else 0
        if force_correct:
            # force correct answer
            return True, [TextSendMessage(text=f'''正確答案是{self.ans}''')]
        if type(ans) is str:
            if ans.lower().strip() == self.ans:
                return True, []
            else:
                return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]
        return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]


class Question5(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 94
        self.story_name = '電話號碼'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '7533967'
        self.reply_messages_wrong = [
            "好像怪怪的!",
            "不對呢，再試試看"
        ]

    def get_main_message(self):
        return [
            AudioSendMessage(
                original_content_url=audio_dict['Q5']['url'],
                duration=audio_dict['Q5']['duration'],
                sender=roles.get('小亭', None),
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(
                                data='$Q5_Bypass', label='好像...', display_text='''嗯？按號碼的聲音，這個應該有用\n​https://onlinetonegenerator.com/dtmf.html''')
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return True, []

class Question5_1(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.id = 941
        self.story_name = '電話號碼'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = []
        self.ans = '7533967'
        self.reply_messages_wrong = [
            "好像怪怪的!",
            "不對呢，再試試看"
        ]

    def get_main_message(self):
        return [
            AudioSendMessage(
                original_content_url=audio_dict['24']['url'],
                duration=audio_dict['24']['duration'],
                sender=roles.get('小亭', None),
                quick_reply=QuickReply(
                    items=[
                        QuickReplyButton(
                            action=PostbackAction(
                                data='$Q5_Bypass', label='等等', display_text='''我聽看看，號碼是...''')
                        )
                    ]
                )
            )
        ]

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        rnd = random.random()
        rnd_reply_idx = 1 if rnd > 0.5 else 0
        if force_correct:
            # force correct answer
            return True, [TextSendMessage(text=f'''正確答案是{self.ans}''')]
        if type(ans) is str:
            if ans == self.ans:
                return True, []
            else:
                if retry_count == 3:
                    return False, [
                        TextSendMessage(
                            text='...',
                            quick_reply=QuickReply(
                                items=[
                                    QuickReplyButton(
                                        action=PostbackAction(
                                            data='$Q5_Bypass', label='也太難了吧', display_text='''我聽出來了！好像是7533什麼的，到底完整的電話號碼是什麼呢？''')
                                    )
                                ]
                            )
                        ),
                    ]
                elif retry_count > 3:
                    False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]
        return False, [TextSendMessage(text=self.reply_messages_wrong[rnd_reply_idx])]

class Ending(Story):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(args, kwargs)
        self.username = kwargs.get('username', '玩家')
        self.id = 99
        self.story_name = 'Ending'
        self.pre_messages = []
        self.post_messages = []
        self.main_messages = ["遊戲結束"]
        self.ans = ''
        self.reply_messages_correct = []
        self.reply_messages_wrong = ['你已經闖關完畢囉!']

    def get_main_message(self):
        main_msg = [
            TemplateSendMessage(
                alt_text='Buttons template',
                template=ButtonsTemplate(
                    title='幕後花絮集錦',
                    text='想更深入了解龍口市場的歷史跟我們團隊嗎?請點選下面按鈕',
                    actions=[
                        MessageTemplateAction(
                            label='小亭走過哪',
                            text=f'小亭走過哪:https://drive.google.com/file/d/1_6PpXr0uA8CNEqhKvw1-YcCvJo6r8jUE/view'
                        ),
                        MessageTemplateAction(
                            label='解題策略',
                            text=f'解題策略:https://drive.google.com/file/d/1KG0nVTn0Y9sMRT-go2oPpwWtqB4QIEU5/view'
                        ),
                        MessageTemplateAction(
                            label='龍口歷史',
                            text=f'龍口歷史:TBD'
                        ),
                    ]
                )
            )
        ]
        return main_msg

    def check_ans(self, ans, force_correct=False, retry_count=0):
        '''return (True, Messages:list), Message is empty list if ans is correct, otherwise need to throw error message to reply to linbot'''
        return False, []


def simple_msg_maker(id, msg='', button_label='', text_after_clicked='', sender_name=''):
    return SimplePostbackStory(id, msg=msg, button_label=button_label, text_after_clicked=text_after_clicked, sender_name=sender_name)


def simple_audio_maker(id, audio_name='', sender_name='', button_label='', text_after_clicked='',):
    return AudioStory(id, audio_name=audio_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)


def simple_video_maker(id, video_name='', sender_name='', button_label='', text_after_clicked='',):
    return VideoStory(id, video_name=video_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)


def simple_image_maker(id, image_name='', sender_name='', button_label='', text_after_clicked='',):
    return ImageStory(id, image_name=image_name, sender_name=sender_name, button_label=button_label, text_after_clicked=text_after_clicked)
