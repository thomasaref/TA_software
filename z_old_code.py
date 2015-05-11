# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 10:02:28 2015

@author: thomasaref
"""

#
#class Save_File(Filer):
#    cmd_num=Int()
#    print_log=Bool(True)
#    log_buffer=Dict()
#    point_buffer=Dict(default={"Measurement":{}, "Set Up":{}})
#    string_buffer=Dict(default={"Measurement":{}, "Set Up":{}})
#    buffer_save=Bool(False)
#    comment=Unicode()
#
#    def _default_log_buffer(self):
#        return {"Full Log":""}
#
#    def _default_point_buffer(self):
#        return {"Measurement":{}, "Set Up":{}}
#
#    def _default_string_buffer(self):
#        return {"Measurement":{}, "Set Up":{}}
#
#    @observe( "dir_path")
#    def filedir_path_changed(self, change):
#        """if the file path exists and the file location is changed, this function moves the entire directory to the new location"""
#        if change['type']!='create':
#            old_dir_path=change['oldvalue']
#            if not os.path.exists(self.file_path):
#                if os.path.exists(old_dir_path):
#                    shutil.move(old_dir_path, self.dir_path)
#                    self.update_log("Moved files to: {0}".format(self.dir_path))
#
#    def update_log(self, logstr):
#        """used for logging. if the logstr begins with 'RAN', the cmd num is updated.
#           Printing of the log is available via print log"""
#        if logstr[0:4]=="RAN:":
#            self.cmd_num+=1
#        newstr="[{cmd_num}] {logstr}".format(cmd_num=self.cmd_num, logstr=logstr)
#        if self.print_log:
#            print newstr
#        self.write_to_log(newstr)
#
#    def makedir(self):
#        if not os.path.exists(self.dir_path):
#            makedirs(self.dir_path)
#        if not os.path.exists(self.file_path):
#            self.create_file()
#            self.update_log("Created file at: {0}".format(self.file_path))
#
#    def save_code(self, obj):
#        """saves the code containing the passed in object"""
#        module_path, ext = os.path.splitext(inspect.getfile(obj))
#        code_file_path = module_path + '.py'   # Should get the py file, not the pyc, if compiled.
#        code_file_copy_path = self.dir_path+self.divider+os.path.split(module_path)[1]+".py"
#        if not os.path.exists(code_file_copy_path):
#            shutil.copyfile(code_file_path, code_file_copy_path)
#            self.update_log("Saved code to: {0}".format(code_file_copy_path))
#
#    def full_save(self, obj):
#        """does a full save, making files and directories, flushing the buffers, and saving the code"""
#        self.makedir()
#        self.flush_buffers()
#        self.save_code(obj)
#
#    def write_to_log(self, new_string, log="Full Log"):
#        if self.buffer_save:
#            self.log_buffer[log]=self.log_buffer[log]+new_string+"\n"
#        else:
#            self.save_to_log(new_string, log)
#
#    def flush_buffers(self):
#        if self.buffer_save:
#            self.buffer_save=False
#            for key, item in self.log_buffer.iteritems():
#                self.write_to_log(item, log=key)
#            for group_name, item in self.point_buffer.iteritems():
#                for name, subitem in item.iteritems():
#                    for key, arr in subitem.iteritems():
#                        self.dataset_save(arr, name=name, group_name=group_name)
#            for group_name, item in self.string_buffer.iteritems():
#                for name, subitem in item.iteritems():
#                    for key, newstr in subitem.iteritems():
#                        self.string_save(newstr, name=name, group_name=group_name)
#            self.log_buffer=self._default_log_buffer()
#            self.point_buffer=self._default_point_buffer()
#            self.string_buffer=self._default_string_buffer()
#            self.buffer_save=True
#
#    def data_save(self, data, name="Measurement", group_name="Measurement", append=True):
#        if self.buffer_save:
#            if name not in self.data_buffer[group_name].keys():
#                self.data_buffer[group_name][name]=dict()
#                append=False
#            if type(data) not in [list, ndarray]:
#                data=[data]
#            if append==False:
#                namestr="{0}".format(len(self.data_buffer[group_name][name]))
#                self.data_buffer[group_name][name][namestr]=data
#            else:
#                namestr="{0}".format(len(self.data_buffer[group_name][name])-1)
#                self.data_buffer[group_name][name][namestr].extend(data)
#        else:
#            self.do_data_save(data, name, group_name, append)
#
#    def create_file(self):
#        print "create_file not overwritten"
#
#    def save_to_log(self, logstr, log):
#        print "save_to_log not overwritten"
#
#    def do_data_save(self, data, name, groupname, append):
#        print "do_data_save not overwritten"
#
#from HDF5_functions import create_hdf5, save_hdf5_log, hdf5_data_save
#class Save_HDF5(Save_File):
#    def create_file(self):
#        create_hdf5(self.file_path)
#
#    def save_to_log(self, new_string, log):
#        save_hdf5_log(self.file_path, new_string, log)
#
#    def do_data_save(self, data, name, group_name, append):
#        hdf5_data_save(self.file_path, data, name, group_name, append)
#
#from TXTNP_functions import create_txt, save_txt_log, save_txt_data, save_np_data
#class Save_TXT(Save_File):
#    def create_file(self):
#        create_txt(self.dir_path)
#    def save_to_log(self, new_string, log):
#        save_txt_log(self.dir_path)
#    def do_data_save(self, data, name, group_name, append):
#        save_txt_data(self.dir_path+self.divider, data, name)
#
#class Save_NP(Save_TXT):
#    def do_data_save(self, data, name, group_name, append):
#        save_np_data(self.dir_path+self.divider, data, name)
#
#class Save_DXF(Save_File):
#    pass


