# -*- coding: utf-8 -*-
"""
Created on Thu Jun 18 22:36:11 2015

@author: thomasaref
"""

if __name__=="__main__2":
    #a=EBLRectangle(name="blah")
    b=EBL_Item(name="blah")
#    print dir(b.get_member("polylist"))
    b.polylist=[R(), R()]

#    print b.polylist[0].verts
#    print dir(b.get_member("polylist"))
#    print b.get_member("polylist")
    class subarr(Atom):
        name=Unicode()
        polyindex = Int()
        polylength=Int()
        instr=Typed(Atom)
        show_value=Typed(EBLPolygon)
        #show_poly=ContainerList()
        show_verts=ContainerList()
        vertindex = Int()
        vertlength=Int()

        changed=Bool(False)
        #mytype=Enum(float, tuple, EBL_Item.EBLPolygon)

        def get_polyarr(self, polyindex=None):
            if polyindex==None:
                return getattr(self.instr, self.name)
            return getattr(self.instr, self.name)[polyindex]

        def get_vertarr(self, polyindex=None, vertindex=None):
            polyarr=self.get_polyarr(polyindex)
            if polyindex==None or vertindex==None:
                return polyarr
            return polyarr[vertindex]

        def __init__(self, **kwargs):
            super(subarr, self).__init__(**kwargs)
            self.instr.observe(self.name, self.value_changed)
            if self.polylength>=0:
                self.instr.polylist[self.polyindex].observe('verts', self.verts_changed)

        def _default_polylength(self):
            return len(self.get_polyarr())-1

        def _default_vertlength(self):
           if self.polylength>=0:
               return len(self.get_vertarr())-1

        def value_changed(self, change):
            self.polylength=len(change['value'])-1
            if self.polyindex >= self.polylength:
                self.polyindex=self.polylength
            self.polyindex_changed({})
            self.show_value  #call to update

        def coercer(self):
            try:
                self.show_value=self.get_polyarr(self.polyindex)
            except IndexError:
                self.show_value=EBLPolygon()

        def conve(self):
            return self.show_value

        @observe('polyindex')
        def polyindex_changed(self, change):
            self.changed=True
            self.coercer()
            self.changed=False

        def _observe_show_value(self, change):
            if self.changed==False:
                try:
                    getattr(self.instr, self.name)[self.polyindex]=self.conve() #tuple(self.show_value)
                except IndexError:
                    getattr(self.instr, self.name).append(self.conve())

        def polyinsert(self):
            self.get_arr().insert(self.polyindex, self.conve())

        def polypop(self):
            self.get_arr().pop(self.polyindex)

    class subarr2(subarr):
        show_value=ContainerList(default=[0.0,0.0])

        def coercer(self):
            try:
                self.show_value=list(self.get_arr(self.index))
            except IndexError:
                self.show_value=[0.0, 0.0]

        def conve(self):
            return tuple(self.show_value)

    c=subarr(instr=b, name="polylist")
    print c.index
    print c.length
    c.index=1
    b.polylist.append(R())
    print c.length        #print a.view
    print c.show_value.verts    #print a.verts
    d=subarr2(instr=c.show_value, name="verts")
    print d.length
    print d.show_value
    d.index=1
    print d.show_value
        #b=EBL_Item()
        #print dir(b.get_member("polylist"))
        #print b.get_member("polylist").validate_mode[1].validate_mode[1]
        #b.show()
        #print a.verts
        #a.verts.append((6,5))
        #print a.verts
        #print a.get_type("poly3")
        #a.polylist=["a.poly3"]
        #print ebl_boss.instruments[0].name
    log_debug(2)

