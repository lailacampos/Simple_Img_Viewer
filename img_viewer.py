# Tutorial:
# https://realpython.com/pysimplegui-python/

import PySimpleGUI
import os.path
from PIL import Image

# Window layout in two columns

# Create a nested list of elements that represent a vertical column of the user interface. This will create a Browse
# button that you’ll use to find a folder that has images in it.
file_list_column = [
    [
        PySimpleGUI.Text('Image Folder'),

        # The key parameter is what it's used to identify a specific element in your GUI. For the
        # In() input text control, you give it an identity of "-FOLDER-". You’ll use this later to access the
        # contents of the element.
        PySimpleGUI.In(size=(25, 5), enable_events=True, key='-FOLDER-'),
        PySimpleGUI.FolderBrowse(),
    ],
    [
        # The Listbox element: https://pysimplegui.readthedocs.io/en/latest/#listbox-element

        # The Listbox() element will display a list of paths to the images that you can then choose from to display.
        # You can prefill the Listbox() with values by passing in a list of strings.
        # When you first load up your user interface, you want the Listbox() to be empty, so you pass it an empty list.
        PySimpleGUI.Listbox(
            values=[], enable_events=True, size=(40, 20), key='-FILE LIST-'
        )
    ]
]

# Image viewer column
image_viewer_column = [
    [PySimpleGUI.Text('Choose an image from the list on the left')], # Tells the user that they should choose an image to display.
    [PySimpleGUI.Text(size=(40, 1), key='-IMG NAME-')],  # Displays the name of the selected file.
    [PySimpleGUI.Image(key='-IMAGE-')]
]
# Full layout
layout = [
    [
        PySimpleGUI.Column(file_list_column),
        PySimpleGUI.VSeperator(), # Vertical Separator Element draws a vertical line at the given location.
        PySimpleGUI.Column(image_viewer_column),
    ]
]

window = PySimpleGUI.Window('Image Viewer', layout)

while True:
    # There are 2 return values from a call to Window.read(), an event that caused the Read to return and values a
    # list or dictionary of values.
    #
    # The first parameter event describes why the read completed.

    # The second parameter from a Read call is either a list or a dictionary of the input fields on the Window.
    # By default return values are a list of values, one entry for each input field, but for all but the simplest of
    # windows the return values will be a dictionary. This is because you are likely to use a 'key' in your layout.
    # When you do, it forces the return values to be a dictionary.
    event, values = window.read()
    if event == 'Exit' or event == PySimpleGUI.WIN_CLOSED:
        break

    # Check the event against the "-FOLDER-" key, which refers to the In() element created earlier.
    # Folder name was filled in, make a list of files in the folder.
    if event == '-FOLDER-':
        folder = values['-FOLDER-'] # folder receives the value attributed to the key '-FOLDER-' in the values dictionary.
        try:
            # Get list of files in folder
            # listdir returns a list containing the names of the files in the directory.
            file_list = os.listdir(folder)
        except:
            file_list = []

        file_names = [
            # Filter that list with file names down to only the files with the extension ".png" or ".gif"
            f
            for f in file_list

            # os.path.join(path, *paths)
            # Join one or more path components intelligently. The return value is the concatenation of path and any
            # members of *paths with exactly one directory separator following each non-empty part except the last,
            # meaning that the result will only end in a separator if the last part is empty.
            if os.path.isfile(os.path.join(folder, f)) # os.path.isfile(path) returns True if path is an existing regular file
            and f.lower().endswith('.png', '.gif')
        ]
        window['-FILE LIST-'].update(file_names)

    # If the event equals "-FILE LIST-", then the user has chosen a file in the Listbox(), and you want to update the
    # Image() element as well as the Text() element that shows the selected filename on the right.
    elif event == '-FILE LIST-':  # A file was chosen from the listbox
        try:
            filename = os.path.join(values['-FOLDER-'], values['-FILE LIST-'][0])
            window['-IMG NAME'].update(filename)
            window['-IMAGE-'].update(filename=filename)
        except:
            pass

window.Close()