#if __name__=="__main__2":
#    hdf5=Save_HDF5()
#    hdf5.write_to_log("yo")
#    hdf5.dataset_save([1,2,3], name="arr")
#    hdf5.point_save(1,name="point")
#    hdf5.string_save("blah")
#f = open('workfile', 'w')
# 'r' when the file will only be read,
#'w' for only writing (an existing file with the same name will be erased),
# 'a' opens the file for appending; any data written to the file is automatically added to the end.
#'r+' opens the file for both reading and writing. The mode argument is optional; 'r' will be assumed if it’s omitted.

#if __name__=="__main__":
#    reader=Read_HDF5(main_dir= 'two tone, flux vs control freq, egate n111dbm, IDT n127dbm  2013-10-12_104752', main_file='meas.h5') #'discard/Saved 2015-02-11_130527',)
#    a=reader.open_and_read()
#    print a['GeneralStepper (110329744)']['attrs'].keys()
    #a=reader.data
#def printname(name):
#    print name
#f.visit(printname)
#f.visititems()
#for line in f:
#        print line,

# f.write('This is a test\n')



    def data_save(self, instr, name, value):
        if not instr.get_tag(name, 'discard', False):
            if instr.get_tag(name, 'save', False):
                group_name="Measurement"
            else:
                group_name="Set Up"
            label=instr.get_tag(name, 'label', name)
            if instr.get_type(name) in (Float, Int, Range, FloatRange, ContainerList, Unicode, Str):
                self.save_hdf5.data_save(value=value, name=label, group_name=group_name)
            elif instr.get_type(name) in (List, Callable):
                pass
            elif instr.get_type(name) in (Bool, Enum):
                self.save_hdf5.data_save(new_string=str(value), name=label, group_name=group_name)
            else:
                log_warning("No save format!")
                
enamldef BossItem(DockItem):
    #attr window
    #dock_area='top'
    name = 'boss'
    title = "boss"
    Container:
        constraints = [hbox(plot_box, vbox(prepare, run, finish, run_measurement, abort, spacer),
                            save_box)]
        #padding = 0

        PushButton: prepare:
            text = "Prepare"
            clicked :: boss.prepare()
        PushButton: finish:
            text = "Finish"
            clicked :: boss.finish()
        PushButton: run:
            text = "Run"
            clicked ::
                boss.run()
#        CheckBox: buffer_save:
#            text = "buffer save"
#            checked := boss.save_hdf5.buffer_save
        PushButton: run_measurement:
            text = "Run Measurement"
            clicked ::
                boss.run_measurement()
        PushButton: abort:
            text = "Abort"
            clicked ::
                boss.wants_abort=True
            visible = False
        SaveBox: save_box:
            pass
        PlotBox: plot_box:
            pass

       
enamldef BossToolBar2(ToolBar):
    dock_area='left'
    Action:
        separator=True
    Action:
        text = "Boss"
        triggered::
            show_boss2(bossarea)
    Action:
        separator=True
    Action:
        text="Log"
        triggered::
            show_log2(bossarea, "yoyoyo")
    Action:
        text = "Plot"
        triggered:: show_pane(dyn_pages, 'Plot')
    Action:
        text=""
    Action:
        separator=True
    Action:
        text = "Instruments"
        triggered:: 
                show_all_instruments2(bossarea, boss)
#                show_instrument2(bossarea, instr)
                print bossarea.dock_items()
                #item=InstrumentItem(bossarea, instr=instr)
                #op = InsertTab(item=item.name, target='')
                #bossarea.update_layout(op)
                print bossarea.dock_items()[0].name

    Action:
        separator=True
    Looper: loopy:
        iterable := boss.instruments
        Action:
            text = loop_item.name
            #tool_tip = text
            triggered:: show_instrument2(bossarea, loop_item)
    Action:
        separator=True
    Action:
        text = "Boot All"
        triggered::boss.boot_all()
    Action:
        text = "Close All"
        triggered::boss.close_all()
    Action:
        separator=True
