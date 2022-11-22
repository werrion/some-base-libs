import PySimpleGUI as Sg
import traceback
import os
import webbrowser


"""
Create UI windows
Have bug in lib - not work keyboard shortcuts for not_eng languages, fix by interception keyboard press

"""
version = "Ver. 12.12.12"
CHECK_STATUS = list()


HELP = """
Here will be help text coming soon...
"""


def checking_mandatory_settings_for_start(switch_status_check="All"):
    def check_files_before_start(parameter):
        # some funcs
        pass
        files_found = list()
        files_not_found = list()
        return files_found, files_not_found

    if switch_status_check == 'test1':
        status_check = check_files_before_start(parameter="test1 files")
        return status_check

    if switch_status_check == 'test2':
        status_check = check_files_before_start(parameter="test2 files")
        return status_check

    if switch_status_check == 'All':
        overall_status = list()
        status_check1 = check_files_before_start(parameter="test1 files")
        # overall_status.append(fail_status_check1)
        status_check2 = check_files_before_start(parameter="test2 files")
        # overall_status.append(fail_status_check2)

        # check all tests status
        if overall_status:
            # current_logger.error_log(f"Checking_mandatory_settings_for_start - {overall_status}")
            return overall_status
        else:
            return True


def start():
    # some funcs
    pass


