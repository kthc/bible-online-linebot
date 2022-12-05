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
    Sender
)
from app_global import line_bot_api
import story
from story_data_collection import audio_dict, video_dict, img_dict

class Story_Manager:
    def __init__(self, user_name='USER') -> None:
        self.stories = [
            story.Welcome(username=user_name),  
            story.simple_msg_maker(2, msg='電話響起', button_label='誰啊?', text_after_clicked='嗯？誰啊？不明電話？算了接一下好了', sender_name="BG"),
            story.simple_audio_maker(3, audio_name='01', sender_name='unknown', button_label='這是.....', text_after_clicked='這是什麼啊？打錯了嗎？怎麼突然又掛掉了呢？\n但又感覺這聲音有點熟悉，但聲音真得有點糊……\n又來一通？'),
            story.simple_audio_maker(5, audio_name='02', sender_name='unknown', button_label='你說什麼？', text_after_clicked='等等等？你真的是小亭？穿越到過去是什麼鬼？阿你沒事答應人家幹嘛？我怎麼會知道在哪裡啦？要找到也要花一陣子啊！'),
            story.simple_audio_maker(6, audio_name='03', sender_name='小亭', button_label='好啊！', text_after_clicked='痾好喔！這也太難，這麼古老以前，誰會知道啊，痾痾痾……\n阿對了，可以去找找社區的爺爺奶奶，說不定能得到一些結論。'),
            story.Question1(),
            story.Question1_1(),
            story.simple_msg_maker(7, msg='找到了', button_label='找到了', text_after_clicked='找是找到了，但是沒想到原來龍口市場之前有條小河啊！\n已經30分鐘了，不知道他有沒有找到方法能聯絡到我……\n痾電話？終於來了？「喂？', sender_name="BG"),
            story.simple_audio_maker(8, audio_name='04', sender_name='小亭', button_label='有阿', text_after_clicked='有有有，那個地方很好認，你那時候龍口市場有條河，就在他附近，雜貨店旁邊有豆漿店、肉攤，對面有米店。'),
            story.simple_audio_maker(9, audio_name='05', sender_name='小亭_19', button_label='如果', text_after_clicked='嗯嗯，如果照他說的，幫忙解決完這個問題完應該會再跳到下一個年代吧？'),
            # simple_msg_maker(10, msg='1小時後', button_label='不知名來電？', text_after_clicked='又一通不知名來電？難不成又是小亭？', sender_name="BG"),
            # simple_image_maker(10, image_name='OneHourLater', button_label='不知名來電？', text_after_clicked='又一通不知名來電？難不成又是小亭？', sender_name="BG"),
            story.OneHourLater(),
            # simple_video_maker(10, video_name='OneHourLater', button_label='不知名來電？', text_after_clicked='又一通不知名來電？難不成又是小亭？', sender_name="BG"),
            story.simple_audio_maker(11, audio_name='06', sender_name='小亭', button_label='痾...', text_after_clicked='痾！我可以幫忙啊，但我要知道內容是什啊！'),
            story.simple_audio_maker(12, audio_name='07', sender_name='小亭_12', button_label='等等等', text_after_clicked='停一下大哥，你那一串是什麼鬼，泰文喔？你這樣不行啦，你告訴我你在哪個年代，在什麼地方，那位姊姊叫什麼，我想想辦法，說不定能找到線索。'),
            story.simple_audio_maker(13, audio_name='08', sender_name='小亭', button_label='那怎麼辦？', text_after_clicked='我怎麼幫你啊，我根本就不知道內容，但是你這麼一講，那位姊姊的名字好耳熟欸……\n讓我想想喔！難道是小美奶奶嗎？我去找她問問，說不定他還留著那封信。'),
            story.simple_audio_maker(14, audio_name='09', sender_name='小亭', button_label='但不確定...', text_after_clicked='……還沒確定是不是，小心別叫人家奶奶喔，人家還很年輕，那我先打電話去問問她，掰掰。'),
            story.Question2(),
            story.Question2_1(),
            story.simple_msg_maker(15, msg='解出來了', button_label='有！但...', text_after_clicked='解是解出來了，但奶奶說什麼約的又是什麼？\n好險剛好在一個小時左右解開了，等等他的電話吧！', sender_name="BG"),
            story.simple_audio_maker(16, audio_name='10', sender_name='小亭_14', button_label='是他沒錯！', text_after_clicked='嗯嗯，他是小美奶奶，這封信其實是藏頭詩，解出來是龍口（龍口市場）？但不知道有什麼意思。'),
            story.simple_audio_maker(17, audio_name='11', sender_name='小亭', button_label='約？', text_after_clicked='約在那裡？帶小美「姊姊」？他怎麼知道也知道什麼約啊！還這麼親密……'),
            story.simple_msg_maker(18, msg=r'''‧★*"`'*-''', button_label='嗯？', text_after_clicked='嗯？信去了哪裡啊，我剛是放在這裡啊？\n奶奶，是怎麼回事，信不見了！', sender_name="BG"),
            story.simple_msg_maker(181, msg=r'''     *"`'*-.,_,.-*''', button_label='這是？', text_after_clicked='嗯？這是什麼情況，奶奶？奶奶？\n難不成幫助奶奶後，奶奶就消失了', sender_name="BG"),
            story.simple_msg_maker(182, msg=r'''           *-.,_,.-*'`"*-.,_☆''', button_label='看來...', text_after_clicked='看來改變過去，也改變了現在', sender_name="BG"),
            story.simple_msg_maker(19, msg='又過了一陣子', button_label='喂？', text_after_clicked='喂？幹嘛，又要幫忙？', sender_name="BG"),
            story.simple_audio_maker(20, audio_name='12', sender_name='小亭', button_label='好喔！', text_after_clicked='好喔，我錄一下。'),
            story.simple_audio_maker(21, audio_name='13', sender_name='小亭', button_label='讓我想想', text_after_clicked='好喔，我想想辦法把它解開來，這都是些什麼地方的話啊？好像有幾句粵語欸，Google翻譯聽不出來吧……\n到底要找誰幫忙呢？'),
            story.Question3(),
            story.simple_msg_maker(22, msg='沒想到', button_label='沒想到', text_after_clicked='原來融合了那麼多地方方言啊！', sender_name="BG"),
            story.simple_audio_maker(23, audio_name='14', sender_name='小亭', button_label='一碗...', text_after_clicked='一碗62元，趕快跟警察講吧！你也能趕快解開這次的謎題。'),
            story.simple_audio_maker(24, audio_name='15', sender_name='小亭', button_label='......', text_after_clicked='……誰累啊！明明都是我解的題，是我才累吧。'),
            story.simple_audio_maker(25, audio_name='16', sender_name='小亭_09', button_label='白眼', text_after_clicked='誰叫你都不好好學啊！算了沒事，來吧！什麼問題啊？'),
            story.simple_audio_maker(26, audio_name='17', sender_name='小亭', button_label='算了！', text_after_clicked='痾那算了！千禧蟲問題的話，你在幾年啊？如果2000年的話你也許能簡訊打字把訊息給我吧？'),
            story.simple_audio_maker(27, audio_name='18', sender_name='小亭', button_label='繼續保持', text_after_clicked='保持這份心情，應該是快要回來了，加油吧！先把題目給我，我趕快想想，那我先掛了喔！'),
            story.Question4(),
            story.simple_audio_maker(28, audio_name='19', sender_name='小亭', button_label='嗯嗯', text_after_clicked='嗯嗯答案是present，P R E S E N T，有聽懂吧？輸進去應該就可以了。'),
            story.simple_audio_maker(29, audio_name='20', sender_name='小亭_20', button_label='我也期待', text_after_clicked='嗯嗯我也期待你回來，這樣我就不用再動那麼多腦，而且休想拿一餐打發我，我可是費心費力費腦力欸！好啦，掰掰，我要休息一下下。'),
            story.simple_msg_maker(30, msg='又是電話', button_label='又......？', text_after_clicked='這次怎麼了？', sender_name="BG"),
            story.simple_audio_maker(31, audio_name='21', sender_name='小亭_10', button_label='痾.......', text_after_clicked='我想想喔，你打電話給他爸媽，告訴他們孩子被綁在哪？'),
            story.simple_audio_maker(32, audio_name='22', sender_name='小亭_10', button_label='聲音？', text_after_clicked='聲音，嗯……的確聽不到，讓我想想。\n對了，你可以錄下來給我啊，你應該在民國90幾年了吧！已經可以傳音訊給我了。'),
            story.simple_audio_maker(34, audio_name='23', sender_name='小亭', button_label='急死人了...', text_after_clicked='快快快'),
            story.simple_audio_maker(341, audio_name='Q5', sender_name='小亭', button_label='好像...', text_after_clicked='嗯？按號碼的聲音，這個應該有用\n​https://onlinetonegenerator.com/dtmf.html (若聽不到聲音請開啟靜音鍵喔!)'),
            # label='好像...', display_text='''嗯？按號碼的聲音，這個應該有用\n​https://onlinetonegenerator.com/dtmf.html'''
            # story.simple_audio_maker(33, audio_name='23', sender_name='小亭', button_label='好像...', text_after_clicked='嗯？按號碼的聲音，這個應該有用。'),
            # story.Question5(),
            story.Question5_1(),
            # story.simple_audio_maker(34, audio_name='24', sender_name='小亭', button_label='有了！', text_after_clicked='有有有，電話號碼是7533967，你趕快打給他爸媽，告訴他孩子在哪裡。'),
            story.simple_audio_maker(35, audio_name='25', sender_name='小亭_11', button_label='好喔……', text_after_clicked='好喔……'),
            story.simple_msg_maker(36, msg='過了一陣子', button_label='LINE？', text_after_clicked='LINE 語音?', sender_name="BG"),
            story.simple_audio_maker(37, audio_name='26', sender_name='小亭_19', button_label='真的假的？', text_after_clicked='等等等，摸了摸貓，就回來了？為什麼啊？怎麼那麼容易？'),
            story.simple_audio_maker(38, audio_name='27', sender_name='小亭', button_label='怎麼了？', text_after_clicked='怎麼了？又發生什麼事？'),
            story.simple_audio_maker(39, audio_name='28', sender_name='小亭', button_label='難道說...', text_after_clicked='喔，看來那隻貓有不為人知的能力呢！'),
            story.simple_audio_maker(40, audio_name='29', sender_name='小亭', button_label='沒問題！', text_after_clicked='好啊！等等我。'),
            story.Ending()
        ]
        self.user_name = user_name

    def set_username(self, username):
        self.user_name = username

    def get_story(self, story_id):
        '''return story instance if found'''
        for story in self.stories:
            if story_id == story.id:
                return story
        print(f'找不到Story_id:{story_id}')

    def last_story(self, story_id):
        '''return last story instance if found'''
        i = 0
        for i, story in enumerate(self.stories):
            if story_id == story.id:
                break
        if i-1 >= 0:
            last_story = self.stories[i-1]
            return last_story
        else:
            print(f'找不到上一個Story')
            return None

    def next_story(self, story_id):
        '''return next story instance if found'''
        for i, story in enumerate(self.stories):
            if story_id == story.id:
                break
        try:
            next_story = self.stories[i+1]
            return next_story
        except IndexError:
            print(f'找不到下一個Story')
            return None

    def is_end_story(self, story_id):
        '''check if this story is the last one'''
        story = self.next_story(story_id)
        if story:
            return False
        return True
    
    def show_welcome_story(self, event):
        story = self.get_story(0)
        messages = story.get_pre_message() + story.get_main_message()
        line_bot_api.reply_message(
                event.reply_token,
                messages=messages
                )

    def check_answer(self, event, story_id, ans, force_correct=False, retry_count=0) -> None:
        '''check answer and auto reply linebot
        return True if correct, else False
        '''
        story = self.get_story(story_id)
        correct, messages = story.check_ans(ans,force_correct,retry_count)
        if len(messages) > 5:
            line_bot_api.reply_message(
                event.reply_token,
                messages=TextSendMessage(text='回應訊息數超過五則喔!要重新修改後才能正確回傳!')
                )
            return False
        if correct or force_correct:
            next_story = self.next_story(story_id)
            if next_story:
                next_story_messages = messages + next_story.get_pre_message() + next_story.get_main_message()
                if len(next_story_messages) > 5:
                    line_bot_api.reply_message(
                        event.reply_token,
                        messages=TextSendMessage(text='回應訊息數超過五則喔!要重新修改後才能正確回傳!')
                        )
                    return False
                line_bot_api.reply_message(
                        event.reply_token,
                        messages=next_story_messages
                        )
            else:
                line_bot_api.reply_message(
                        event.reply_token,
                        messages=messages
                        )
            return True
        else:
            line_bot_api.reply_message(
                    event.reply_token,
                    messages=messages
                    )
            return False

    def show_story(self, event, story_id) -> None:
        '''show pre and main message of this story'''
        story = self.get_story(story_id)
        if story:
            messages = story.get_pre_message() + story.get_main_message()
            line_bot_api.reply_message(
                    event.reply_token,
                    messages=messages
                    )

if __name__=='__main__':
    s = Story_Manager()
    s.get_story(2)