enamldef BossMain2(MainWindow):# main:
    attr boss
    attr instr
    alias bossarea
    Container:
        alias bossarea        
        BossDockArea: bossarea:
            #DockItem:
                pass #dock_events_enabled=True

        
#    attr path : unicode=u''
#    attr counter = 0
#    initial_size=(500, 500)
#    constraints = [ height == 500]
#    StatusBar: statbar:
#        StatusItem:
#            Label:
#                text = 'Status:'
#        StatusItem:
#            Label:
#                text = 'other stuff really happened:'
#
    BossToolBar2:
        pass
#    alias bosspane: bossp
#    BossPane: bossp:
#        window:=main
#    alias logpane: logp
#    LogPane: logp:
#        pass
#    alias dyn_pages#: dyn_pages
#    Include: dyn_pages:
#        pass

enamldef Main2(Window):
    attr instr
    Container:
        PushButton:
            clicked ::
                print "clicked"
                item=InstrumentItem(bossarea, instr=instr)
                op = InsertItem(item=item.name, target='item_1')
                bossarea.update_layout(op)
        BossDockArea: bossarea:
            pass #dock_events_enabled=True
            #pass #instr=instr

def show_log2(area, log_str):
    dock_items=area.dock_items()
    names=(o.name for o in dock_items)
    if "logger" not in names:
        item=LogItem(area, log_str=log_str)
        op = InsertBorderItem(item="logger", position="bottom")
        area.update_layout(op)

def show_boss2(area):
    dock_items=area.dock_items()
    names=(o.name for o in dock_items)
    if "boss" not in names:
        item=BossItem(area)
        op = InsertBorderItem(item="boss", position="top")
        area.update_layout(op)


#enamldef LogItem(DockItem):
#    #dock_area='bottom'
#    attr log_str
#    name = "logger"
#    title = "Log"
#    Container:
#        padding = 0
#        MultilineField: mlf:
#            text << log_str

enamldef MasterMain(MainWindow):main:
    attr boss
    attr path : unicode=u''
    MasterToolBar:
        pass
    MasterPane:
        window:=main
    alias logpane: logp
    LogPane: logp:
        pass
    alias dyn_pages#: dyn_pages
    Include: dyn_pages:
        pass

enamldef InstrMain(MainWindow): main:
    attr instr
    attr boss
    attr path : unicode=u''
    BossToolBar:
        pass
    alias bosspane: bossp
    BossPane: bossp:
        window:=main
        visible = False
    alias logpane: logp
    LogPane: logp:
        pass
    alias dyn_pages#: dyn_pages
    Include: dyn_pages:
        objects=[InstrumentPane(instr=instr)]

#enamldef PlotPane(DockPane): pp:
#    title = "Plot"
#    closed :: dyn_pages.objects.remove(pp)
#    dock_area='right'

#enamldef InstrumentPane(DockPane): ip:
#    attr instr
#    closed :: dyn_pages.objects.remove(ip)
#    title = instr.name
#    dock_area='right'
#    DynamicTemplate:  #use of dynamic template allows custom instrument layouts if defined in enaml
#        base = InstrTemp
#        args = (instr.view,)
#
#def show_instrument(dyn_pages, loop_item):
#    exists=False
#    for pane in dyn_pages.objects:
#        if pane.title==loop_item.name:
#            pane.show()
#            exists=True
#    if not exists:
#        pane=InstrumentPane(instr=loop_item)
#        dyn_pages.objects.append(pane) #boss.instruments[0].instr_show()
#
#def show_all_instruments(dyn_pages, boss):
#    for instr in boss.instruments:
#        show_instrument(dyn_pages, instr)
#
#def show_all_slaves(dyn_pages, boss):
#    for instr in boss.slaves:
#        show_instrument(dyn_pages, instr)

enamldef SaveBox(GroupBox):
        constraints =[vbox(hbox(base_dir_lbl, base_dir_fld, base_dir),
                                 hbox(main_dir_lbl, main_dir),
                                 hbox(quality_lbl, quality, save, spacer),
                                 hbox(comment_lbl, comment_mlf, spacer))]
        Label: main_dir_lbl:
            text = "Save name:"
        Field: main_dir:
            text := boss.save_file.main_dir

        PushButton: save:
            text = "Save"
            clicked ::
                boss.do_save()
            visible = boss.save_file.buffer_save

        Label: quality_lbl:
            text = "Quality:"
        ObjectCombo: quality:
            items = list(boss.save_file.get_member('quality').items)
            selected := boss.save_file.quality
#        Container: cont:
#            constraints = [vbox(hbox(lbl, pb, spacer), fld), align('v_center', lbl,  pb),]
        Label: base_dir_lbl:
            text = 'Base directory'
        PushButton: base_dir:
                text = 'Browse'
                clicked ::
                    path = FileDialogEx.get_existing_directory(window)
                    if path:
                        boss.save_file.base_dir = path
        Field: base_dir_fld:
                read_only = True
                text << boss.save_file.base_dir