def create_ui():

    def update_text(string_text, string_place):
        text_elem = window[string_place]
        text_elem.update(string_text)

    Sg.theme('DarkAmber')

    layout = [
        [Sg.Button('Help', enable_events=True, key='-Help-'),
         Sg.Button('Open link', enable_events=True, key='-OpenUtilityDoc-'),
         Sg.Text("", size=(56, 1)),
         Sg.Text(version)],
        [Sg.Text("Select folder with XMLs: ", size=(25, 1)),
         Sg.In(size=(50, 1), enable_events=True, disabled=True, readonly=True, key="-FOLDER-",
               disabled_readonly_background_color='#705e52',
               tooltip=r"Example: C:\Users\PC3\Desktop\data\Files\Cache"),
         Sg.FolderBrowse()],
        [Sg.Text('Insert link to doc', size=(25, 1)),
         Sg.InputText('', size=(50, 1), justification='center', key='-DOC_PATH-',
                      tooltip=r"Example: "
                              r"https://docs.google.com/spreadsheets/d/1QWOdFJ2D63dfdf2pgODLDFlqnOnd_uNLxzQ-cKtpZI/"
                              r"edit#gid=913670")],
        [Sg.Button('START Parsing ', enable_events=True, key='-START_PARSING-',
                   tooltip=r"Lets the battle has begun!"),
         Sg.Text(' '*21),
         Sg.Text('Event placement in balance doc ', size=(25, 1)),
         Sg.OptionMenu(values=['Upper Event', 'Lower Event'], size=(15, 1),
                       default_value='Select allocation', key='-DOC_PLACE-')],
        [Sg.Text("Output: ")],
        [Sg.Text('First choose folder with XMLs files for parsing', key='-OUTPUT_TEXT-')],
        [Sg.Text('', key='-STATUS_TEXT-')],
        [Sg.Text('', key='-END_TEXT-')],
        [Sg.Text('', key='-ERROR-')]]

    def on_key_release(event):
        ctrl = (event.state & 0x4) != 0
        if event.keycode == 88 and ctrl and event.keysym.lower() != "x":
            event.widget.event_generate("<<Cut>>")

        if event.keycode == 86 and ctrl and event.keysym.lower() != "v":
            event.widget.event_generate("<<Paste>>")

        if event.keycode == 67 and ctrl and event.keysym.lower() != "c":
            event.widget.event_generate("<<Copy>>")

    window = Sg.Window('Test Utility', layout, auto_size_text=True, finalize=True)
    window.TKroot.bind_all("<Key>", on_key_release, "+")

    while True:
        event, values = window.read()

        if event == '-Help-':
            Sg.popup(HELP, title='Help', line_width=150, font=('', '11'))

        elif event == '-OpenUtilityDoc-':
            webbrowser.open(f'https://****************', new=2)

        elif event == "-FOLDER-":
            check_working_files = False
            # check_working_files = checking_mandatory_settings_for_start(switch_status_check='test1')
            if check_working_files:
                # current_logger.debug_log("Files check - OK")
                update_text("All files find and ready to start", '-OUTPUT_TEXT-')
                # Config.set_xml_path(values["-FOLDER-"])
            else:
                update_text(
                    f"Working files NOT found! Try change folder! \n We have only: \n"
                    f"Need: ", '-OUTPUT_TEXT-')

        elif event == "-DOC_PATH-":
            check_path = str()
            # check_path = check_working_files = checking_mandatory_settings_for_start(switch_status_check='test2')
            if check_path is True:
                # current_logger.debug_log(f"Balance doc OK, Path: {values['-DOC_PATH-']}")
                update_text("Balance doc ready, you can start...", '-OUTPUT_TEXT-')
            else:
                # current_logger.error_log(f"Balance doc NOT found! Path: {values['-DOC_PATH-']}")
                update_text("Balance doc NOT found! Try change path!", '-OUTPUT_TEXT-')

        elif event == '-START_PARSING-':
            # current_logger.debug_log(f"User press START_PARSING")
            if values["-FOLDER-"] == '':
                update_text("You must select folder with XMLs first!", '-OUTPUT_TEXT-')
                # current_logger.error_log(f"User press START_PARSING but empty FOLDER! ")
            elif values["-DOC_PATH-"] == '':
                update_text("You must insert google doc with Happy Hours balance first!", '-OUTPUT_TEXT-')
                # current_logger.error_log(f"User press START_PARSING but empty Doc link! ")
            elif values["-DOC_PLACE-"] == 'Select allocation':
                update_text("You need select event place in balance first!", '-OUTPUT_TEXT-')
                # current_logger.error_log("User press START_PARSING but not select event in doc place! ")

            else:
                error_description = str()
                start_check = checking_mandatory_settings_for_start(switch_status_check="All")

                if not start_check:
                    update_text("test for start - FAIL!", '-OUTPUT_TEXT-')
                    # current_logger.error_log(f"test for start - FAIL!")

                else:
                    # Config.event_order = values["-DOC_PLACE-"]
                    status_check = True

                    # current_logger.debug_log(f"User start parce...")
                    # Config.clear_check_status()
                    # slack_report.send_using_message()

                    try:
                        start()

                    except Exception:
                        status_check = False
                        update_text(f"Crash!!! \n Error: \n{traceback.format_exc()}", '-OUTPUT_TEXT-')
                        # slack_report.send_crash_message(traceback.format_exc())
                        error_description = traceback.format_exc()
                        # current_logger.error_log(f"CRASH!!! \n{error_description}")
                        # slack_report.send_file_to_crash_channel(file_path=current_logger.file_name)
                        # slack_report.send_file_to_crash_channel(
                        #    file_path=Path(Config.xml_path) / Path('WORKING FILE NAME '))
                    finally:

                        if status_check:
                            update_text("Operation successful finished!", '-OUTPUT_TEXT-')
                            # update_text(Errors_status.get_errors_text(), '-ERRORS_TEXT-')
                            # current_logger.debug_log(f"Operation finished! Errors_status: \n
                            # {Errors_status.get_errors_text()}")

                        else:
                            update_text(f"Operation FAIL! \nError: \n{error_description}", '-OUTPUT_TEXT-')
                            update_text("Contact the developer for help, attach a log and a screenshot!", '-END_TEXT-')

        elif event == Sg.WIN_CLOSED:
            # current_logger.debug_log(f'User_push WIN_CLOSED')
            break

    window.close()


create_ui()