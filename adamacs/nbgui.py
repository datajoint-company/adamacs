import ipywidgets
from adamacs import subject
from IPython.display import clear_output, display
import ipysheet

class MouseEntry(object):
    """DEPRECATED. REMOVE SOON."""
    def __init__(self):
        self.sub = subject.Subject()
        self.columns = self.sub.fetch().dtype.names
        self.widgets = {}
        for col in self.columns:
            curr_widget = ipywidgets.widgets.Text(
            value='',
            placeholder='',
            description=col,
            disabled=False)
            self.widgets[col] = curr_widget

        self.upload_button = ipywidgets.widgets.Button(
            description='Upload Data',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to upload data',
            icon='database' # (FontAwesome names without the `fa-` prefix)
        )

        self.query_button = ipywidgets.widgets.Button(
            description='Query',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to upload data',
            icon='table' # (FontAwesome names without the `fa-` prefix)
        )

        self.upload_button.on_click(self.button_on_click)

        self.app = ipywidgets.widgets.VBox((*self.widgets.values(), self.upload_button))
    
    def upload_button_on_click(self, b):
        data = [self.widgets[x].value for x in self.widgets]
        self.sub.insert1(data)
        clear_output(wait=True)
        display(self.app)

class MouseEntrySheet(object):
    def __init__(self):
        self.sub = subject.Subject()
        self.columns = self.sub.fetch().dtype.names
        self.widgets = {}

        self.sheet = ipysheet.sheet(key='main', rows=10, columns=len(self.columns), column_headers=self.columns, row_headers=False)
        # self.ipysheet = ipysheet  # Check if that makes sense
        self.rows = []
        for x in range(self.sheet.rows):
            self.rows.append(ipysheet.row(x, ['']*self.sheet.columns))

        self.upload_button = ipywidgets.widgets.Button(
            description='Upload Data',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to upload data',
            icon='database' # (FontAwesome names without the `fa-` prefix)
        )
        
        self.query_button = ipywidgets.widgets.Button(
            description='Query',
            disabled=False,
            button_style='', # 'success', 'info', 'warning', 'danger' or ''
            tooltip='Click to query data',
            icon='table' # (FontAwesome names without the `fa-` prefix)
        )

        self.query_able = {'Lab': subject.Lab,
                           'Line': subject.Line,
                           'User': subject.User,
                           'Project': subject.Project,
                           'Protocol': subject.Protocol}

        self.query_dropdown = ipywidgets.widgets.Dropdown(
            options=list(self.query_able.keys()),
            value=list(self.query_able.keys())[0],
            description='Query Table:',
            disabled=False,
        )

        self.upload_button.on_click(self.upload_button_on_click)
        self.query_button.on_click(self.query_button_on_click)
        self.buttons = ipywidgets.widgets.HBox((self.upload_button, self.query_button, self.query_dropdown))
        self.app = ipywidgets.widgets.VBox((self.sheet, self.buttons))
    
    def upload_button_on_click(self, b):
        for row in self.sheet.cells:
            if row.value[0]:
                self.sub.insert1(row.value)
        clear_output(wait=True)
        display(self.app)

    def query_button_on_click(self, b):
        clear_output(wait=True)
        display(self.app)
        display(self.query_able[self.query_dropdown.value]())