if __name__=="__main__3":
    class PolygonWatch(Atom):
        #verts=ContainerList(default=[(0.0, 0.0)])
        polygon=Typed(EBLPolygon)
        vertindex=Int()
        vertx=Float()
        verty=Float()
        changed=Bool(False)

        def print_poly(self):
            print self.polygon.verts
            for i,x in enumerate(self.polygon.verts):
                self.vertindex=i
                print self.vertindex, self.vertx, self.verty

        def update_xy(self):
            if not self.changed:
                self.changed=True
                self.vertx=self.polygon.verts[self.vertindex][0]
                self.verty=self.polygon.verts[self.vertindex][1]
                self.changed=False
        @observe("polygon.verts")
        def _observe_verts(self, change):
            self._observe_vertindex({}) #update_xy()

        def _observe_vertindex(self, change):
            if self.vertindex>=len(self.polygon.verts)-1:
                self.vertindex=len(self.polygon.verts)-1
            if self.vertindex<0:
                self.vertindex=0
            self.update_xy()

        def _observe_vertx(self, change):
            if not self.changed:
                self.changed=True
                old_verty=self.polygon.verts[self.vertindex][1]
                self.polygon.verts[self.vertindex]=(self.vertx, old_verty)
                self.changed=False

        def _observe_verty(self, change):
            if not self.changed:
                self.changed=True
                old_vertx=self.polygon.verts[self.vertindex][0]
                self.polygon.verts[self.vertindex]=(old_vertx, self.verty)
                self.changed=False

    class EBL_ItemWatch(Atom):
        polywatch=Typed(PolygonWatch)
        ebl_item=Typed(EBL_Item)
        polyindex=Int()

        def _default_polywatch(self):
            return PolygonWatch(polygon=self.ebl_item.polylist[0])

        def print_polylist(self):
            oldpolyindex=self.polyindex
            for i, poly in enumerate(self.ebl_item.polylist):
                self.polyindex=i
                self.polywatch.print_poly()
            self.polyindex=oldpolyindex

        @observe("ebl_item.polylist")
        def _observe_polylist(self, change):
            self._observe_polyindex({}) #self._observe_polylist[self.polyindex]._observe_vertindex({})


        def _observe_polyindex(self, change):
            if self.polyindex>=len(self.ebl_item.polylist)-1:
                self.polyindex=len(self.ebl_item.polylist)-1
            if self.polyindex<0:
                self.polyindex=0
            self.polywatch=PolygonWatch(polygon=self.ebl_item.polylist[self.polyindex])
            self.polywatch._observe_vertindex({})

    a=EBL_Item(name="blah", polylist=[R(), R()])
    b=EBL_ItemWatch(ebl_item=a)
    b.print_polylist()
    a.polylist[0].verts=[(0, 0), (1,2), (3,4)]
    print b.polywatch.vertindex
    print b.polywatch.vertx
    b.polywatch.vertx=5
    b.print_polylist()
    a.show()

#needs some work
        """stand alone for showing instrument. Shows a modified boss view that has the instrument as a dockpane"""
#        with imports():
#            from EBL_enaml import EBMain
#        app = QtApplication()
#        view = EBMain(base=self, boss=self.boss)
#        view.show()
#        app.start()
#    def show(self):
#        """stand alone for showing instrument. Shows a modified boss view that has the instrument as a dockpane"""
#        with imports():
#            from enaml_Boss import EBLItemMain
#        try:
#            app = QtApplication()
#            view = EBLItemMain(eblitemin=self, boss=self.boss)
#            view.show()
#            app.start()
#        finally:
#            pass #self.boss.close_all()

#b=R()


    #def show(self):
    #    """stand alone for showing instrument. Shows a modified boss view that has the instrument as a dockpane"""
    #    with imports():
    #        from enaml_Boss import EBLItemMain
    #    try:
    #        app = QtApplication()
    #        view = EBLItemMain(eblitemin=self, boss=self.boss)
    #        view.show()
    #        app.start()
    #    finally:
    #        pass #self.boss.close_all()

    #def plot(self):
    #    self.boss.plot.add_poly_plot(n=self.n, verts=self.verts, cn=self.color, polyname=self.name)
    #    self.boss.plot.plot.request_redraw()
#    def poly2gds(self):
#        """converts polygon to gds format and returns list of commands (text based)"""
#        tlist=[] #temporary list of string commands
#        #xr, yr, wr, hr = 10000.0*xr, 10000.0*yr, 10000.0*wr, 10000.0*hr #scale up useful for debugging
#        tlist.append('BOUNDARY\n')
#        tlist.append('LAYER: {0}\n'.format(self.layer))
#        tlist.append('DATATYPE: {0}\n'.format(self.cn))
#        vlist=[]
#        vlist.append('XY: ')
#        for v in self.verts:
#            vlist.append('{0}, {1}, '.format(int(v[0]*10000), int(v[1]*10000)))
#        vlist[-1]=vlist[-1][:-2]
#        vlist.append('\n')
#        tlist.append(''.join(vlist))
#        tlist.append('ENDEL\n')
#        return tlist
