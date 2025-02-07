import PySimpleGUI as sg
from serial.tools import list_ports as tools
import back

sg.theme('Dark Grey 16')

setfil_layout = [
    [sg.Text('Average:'), sg.Push(), sg.Input(key='-AVERAGE-', size=(15, 1))],
    [sg.Text('Coefficient'), sg.Push(), sg.Input(key='-COEF-', size=(15, 1))],
    [sg.Push(), sg.OK(size=(7, 1)), sg.Push()]
]
frame_parametrs = [
    [sg.Text('Port:'), sg.Push(), sg.Combo(values=[info.device for info in tools.comports()], size=(8, 4), key='-COM-',
                                           default_value=[info.device for info in tools.comports()][0],
                                           enable_events=True, readonly=True)],
    [sg.Text('Speed:'), sg.Push(), sg.Combo(values=['1200', '2400', '4800', '9600', '14400', '19200', '28800', '38400'],
                                            size=(8, 4), key='-SPEED-', default_value='9600', readonly=True)],
    [sg.Text('Bits:'), sg.Push(), sg.Combo(values=['7', '8'],
                                           size=(8, 4), key='-BITS-', default_value='8', readonly=True)],
    [sg.Text('Stop bits:'), sg.Push(), sg.Combo(values=['1', '2'],
                                                size=(8, 4), key='-SBITS-', default_value='1', readonly=True)],
    [sg.Text('Parity:'), sg.Push(), sg.Combo(values=['None', 'Even', 'Odd', 'Mark', 'Space'],
                                             size=(8, 4), key='-PARITY-', default_value='None', readonly=True)],

    [sg.Button('Connect', key='-CONNECT-', bind_return_key=True)]
]

frame_commands = [
    [sg.Button('MCAL', key='-MCAL-', size=(7, 1))],
    [sg.Button('SETFIL', key='-SETFIL-', size=(7, 1))],
    [sg.Button('Other', key='-OTHER-', size=(7, 1))],
    [sg.Text(size=(40, 1), key='-LINE-OUTPUT-')],
]

frame_output = [
    [sg.Text('All')],
    [sg.Multiline(size=(40, 10), key='-ALL-', autoscroll=True)],
    [sg.Push(), sg.Button('Clear', key='-CLEARALL-')],
    [sg.HorizontalSeparator()],
    [sg.Text('Responses to commands')],
    [sg.Multiline(size=(40, 10), key='-SPEC-', autoscroll=True)],
    [sg.Push(), sg.Button('Clear', key='-CLEARSPEC-')],
]
col1 = [
    [sg.Frame('Parametrs', frame_parametrs, size=(160, 185))],
    [sg.Frame('Commands', frame_commands, size=(160, 220), element_justification='c')]
]

col2 = [
    [sg.Frame('Answers', frame_output)]
]
layout = [
    [sg.vtop(sg.Column(col1, element_justification='c')), sg.Column(col2)]
          ]

window = sg.Window('Module', layout,)
while True:

    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED:
        break
    elif event == '-COM-':
        window['-COM-'].update(values=[info.device for info in tools.comports()],
                               value=[info.device for info in tools.comports()][0], size=(8, 4))
    elif event == '-CONNECT-':
        if not window['-CONNECT-'].metadata or window['-CONNECT-'].metadata is None:
            window['-CONNECT-'].update('Disconnect')
            window['-CONNECT-'].metadata = True
            speed = values['-SPEED-']
            port = back.initcom(values['-COM-'], int(values['-SPEED-']), values['-PARITY-'][0], int(values['-SBITS-']),
                                int(values['-BITS-']))
        else:
            window['-CONNECT-'].update('Connect')
            window['-CONNECT-'].metadata = False
            port.close()
    elif event == '-OTHER-':
        d = sg.popup_get_text('Command')
    elif event == '-SETFIL-':
        d = (sg.Window('SETFIL', setfil_layout).read(close=True)[1])

window.close()
