# coding: latin-1
"""
@file

@brief  defines @see cl FrameParams
"""
import sys, os, tkinter

from .function_helper       import private_adjust_parameters
from .storing_functions     import _private_restore, _private_store, interpret_parameter


class FrameParams (tkinter.Frame) :
    """
    creating a Frame window for a list of parameters
    """
    
    def __init__ (self, parent, 
                        restore         = True, 
                        width           = 100, 
                        raise_exception = False, 
                        params          = {},
                        help            = "",
                        key_save        = "",
                        command_leave   = None) :
        """
        constructor
        @param      parent          window parent
        @param      restore         if True, check if existing saved parameters are present
        @param      width           number of characters in every Entry field
        @param      raise_exception raise an exception instead of catching it
        @param      params          parameters to overwrite
        @param      help            help to display
        @param      key_save        to make unique the file storing and restoring the parameters
        @param      command_leave   if not None, this function will be called when clicking on Cancel or Leave
        """
        tkinter.Frame.__init__ (self, parent)
        self.fdoc       = tkinter.Frame (self)
        self.fpar       = tkinter.Frame (self)
        self.fbut       = tkinter.Frame (self)
        self.fpar.pack ()
        self.fbut.pack ()
        self.fdoc.pack ()
        self.restore    = restore
        self.parent     = parent
        self.input      = { }
        self.types      = {}
        self.raise_exception = raise_exception
        self._added     = { }
        self.key_save   = key_save
        self.command_leave = command_leave
        
        # retieve previous answers
        self._history  = [ ]
        self._hpos     = -1

        self.info       = { "name":"FrameParams", "param":params, "help":help, "key_save":key_save }
        
        if restore : 
            self._history = _private_restore (".".join( [ self.info ["name"], self.info ["key_save"] ] ))
            if len(self._history) > 0 :
                self.info ["param"].update (self._history[-1])
                self._hpos = len(self._history)-1
            
        for k in self.info ["param"]:
            self.types [k] = self.info ["param"][k].__class__
            if self.types [k] in [None, None.__class__] : 
                self.types [k] = str
        
        # documentatin 
        tlab = tkinter.Label(self.fdoc, text = "Help")
        tlab.pack (side = tkinter.LEFT)
        lab = tkinter.Text (self.fdoc, width = width, height = 7)
        lab.pack (side=tkinter.LEFT)
        lab.insert ("0.0", self.info ["help"])
        
        scroll=tkinter.Scrollbar(self.fdoc)
        scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        scroll.config(command=lab.yview, width=5)
        lab.config(yscrollcommand = scroll.set)        
                
        self.fdoc.bind('<Return>', self.run_function)
        self.fdoc.bind('<Escape>', self.run_cancel)
        
        # next
        line = 0
        for k in sorted (self.info ["param"]) :
            if k in self._added : continue
            lab = tkinter.Label (self.fpar, text = k)
            lab.grid (row = line, column = 0)
            
            if k == "password" :
                lab = tkinter.Entry (self.fpar, width = width, show = "*")
            else :
                lab = tkinter.Entry (self.fpar, width = width)
            
            lab.grid (row = line, column = 1)
            if self.info ["param"][k] != None :
                lab.insert ("0", str (self.info ["param"][k]))
            self.input [k] = lab
            lab.bind('<Return>', self.run_function)
            lab.bind('<Escape>', self.run_cancel)
            line += 1

        # optional
        for k in sorted (self.info ["param"]) :
            if k not in self._added : continue
            lab = tkinter.Label (self.fpar, text = k)
            lab.grid (row = line, column = 0)
            
            if k == "password" :
                lab = tkinter.Entry (self.fpar, width = width, show = "*")
            else :
                lab = tkinter.Entry (self.fpar, width = width)
            
            lab.grid (row = line, column = 1)
            if self.info ["param"][k] != None :
                lab.insert ("0", str (self.info ["param"][k]))
            lab.bind('<Return>', self.run_function)
            lab.bind('<Escape>', self.run_cancel)
            self.input [k] = lab

            line += 1

        # next: button
        self.cancel = tkinter.Button (self.fbut, text = "cancel or leave")
        self.run    = tkinter.Button (self.fbut, text = "     ok       ")
        self.cancel.pack (side = tkinter.LEFT)
        self.run.pack (side = tkinter.LEFT)
        self.run.bind('<Return>', self.run_function)
        self.run.bind('<Escape>', self.run_cancel)
        
        self.cancel.config (command = self.run_cancel)
        self.run.config (command = self.run_function)
        private_adjust_parameters (self.info ["param"])
        self._already = False
        
        # up, down
        self.bup   = tkinter.Button (self.fbut, text = "up")
        self.bdown = tkinter.Button (self.fbut, text = "down")
        self.bup.pack (side = tkinter.LEFT)
        self.bdown.pack (side = tkinter.LEFT)
        self.bup.config (command = self.history_up)
        self.bdown.config (command = self.history_down)
        
    def update (self):
        """
        update the parameters (ie ``self.info``)
        """
        for k in self.input :
            self.input[k].delete(0, tkinter.END)
            self.input[k].insert ("0", str (self.info ["param"].get(k,"")))
        
    def history_up(self, *args) :
        """
        look back in the history (log of used parameters)
        and update the parameters
        """
        if len(self._history) > 0 :
            self._hpos = (self._hpos+1) % len(self._history)
            self.info ["param"].update (self._history[self._hpos])
            self.update()
        
    def history_down(self, *args):
        """
        look forward in the history (log of used parameters)
        and update the parameters
        """
        if len(self._history) > 0 :
            self._hpos = (self._hpos+len(self._history)-1) % len(self._history)
            self.info ["param"].update (self._history[self._hpos])
            self.update()
        
    def run_cancel(self, *args) :
        """
        what to do when Cancel is pressed
        """
        self.info["param"]["__cancel__"] = True
        if self.command_leave != None :
            self.command_leave()
        else :
            self.parent.destroy()
        
    def get_parameters (self) :
        """
        returns the parameters
        
        @return     dictionary
        """
        res = { }
        for k,v in self.input.items () :
            s = v.get ()
            s = s.strip ()
            if len (s) == 0 : s = None
            ty = self.types [k]
            res[k] = interpret_parameter(ty, s)
        return res
        
    def get_title (self) :
        """
        return the title
        
        @return self.info ["name"]
        """
        return self.info ["name"]
        
    def refresh (self) :
        """
        refresh the screen
        """
        if self._already :
            self.after (1000, self.refresh)
        else :
            self.run.config (state = tkinter.NORMAL)
            if True :
                self.parent.destroy ()
        
    def run_function (self, *args) :
        """
        run the function
        """
        if True :  self.parent.withdraw ()
        else :     self.run.config (state = tkinter.DISABLED)
        self._already = True
        
        res = self.get_parameters ()
        if self.restore :
            _private_store (".".join( [ self.info ["name"], self.info ["key_save"] ] ) , res)
            
        self.info["param"].update(res)
        self.parent.destroy()
        
    @staticmethod
    def open_window (   params,
                        help_string       = "",
                        title             = "",
                        top_level_window  = None,
                        key_save          = "") :
        """
        Open a tkinter window to set up parameters. 
        It adds entries for the parameters,
        it displays the help given to this function.
        It also memorizes the latest values used (stored in ``<user>/TEMP folder``).
        
        @param      help_string             help to de displayed
        @param      top_level_window        if you want this window to depend on a top level window from tkinter
        @param      params                  if not None, overwrite values for some parameters,
                                                it will be updated by the function (= returned value)
        @param      key_save                parameters are saved and restore from a file, key_save will make this file unique
        @param      title                   title of the window
        @return                             new parameters
        
        @warning If the string "__cancel__" is present in the results, it means the users clicked on cancel.
        
        The window looks like:
        @image html http://www.xavierdupre.fr/app/screenshots/open_window_params.png
        
        Example:
        @code
        params =  {"velib_key": "", "contract":"Paris"}
        newparams = FrameParams.open_window (params, "fetch data from Velib website")
        @endcode
        """
        param   = params if params != None else {  }

        root = top_level_window if top_level_window != None else tkinter.Tk ()
        ico  = os.path.realpath (os.path.join (os.path.split (__file__) [0], "project_ico.ico"))
        fr   =  FrameParams ( root, params = param, help = help_string, key_save = key_save)
        fr.pack ()
        root.title (title)
        if ico != None and top_level_window == None and sys.platform.startswith("win") : 
            root.wm_iconbitmap(ico)
        fr.mainloop ()
        return param
        
