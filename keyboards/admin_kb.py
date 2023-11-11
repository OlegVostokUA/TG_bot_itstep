from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


# buttons for first KB
button_load = KeyboardButton(text='/Download') # start process FSM/
button_show = KeyboardButton(text='/Show_goods') # show info from DB
button_delete = KeyboardButton(text='/Delete') # delete from DB
button_parse = KeyboardButton(text='/Show_info') # courses $, EURO
button_prog_lang = KeyboardButton(text='/Progr_lang-s') # transf to second keyboard
button_doc = KeyboardButton(text='/Read_me_doc') # send read_me.doc in message
# buttons for second KB
button_python = KeyboardButton(text='/Python')
button_cpp = KeyboardButton(text='/C++')
button_java = KeyboardButton(text='/Java')
button_php = KeyboardButton(text='/PHP')
button_back = KeyboardButton(text='/<Back')


# main keybord
main_keyboard = ReplyKeyboardMarkup(keyboard=[[button_load, button_show, button_delete], # ,
                                              [button_parse, button_prog_lang, button_doc]], resize_keyboard=True)
# second keyboard
second_keyboard = ReplyKeyboardMarkup(keyboard=[[button_python, button_cpp],
                                                [button_java, button_php],
                                                [button_back]], resize_keyboard=True)
