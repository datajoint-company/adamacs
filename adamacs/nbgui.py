import ipywidgets
from adamacs import subject
from IPython.display import clear_output, display

class MouseEntry(object):
    def __init__(self):
        self.sub = subject.Subject()
        self.columns = self.sub.fetch().dtype.names
        self.widgets = {}
        for col in self.columns:
            curr_widget = ipywidgets.widgets.Text(
            value=col,
            placeholder='Type something',
            description=col,
            disabled=False)
            self.widgets[col] = curr_widget

        self.button = ipywidgets.widgets.Button(
            description='Enter Data',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to enter data',
            icon='database' # (FontAwesome names without the `fa-` prefix)
        )
        self.button.on_click(self.button_on_click)

        self.app = ipywidgets.widgets.VBox((*self.widgets.values(), self.button))
    
    def button_on_click(self, b):
        data = [self.widgets[x].value for x in self.widgets]
        self.sub.insert1(data)
        clear_output(wait=True)
        display(self.app)