def open_window_params (  params,
                          help_string       = "",
                          title             = "",
                          top_level_window  = None,
                          key_save          = "") :
    """
    Open a tkinter window to set up parameters. 
    It adds entries for the parameters,
    it displays the help given to this function.
    It also memorizes the latest values used (stored in <user>/TEMP folder).
    
    @param      help_string             help to de displayed
    @param      top_level_window        if you want this window to depend on a top level window from tkinter
    @param      params                  if not None, overwrite values for some parameters,
                                            it will be updated by the function (= returned value)
    @param      key_save                parameters are saved and restore from a file, key_save will make this file unique
    @param      title                   title of the window
    @return                             new parameters
    
    @warning If the string "__cancel__" is present in the results, it means the users clicked on cancel.
    
    The window looks like:
    @image html http://www.xavierdupre.fr/app/screenshots/open_window_params.png
    
    @example(open a tkinter window to ask parameters to a user)
    @code
    params = { "user":os.environ["USERNAME"],
               "password":"" }
    newparams = open_window_params (params, "try the password *", help_string = "unit test")
    @endcode
    
    The program opens a window like the following one:
    
    @image images/open_params.png
    
    @endexample
    
    Password are not stored in a text file. You must type them again next time.
    """
    return FrameParams.open_window (params = params,
                                help_string = help_string,
                                title = title,
                                top_level_window = top_level_window,
                                key_save = key_save)