#    Container:
#        padding = 0
        Label: comment_lbl:
            text = 'Comment'
        MultilineField: comment_mlf:
            text := boss.save_file.comment
#        PushButton:
#            pass

enamldef BossPane(DockPane):
    dock_area='left'
    title = "boss"
    Container:
        constraints = [hbox(plot_box, vbox(prepare, run, finish, run_measurement, abort, spacer))]

        PushButton: prepare:
            text = "Prepare"
            clicked :: boss.prepare()
        PushButton: finish:
            text = "Finish"
            clicked :: boss.finish()
        PushButton: run:
            text = "Run"
            clicked ::
                boss.run()
        PushButton: run_measurement:
            text = "Run Measurement"
            clicked ::
                boss.run_measurement()
        PushButton: abort:
            text = "Abort"
            clicked ::
                boss.wants_abort=True
            visible = False
        PlotBox: plot_box:
            pass
enamldef MasterPane(DockPane):
    attr window
    dock_area='top'
    title = "Master"
    Container:
        constraints = [hbox(vbox( run, abort, spacer), save_box)]
        PushButton: run:
            text = "Run"
            clicked ::
                boss.run()
        PushButton: abort:
            text = "Abort"
            clicked ::
                boss.wants_abort=True
            visible = False
  #      SaveBox: save_box:
  #          pass
            
            #template ValView(model, modelType: func):
#    """ This default specialization for function variables."""
#    Container:
#        padding = 0
#        constraints = [hbox(cb, run)]
#        CheckBox: cb:
#            checked := model._value
#        PushButton: run:
#            text = 'Run'
#            clicked :: model.send()
#            #enabled << vr.set_cmd!=None and not vr.instr.busy
#            #visible << (vr.set_cmd!=None or vr.get_cmd!=None) and vr.full_interface
#        PushButton: run:
#            text = var.button_label
#            enabled << not var.instr.busy
#            clicked :: do_it_if_needed(var, 'run')
#            visible << var.run_cmd!=None
#        GroupBox: run_params:
#            padding = 0
#            visible << var.run_params!=[]
#            title = var.label+" run parameters"
#            Looper:
#                iterable << var.run_params
#                DynamicTemplate:
#                        base=VarTemp #text = '{0} {1}'.format(loop_index, loop_item)
#                        args=(getattr(var.instr, loop_item), getattr(var.instr, loop_item).type())
            
            #    Action:
#        text="Log"
#        triggered::
#            logpane.show()
#    Action:
#        text="boss"
#        triggered::
#            #boss.instruments.append(boss.instruments[0])
#            #actionList=[]
#            #for instr in boss.instruments:
#            #    action=InstrAction(instr=instr)
#            #    actionList.append(action)
#            #instrs.objects=actionList
#            print logpane.dock_area
#            print dyn_pages.objects
# #           print dir(mainw)
#    Action:
#        text=""
#    Action:
#        separator=True
#    Action:
#        text = "Instruments"
#        triggered:: show_all_instruments(dyn_pages, boss)
#    Action:
#        text = "Boot All"
#        triggered::boss.boot_all()
#    Action:
#        text = "Close All"
#        triggered::boss.close_all()
#    Action:
#        separator=True
##    Include: instrs:
##        pass
#    Looper: loopy:
#        iterable := boss.instruments
#        Action:
#            text = loop_item.label
#            #tool_tip = text
#            triggered:: show_instrument(dyn_pages, loop_item)

enamldef PlotPane(DockPane):pp:
    #attr plotr
    closed :: dyn_pages.objects.remove(pp)
    dock_area='right'
    Container:
        PlotToolBar:
            pass
        padding = 0
        EnableCanvas: ecanvas:
            constraints=[height==400, width==600]
            component << plotr.plot
            
            enamldef MatPlotPane(DockPane):mp:
    #attr plotr
    closed :: dyn_pages.objects.remove(mp)
    dock_area='right'
    Container:
        #constraints=[height==600, width==800]
        PlotToolBar:
            pass
        ObjectCombo: cbox:
            items = ['one', 'two']
        padding = 0
        MPLCanvas: canvas:
            #constraints=[height==600, width==800]
            figure << plotr.figures[cbox.selected]
            toolbar_visible=True
def show_pane(dyn_pages, title):
    exists=False
    for pane in dyn_pages.objects:
        if pane.title==title:
            pane.show()
            exists=True
    if not exists:
        if title=='XY Format':
            pane=XYfPane()
        elif title=="Plot Format":
            pane=PlotfPane()
        elif title=="Plot":
            pane=PlotPane()
        dyn_pages.objects.append(pane)