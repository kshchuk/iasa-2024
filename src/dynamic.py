import panel as pn


class DynamicContentHolder:
    def __init__(self):
        self._holder = pn.Column()
        self._active_content = pn.Row()
        self._holder.append(self._active_content)

    def set_content(self, widget):
        temp_content = pn.Row(widget)
        self._holder.append(temp_content)
        self._active_content.clear()
        self._active_content = temp_content

    def get_content(self):
        return self._active_content[0]

    def set_holder(self, panelT):
        self._holder = panelT

    def get_holder(self):
        return self._holder
