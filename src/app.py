import panel as pn
import param


class GoogleMapViewer(param.Parameterized):
    continent = param.ObjectSelector(default='Asia',
                                     objects=['Africa', 'Asia', 'Europe'])

    country = param.ObjectSelector(default='China',
                                   objects=['China', 'Thailand', 'Japan'])

    _countries = {'Africa': ['Ghana', 'Togo', 'South Africa', 'Tanzania'],
                  'Asia': ['China', 'Thailand', 'Japan'],
                  'Europe': ['Austria', 'Bulgaria', 'Greece', 'Portugal',
                             'Switzerland']}

    @param.depends('continent', watch=True)
    def _update_countries(self):
        countries = self._countries[self.continent]
        self.param['country'].objects = countries
        self.country = countries[0]

    @param.depends('country')
    def view(self):
        iframe = """
        <iframe width="800" height="400" src="https://maps.google.com/maps?q={country}&z=6&output=embed"
        frameborder="0" scrolling="no" marginheight="0" marginwidth="0"></iframe>
        """.format(country=self.country)
        return pn.pane.HTML(iframe, height=400)


viewer = GoogleMapViewer(name='Google Map Viewer')
application = pn.Row(viewer.param, viewer.view)

pn.serve(application)
