# -*- coding: utf-8 -*-
"""
Created on Sun Jan 10 17:30:54 2016

@author: thomasaref
"""


#        updates=[attr[0] for attr in getmembers(self) if attr[0].startswith(_UPDATE_PREFIX_)]
#        for update_func in updates:
#            f=getattr(self, update_func).im_func
#            argcount=f.func_code.co_argcount
#            argnames=list(f.func_code.co_varnames[0:argcount])
#            if "self" in argnames:
#                argnames.remove("self")
#            f.argnames=argnames
#            for name in argnames:
#                upd_list=self.get_tag(name, "update", [])
#                if update_func not in upd_list:
#                    upd_list.append(update_func)
#                    self.set_tag(name, update=upd_list)
#        for param in self.default_list:
#            if param not in kwargs and not hasattr(self, "_default_"+param) and hasattr(self, "_update_"+param):
#                setattr(self, param, self.get_default(param))
#            else:
#                setattr(self, param, getattr(self, param))

#    def do_update(self, name):
#        log_debug(name)
#        if self.updating:
#            self.updating=False
#            results=self.search_update(name)
#            for key in results:
#                if key!=name:
#                    setattr(self, key, results[key])
#            self.updating=True
#
#    def search_update(self, param, results=None):
#        if results is None:
#            results=OrderedDict()
#            results[param]=getattr(self, param)
#        for update_func in self.get_tag(param, "update", []):
#            param=update_func.split("_update_")[1]
#            if not param in results.keys():
#                argnames=get_attr(getattr(self, update_func).im_func, "argnames")
#                if argnames is not None:
#                    argvalues= [results.get(arg, getattr(self, arg)) for arg in argnames]
#                    kwargs=dict(zip(argnames,argvalues))
#                    result=getattr(self, update_func)(**kwargs)
#                    results[param]=result
#                    self.search_update(param, results)
#        return results
#
#    def get_default(self, name, update_func=None):
#        if update_func is None:
#            update_func="_update_"+name
#        argnames=getattr(self, update_func).im_func.argnames
#        argvalues= [getattr(self, arg) for arg in argnames]
#        kwargs=dict(zip(argnames,argvalues))
#        return getattr(self, update_func)(**kwargs)


#def shower2(*agents):
#    """a powerful showing function for any Atom object(s). Checks if object has a view_window property and otherwise uses a default.
#    also provides a show control of the objects"""
#    app = QtApplication()
#    with imports():
#        from chief_e import agentView, chiefView, basicView
#    for n, a in enumerate(agents):
#        view=getattr(a, "view_window", agentView(agent=a))
#        view.name=getattr(a, "name", "agent_{0}".format(n))
#        loc_chief=getattr(a, "chief", None)
#        view.title=view.name
#        view.show()
#        if loc_chief is not None:
#            if not loc_chief.show_all and n!=0:
#                view.hide()
#    if loc_chief is None:
#        view=basicView(title="Show Control", name="show_control")
#    else:
#        if hasattr(loc_chief, "view_log"):
#            if loc_chief.view_log.visible:
#                loc_chief.view_log.show()
#        if hasattr(loc_chief, "view_window"):
#            view=loc_chief.view_window
#        else:
#            view=chiefView(title="Show Control", name="show_control", chief=loc_chief)
#    view.show()
#    app.start()
#
#def find_windows(a, tl=[]):
#    for name in a.members():
#        member=getattr(a, name)
#        if hasattr(member, "view_window"):
#            tl.append(name)
#            print tl
#            find_windows(member, tl)
#
#    return tl
#
##self.plot.view_window.show()
##        view=self.jdf.view_window
##        view.show()
##        view.hide()


#enamldef chiefView(coreWindow): sv:
#    """a default view of the chief for agents with a chief"""
#    attr chief
#    title = chief.name
#    activated :: chief.activated()
#    Conditional:
#        condition = getattr(chief, "run_func_names", []) != []
#        VGroup:
#            GroupBox:
#                Looper:
#                    iterable=chief.run_func_names
#                    PushButton:
#                        text = loop_item
#                        clicked :: chief.run_func_dict[loop_item]()
#            PushButton:
#                text = "Run All"
#                clicked ::
#                    log_debug(sv.windows)
#                    print sv.agent_wins
#                    print sv.all_wins
#                    print sv.other_wins
#                    #chief.run_all()
#                tool_tip = "Runs all functions"
#    LogSaveToolBar:
#        pass
#    Conditional:
#        condition = False #sv.chief is not None
#        ToolBar:
#            dock_area="right"
#
#            Action:
#                text = "Plot"
#            #    triggered::
#            #         tagent=[b for b in boss.agents if b.name=="EBL_Item_test"][0]
#            #         tagent.plot(tagent)
#                        #print bossarea.dock_items()[0].name
#                        #show_plot(boss.plot.name+'plot', bossarea, target=bossarea.dock_items()[0].name, ItemType=PlotItem, position="right", plotr=boss.plot)
#                tool_tip = "Show plot"
#
#    WindowToolBar:
#        boss_window:=sv
#    AgentToolBar:
#        boss_window:=sv
#
#    ToolBar:
#        dock_area="left"
#        Conditional:
#            condition = sv.chief is not None
#            Action:
#                separator=True
#            Action:
#                separator=True
#            Action:
#                text="Plots"
#                triggered::
#                    all_showing=sv.all_showing
#                    for w in sv.agent_wins:
#                        print w.name
#                        if all_showing:
#                            w.hide()
#                        else:
#                            w.show()
#                            w.send_to_front()
#                tool_tip = "Show/hide all agents"
#            Action:
#                separator=True
#
#            Looper: #loopy:
#                iterable << sv.chief.plots #a_wins
#                Action:
#                    text = loop_item
#                    tool_tip = "Show/hide plot: {0}".format(loop_item)
#                    #triggered::
#                    #    if loop_item.visible:
#                    #        loop_item.hide()
#                    #    else:
#                    #        loop_item.show()

#enamldef LogSaveToolBar(ToolBar):
#    attr log
#    ToolBar:
#        dock_area="top"
#        Action:
#            text="Log"
#            triggered::
#                log.show()
#                log.send_to_front()
#            tool_tip = "Show log"
#        Action:
#            text="Save"
#            triggered::
#                log_debug(sv.windows)
#        #        savepane.show()
#            tool_tip = "Show save pane"
#        Action:
#            text = "PlotPane"
#         #   triggered:: plotpane.show() #print dir(bossarea) #show_plot(bossarea, boss.plot) #show_pane(dyn_pages, 'Plot')
#         #   tool_tip = "Show plot controls"
