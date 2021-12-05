import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Wifi qr codes!")
        encryption_store = Gtk.ListStore(int, str)
        encryption_store.append([1, 'WPA/WPA2'])
        encryption_store.append([2, 'WEP'])
        encryption_store.append([3, 'No Password'])

        grid = Gtk.Grid()
        grid.set_column_spacing(5)
        grid.set_row_spacing(5)
        self.add(grid)

        label1 = Gtk.Label()
        label1.set_text("SSID (Network Name)")
        label1.set_width_chars(15)
        grid.attach(label1, 0, 0, 1, 1)

        self.ssid_entry = Gtk.Entry()
        grid.attach(self.ssid_entry, 1, 0, 1, 1)

        self.passwordEntry = Gtk.Entry()
        grid.attach(self.passwordEntry, 1, 2, 1, 1)

        label3 = Gtk.Label()
        label3.set_text("Password")
        label3.set_width_chars(15)
        grid.attach(label3, 0, 2, 1, 1)

        self.encryption_combo = Gtk.ComboBox.new_with_model(encryption_store)
        renderer_text = Gtk.CellRendererText()
        self.encryption_combo.pack_start(renderer_text, True)
        self.encryption_combo.add_attribute(renderer_text, "text", 1)
        self.encryption_combo.connect("changed", self.on_encryption_changed)
        self.encryption_combo.set_active(0)
        grid.attach(self.encryption_combo, 1, 1, 1, 1)

        label2 = Gtk.Label()
        label2.set_text("Encryption")
        label2.set_width_chars(15)
        grid.attach(label2, 0, 1, 1, 1)

        self.hidden_cbtn = Gtk.CheckButton()
        self.hidden_cbtn.set_label("Hidden")
        grid.attach(self.hidden_cbtn, 1, 3, 1, 1)

        self.set_border_width(5)

    def on_encryption_changed(self, combo):
        tree_iter = combo.get_active_iter()
        encrId = None
        if tree_iter is not None:
            model = combo.get_model()
            encrId = model[tree_iter][0]

        if encrId == 3:
            self.passwordEntry.set_text("")
            self.passwordEntry.set_editable(False)
        else:
            self.passwordEntry.set_editable(True)


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()
