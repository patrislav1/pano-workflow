#!/usr/bin/env python3

import sys

import gi
gi.require_version('Gimp', '3.0')
gi.require_version("Gegl", "0.4")
from gi.repository import Gimp
gi.require_version('GimpUi', '3.0')
from gi.repository import GimpUi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from gi.repository import GLib, Gegl

import json

class ZenitNadirPatchHelper(Gimp.PlugIn):
    PARASITE_NAME = "zenith-nadir-settings"

    def load_state(self, image):
        """Load state from the parasite attached to the image."""
        parasite = image.get_parasite(self.PARASITE_NAME)
        if parasite is not None:
            state = json.loads(bytes(parasite.get_data()).decode('utf-8'))
        else:
            # Default values
            state = {
                "zenith_zoom": 100,
                "zenith_mask": 30,
                "nadir_zoom": 70,
                "nadir_mask": 50
            }
        return state

    def save_state(self, image, state):
        """Save state to the parasite attached to the image."""
        # 1 for PERSISTENT (see https://gitlab.gnome.org/GNOME/gimp/-/blob/master/libgimpbase/gimpparasite.h)
        # (where is that constant in Python?)
        parasite = Gimp.Parasite.new(self.PARASITE_NAME, 1, json.dumps(state).encode('utf-8'))
        image.attach_parasite(parasite)

    def run_gui(self, image):
        GimpUi.init("zenith-nadir-plugin")
        
        state = self.load_state(image)

        dialog = GimpUi.Dialog(title="Zenith and Nadir Settings", use_header_bar=True)
        dialog.add_button("_Cancel", Gtk.ResponseType.CANCEL)
        dialog.add_button("_OK", Gtk.ResponseType.OK)
        
        content_area = dialog.get_content_area()

        # Create a grid to organize the widgets
        grid = Gtk.Grid()
        grid.set_column_spacing(10)
        grid.set_row_spacing(10)
        content_area.add(grid)

        # Zenith Zoom
        zenith_zoom_label = Gtk.Label(label="Zenith Zoom (%)")
        zenith_zoom_entry = Gtk.SpinButton()
        zenith_zoom_entry.set_digits(2)
        zenith_zoom_entry.set_increments(1, 10)
        zenith_zoom_entry.set_range(0, 500)
        zenith_zoom_entry.set_value(state["zenith_zoom"])

        # Zenith Mask Radius
        zenith_mask_label = Gtk.Label(label="Zenith Mask Radius (%)")
        zenith_mask_entry = Gtk.SpinButton()
        zenith_mask_entry.set_digits(2)
        zenith_mask_entry.set_increments(1, 10)
        zenith_mask_entry.set_range(0, 100)
        zenith_mask_entry.set_value(state["zenith_mask"])

        # Nadir Zoom
        nadir_zoom_label = Gtk.Label(label="Nadir Zoom (%)")
        nadir_zoom_entry = Gtk.SpinButton()
        nadir_zoom_entry.set_digits(2)
        nadir_zoom_entry.set_increments(1, 10)
        nadir_zoom_entry.set_range(0, 500)
        nadir_zoom_entry.set_value(state["nadir_zoom"])

        # Nadir Mask Radius
        nadir_mask_label = Gtk.Label(label="Nadir Mask Radius (%)")
        nadir_mask_entry = Gtk.SpinButton()
        nadir_mask_entry.set_digits(2)
        nadir_mask_entry.set_increments(1, 10)
        nadir_mask_entry.set_range(0, 100)
        nadir_mask_entry.set_value(state["nadir_mask"])

        # Add widgets to the grid
        grid.attach(zenith_zoom_label, 0, 0, 1, 1)
        grid.attach(zenith_zoom_entry, 1, 0, 1, 1)
        grid.attach(zenith_mask_label, 0, 1, 1, 1)
        grid.attach(zenith_mask_entry, 1, 1, 1, 1)
        grid.attach(nadir_zoom_label, 0, 2, 1, 1)
        grid.attach(nadir_zoom_entry, 1, 2, 1, 1)
        grid.attach(nadir_mask_label, 0, 3, 1, 1)
        grid.attach(nadir_mask_entry, 1, 3, 1, 1)

        grid.show_all()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            state["zenith_zoom"] = zenith_zoom_entry.get_value()
            state["zenith_mask"] = zenith_mask_entry.get_value()
            state["nadir_zoom"] = nadir_zoom_entry.get_value()
            state["nadir_mask"] = nadir_mask_entry.get_value()

            self.save_state(image, state)
            dialog.destroy()
            return True
        else:
            dialog.destroy()
            return False

    def do_query_procedures(self):
        return ["ph-zenit-nadir-extract", "ph-zenit-nadir-reinsert"]

    def do_set_i18n (self, name):
        return False

    def do_create_procedure(self, name):
        def proc_helper(name, menu_str, doc_str, fn):
            procedure = Gimp.ImageProcedure.new(self, name,
                                                Gimp.PDBProcType.PLUGIN,
                                                fn, None)
            procedure.set_image_types("*")
            procedure.set_menu_label(menu_str)
            procedure.add_menu_path("<Image>/Filters/Panorama/")
            procedure.set_attribution("Patrick Huesmann", "Patrick Huesmann", "2024")
            procedure.set_documentation(doc_str, "", name)
            return procedure

        if name == "ph-zenit-nadir-extract":
            return proc_helper(
                name,
                "Extract Zenit and Nadir",
                "Extract Zenit and Nadir for patching",
                self.extract_zenit_nadir
            )
        elif name == "ph-zenit-nadir-reinsert":
            return proc_helper(
                name,
                "Reinsert Zenit and Nadir",
                "Reinsert Zenit and Nadir after patching",
                self.reinsert_zenit_nadir
            )
        else:
            return None

    def gegl_op(self, graph, inbuf, outbuf, node):
        input = graph.create_child("gegl:buffer-source")
        input.set_property("buffer", inbuf)
        output = graph.create_child("gegl:write-buffer")
        output.set_property("buffer", outbuf)
        input.link(node)
        node.link(output)
        output.process()

    def error_helper(self, procedure, msg):
        error = GLib.Error.new_literal(Gimp.PlugIn.error_quark(), msg, 0)
        return procedure.new_return_values(Gimp.PDBStatusType.CALLING_ERROR, error)

    def extract_zenit_nadir(self, procedure, run_mode, image, n_drawables, drawables, config, run_data):
        if not self.run_gui(image):
            return self.error_helper(procedure, "Aborted")

        if n_drawables != 1:
            msg = f"Procedure '{procedure.get_name()}' only works with one drawable."
            return self.error_helper(procedure, msg)
        else:
            drawable = drawables[0]
