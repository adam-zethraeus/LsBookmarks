import sublime, sublime_plugin
import os, re

class ViewBookmarksCommand(sublime_plugin.WindowCommand):
    locations=[]

    def run(self):
        items=[]
        self.locations=[]
        all_files = list(filter(None, map(lambda f : f.file_name(), sublime.active_window().views())))
        common_prefix = os.path.commonprefix(all_files)
        for view in sublime.active_window().views():
            prefix=""
            if view.name():
                prefix=view.name()+":"
            elif view.file_name():
                prefix=view.file_name()+":"
                if prefix.startswith(common_prefix):
                    prefix = prefix[len(common_prefix):]
            for region in view.get_regions("bookmarks"):
                row,_=view.rowcol(region.a)
                line=re.sub('\s+', ' ', view.substr(view.line(region))).strip()
                items.append([prefix+str(row+1), line])
                self.locations.append((view, region))
        if len(items) > 0:
            self.orig_view = sublime.active_window().active_view()
            self.orig_sel = self.orig_view.sel()
            sublime.active_window().show_quick_panel(items, self.go_there, sublime.MONOSPACE_FONT, on_highlight=self.peek_there)
        else:
            sublime.active_window().show_quick_panel(["No bookmarks found"], None, sublime.MONOSPACE_FONT)

    def go_there(self, i):
        if i >= len(self.locations):
            return
        elif i < 0:
            sublime.active_window().focus_view(self.orig_view)
            self.orig_view.show(self.orig_sel)
        else:
            view, region = self.locations[i]
            sublime.active_window().focus_view(view)
            view.show_at_center(region)
            view.sel().clear()
            view.sel().add(region)

    def peek_there(self, i):
        view, region = self.locations[i]
        sublime.active_window().focus_view(view)
        view.show_at_center(region)
