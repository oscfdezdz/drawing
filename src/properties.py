# properties.py
#
# Copyright 2018 Romain F. T.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from gi.repository import Gtk, Gdk, Gio, GdkPixbuf
import cairo

class DrawingPropertiesDialog(Gtk.Dialog):
	__gtype_name__ = 'DrawingPropertiesDialog'

	def __init__(self, window):
		wants_csd = not ( 'ssd' in window._settings.get_string('decorations') )
		super().__init__(use_header_bar=wants_csd, destroy_with_parent=True, transient_for=window, title=_("Image properties"))
		self._window = window

		builder = Gtk.Builder.new_from_resource('/com/github/maoschanz/Drawing/ui/properties_dialog.ui')
		props_content_area = builder.get_object('props_content_area')
		self.get_content_area().add(props_content_area)

		label_path = builder.get_object('label_path')
		label_format_file = builder.get_object('label_format_file')
		label_format_surface = builder.get_object('label_format_surface')
		self.label_width = builder.get_object('label_width')
		self.label_height = builder.get_object('label_height')

		if window._pixbuf_manager.gfile is not None:
			label_path.set_label(window.get_file_path())
			(pb_format, width, height) = GdkPixbuf.Pixbuf.get_file_info(window.get_file_path())
			label_format_file.set_label(pb_format.get_name())

		enum = {
			0: 'ARGB32',
			1: 'RGB24',
			2: 'A8',
			3: 'A1',
			4: 'RGB16_565',
			5: 'RGB30',
		}
		label_format_surface.set_label(enum.get(window.get_surface().get_format(), _("Invalid format")))
		self.set_size_labels()

		btn_crop = builder.get_object('btn_crop')
		btn_crop.connect('clicked', self.on_crop)

		btn_scale = builder.get_object('btn_scale')
		btn_scale.connect('clicked', self.on_scale)

		btn_scale = builder.get_object('btn_rotate')
		btn_scale.connect('clicked', self.on_rotate)

		self.set_default_size(400, 100)
		self.show_all()

	def on_rotate(self, *args):
		self._window.action_rotate()
		self.set_size_labels()

	def on_scale(self, *args):
		self._window.action_scale()
		self.set_size_labels()

	def on_crop(self, *args):
		self._window.action_crop()
		self.set_size_labels()

	def set_size_labels(self):
		self.label_width.set_label(str(self._window.get_pixbuf_width()) + ' px')
		self.label_height.set_label(str(self._window.get_pixbuf_height()) + ' px')

