from kivy.graphics import Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget


class ReportCell(BoxLayout):
    
    def __init__(self, **kw):
        super(ReportCell, self).__init__(**kw)
        self.data = kw['data']
        with self.canvas.before:
            a = .5
            b = .3
            Color(b, a, b, 1.)
            self.rect_run = Rectangle()
            Color(a, b, b, 1.)
            self.rect_miss = Rectangle()
            Color(b, b, a, 1.)
            self.rect_excl = Rectangle()
        lbl = Label(size_hint=(1, 1))
        lbl.text = '%s %s (%s/%s)' % (self.data[0], self.data[3], self.data[1],
                self.data[2])
        self.add_widget(lbl)
        self.bind(pos=self._update_rect, size=self._update_rect)
        
    def _update_rect(self, *args):
        h = self.height
        w = self.width
        if float(self.data[1]) == 0.:
            return
        run_pct = (float(self.data[1]) - float(self.data[2])) / float(self.data[1])
        miss_pct = float(self.data[2]) / float(self.data[1])
        excl_pct = 1. - run_pct - miss_pct
        # print run_pct, miss_pct, excl_pct
        self.rect_run.pos = self.pos
        self.rect_run.size = w * run_pct, h
        self.rect_miss.pos = self.rect_run.pos[0] + self.rect_run.size[0], self.rect_run.pos[1]
        self.rect_miss.size = w * miss_pct, h
        self.rect_excl.pos = self.rect_miss.pos[0] + self.rect_miss.size[0], self.rect_miss.pos[1]
        self.rect_excl.size = w * excl_pct, h
    