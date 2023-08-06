<%inherit file="base.py.mako"/>
<%block name="imports" filter="trim">
${self.pathlib_import()}
import pygubu
${import_lines}
</%block>

<%block name="class_definition" filter="trim">
class ${class_name}:
    def __init__(self, master=None):
        # build ui
${widget_code}
        # Main widget
        self.mainwindow = self.${main_widget}
    
    def run(self):
        self.mainwindow.mainloop()

${callbacks}\
</%block>