#
        state = self.load_state(image)

        Gegl.init(None)
        graph = Gegl.Node()
        
        src_buf = drawable.get_buffer()

        # Transformation for nadir extraction
        nadir = drawable.copy()
        nadir_buf = nadir.get_buffer()

        pan_map = graph.create_child("gegl:panorama-projection")
        pan_map.set_property("tilt", 90.0)
        pan_map.set_property("zoom", state["nadir_zoom"])
        self.gegl_op(graph, src_buf, nadir_buf, pan_map)

        nadir_buf.flush()
        nadir.set_name("Nadir")
        image.insert_layer(nadir, None, 0)

        # Transformation for zenit extraction
        zenit = drawable.copy()
        zenit_buf = zenit.get_buffer()

        pan_map = graph.create_child("gegl:panorama-projection")
        pan_map.set_property("tilt", -90.0)
        pan_map.set_property("zoom", state["zenith_zoom"])
        self.gegl_op(graph, src_buf, zenit_buf, pan_map)

        zenit_buf.flush()
        zenit.set_name("Zenit")
        image.insert_layer(zenit, None, 0)
  
        Gimp.displays_flush()
        return

    def reinsert_zenit_nadir(self, procedure, run_mode, image, n_drawables, drawables, config, run_data):

        zenit = [l for l in image.list_layers() if l.get_name() == "Zenit"]
        nadir = [l for l in image.list_layers() if l.get_name() == "Nadir"]

        if len(zenit) != 1:
            return self.error_helper(procedure, f"expected 1 zenit layer, found {len(zenit)}")
        if len(nadir) != 1:
            return self.error_helper(procedure, f"expected 1 nadir layer, found {len(zenit)}")

        zenit = zenit[0]
        nadir = nadir[0]

        state = self.load_state(image)
        
        Gegl.init(None)
        graph = Gegl.Node()
        
        z_buf = zenit.get_buffer()
        s_buf = zenit.get_shadow_buffer()
        pan_map = graph.create_child("gegl:panorama-projection")
        pan_map.set_property("tilt", -90.0)
        pan_map.set_property("zoom", state["zenith_zoom"])
        pan_map.set_property("inverse", True)
        self.gegl_op(graph, z_buf, s_buf, pan_map)
        s_buf.flush()
        zenit.merge_shadow(True)
        zenit.update(0, 0, zenit.get_width(), zenit.get_height())
  
        n_buf = nadir.get_buffer()
        s_buf = nadir.get_shadow_buffer()
        pan_map = graph.create_child("gegl:panorama-projection")
        pan_map.set_property("tilt", 90.0)
        pan_map.set_property("zoom", state["nadir_zoom"])
        pan_map.set_property("inverse", True)
        self.gegl_op(graph, n_buf, s_buf, pan_map)
        s_buf.flush()
        nadir.merge_shadow(True)
        nadir.update(0, 0, nadir.get_width(), nadir.get_height())
  
        Gimp.displays_flush()
        return

Gimp.main(ZenitNadirPatchHelper.__gtype__, sys.argv)
