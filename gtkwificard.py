import gi
import os
import shutil

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class MainWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Wifi qr codes!")
        self.set_resizable(False)
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

        button = Gtk.Button.new_with_label("Generate")
        button.connect("clicked", self.make_qr_code)
        grid.attach(button, 0, 4, 2, 1)

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

    def make_qr_code(self, but):
        dialog = Gtk.FileChooserDialog(
            title="Choose a location to save the card to.",
            parent=self,
            action=Gtk.FileChooserAction.SAVE,
        )
        dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK)
        dialog.set_default_size(800, 400)

        response = dialog.run()
        finalFile = None
        if (response == Gtk.ResponseType.OK):
            finalFile = dialog.get_filename()
        else:
            dialog.destroy()
            return;

        dialog.destroy()


        SSID=self.ssid_entry.get_text()
        tree_iter = self.encryption_combo.get_active_iter()
        encrId = self.encryption_combo.get_model()[tree_iter][0]
        hidden = "y" if self.hidden_cbtn.get_active() else "N"
        password = self.passwordEntry.get_text()

        if os.path.isdir('/tmp/gtkwificard'):
            shutil.rmtree('/tmp/gtkwificard')

        os.makedirs('/tmp/gtkwificard')
        current_path = os.path.realpath(__file__)
        dir_path = os.path.dirname(current_path)
        shutil.copyfile(dir_path + '/qr-code/wifiqr', '/tmp/gtkwificard/wifiqr')
        shutil.copyfile(dir_path + '/card/wificard', '/tmp/gtkwificard/wificard')
        os.chdir('/tmp/gtkwificard')

        # It necessarily needs to be bash, because we are sourcing
        # inside of a shell script, which is not POSIX compliant
        os.system('echo "' + SSID + '\n' + hidden + '\n' + str(encrId) + '\n' + password + '" | bash wificard output.png')

        shutil.copyfile('/tmp/gtkwificard/output.png', finalFile)

        message = Gtk.MessageDialog(self, 0, Gtk.MessageType.INFO, Gtk.ButtonsType.CLOSE, "Success!")
        message.run()
        message.destroy()
        self.destroy()


win = MainWindow()
win.connect("destroy", Gtk.main_quit)
win.show_all()
Gtk.main()

if os.path.isdir('/tmp/gtkwificard'):
    shutil.rmtree('/tmp/gtkwificard')
