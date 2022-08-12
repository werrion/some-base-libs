import PySimpleGUI as Sg
from models.logging import Logging
import keyboard
import py_win_keyboard_layout


"""
Create UI windows
Have bug in lib - not work keyboard shortcuts for not_eng languages, fix by interception keyboard press

"""

current_logger = Logging(file_name='Log_work.log')
CHECK_STATUS = list()


HELP = """
Here will be help text coming soon...
"""


def start():
    # some funcs
    pass


def create_ui():
    global CHECK_STATUS
    current_logger.debug_log(f"Create UI window")

    # del old log_file on start
    current_logger.del_log_file()

    def update_text(string_text, string_place):
        text_elem = window[string_place]
        text_elem.update(string_text)

    Sg.theme('DarkAmber')

    layout = [
        [Sg.Button('Help', enable_events=True, key='-Help-'), Sg.Text("", size=(64, 1)), Sg.Text("Ver. 11.08.22")],
        [Sg.Text("1-Step: Select folder with XMLs: ", size=(25, 1)),
         Sg.In(size=(50, 1), enable_events=True, key="-FOLDER-",
               tooltip=r"Example: C:\Users\***\Desktop\data"),
         Sg.FolderBrowse()],
        [Sg.Text('2-Step: Insert link to doc', size=(25, 1)),
         Sg.InputText('', size=(50, 1), justification='center', right_click_menu=['', ['Paste']], key='-DOC_PATH-',
                      tooltip=r"Example: https://docs.google.com/spreadsheets/d/1QWOdFJxzQ-cKtpZI/edit#gid=913670444")],
        [Sg.Button('START Parse ', enable_events=True, key='-START_PARSING-',
                   tooltip=r"Let's the battle has begone!")],
        [Sg.Text("Output: ")],
        [Sg.Text('First choose folder with XMLs files for parsing', key='-OUTPUT_TEXT-')],
        [Sg.Text('', key='-STATUS_TEXT-')],
        [Sg.Text('', key='-END_TEXT-')]]

    window = Sg.Window('Check xml for google doc', layout, auto_size_text=True)
    mline: Sg.Multiline = window['-DOC_PATH-']

    def check_intercept():
        # if we have eng (US or UB lang) - pass: ctrl+V working, if we have another lang - pull the past func
        lang_now = py_win_keyboard_layout.get_foreground_window_keyboard_layout()
        if lang_now not in {67699721, 134809609}:
            mline.Widget.insert(Sg.tk.INSERT, window.TKroot.clipboard_get())

    # intercept Сtrl + V for another lang for paste link in utility
    keyboard.add_hotkey('Ctrl + V', lambda: check_intercept())

    while True:
        event, values = window.read()

        if event == '-Help-':
            Sg.popup(HELP, title='Help', line_width=150, font=('', '11'))

        if event == '-START_PARSING-':
            current_logger.info_log(f"User press START_PARSING")
            if values["-FOLDER-"] == '':
                update_text("You must select folder with XMLs first!", '-OUTPUT_TEXT-')
                current_logger.warning_log(f"User press START_PARSING but empty FOLDER! ")
            elif values["-DOC_PATH-"] == '':
                update_text("You must insert google doc with Happy Hours balance first!", '-OUTPUT_TEXT-')
                current_logger.warning_log(f"User press START_PARSING but empty Doc link! ")
            else:
                current_logger.info_log(f"User start parce...")
                start()

                if CHECK_STATUS[0] is True:
                    update_text("!!!TEST SUCCESS!!!", '-OUTPUT_TEXT-')
                    update_text(
                        f"XML-s tested and equally to doc!", '-STATUS_TEXT-')

                    # output for OK tests
                    list_success_test_events = list()
                    for event in CHECK_STATUS[1]:
                        list_success_test_events.append(event)
                        list_success_test_events.append(' - OK \n')
                    update_text(f"list tested events: \n "
                                f"{' '.join(list_success_test_events)}", '-END_TEXT-')
                    current_logger.debug_log(f"CHECK_STATUS OK, all test success")

                if CHECK_STATUS[0] is False:
                    update_text("!!!TEST FAIL!!!", '-OUTPUT_TEXT-')
                    update_text(f"XML-s tested and there are no coincidences with the Doc! "
                                f"\nSuccess test for: {CHECK_STATUS[1]}", '-STATUS_TEXT-')
                    current_logger.warning_log(f"CHECK_STATUS FAIL! Status: {CHECK_STATUS}")

        if event == "-FOLDER-":
            current_logger.info_log(f"user press -FOLDER-, start check")
            # check folder for rules
            # check_folder = check_find_xml_in_folder(values["-FOLDER-"])
            # if check_folder:
            #     current_logger.debug_log(f"XML folder OK, XML_PATH: {values['-FOLDER-']}")
            #     update_text("Xml-s find and ready to start", '-OUTPUT_TEXT-')
            # else:
            #     update_text("Xmls NOT find! Try change folder!", '-OUTPUT_TEXT-')

        if event == "-DOC_PATH-":
            current_logger.info_log(f"user press -DOC_PATH-, start check")
            # check DOC_PATH for rules

        if event == Sg.WIN_CLOSED:
            current_logger.debug_log(f'user_push WIN_CLOSED')
            break

    window.close()


create_ui()
