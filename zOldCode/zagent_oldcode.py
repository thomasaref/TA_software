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
