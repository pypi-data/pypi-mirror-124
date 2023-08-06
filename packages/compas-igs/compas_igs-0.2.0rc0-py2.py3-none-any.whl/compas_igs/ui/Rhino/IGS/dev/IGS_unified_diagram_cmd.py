from __future__ import print_function
from __future__ import absolute_import
from __future__ import division

import compas

from compas.geometry import centroid_points
from compas.geometry import subtract_vectors
from compas.geometry import scale_vector

import scriptcontext as sc

import compas_rhino

from compas_igs.rhino import mesh_ud

try:
    import Rhino
    import rhinoscriptsyntax as rs
except ImportError:
    compas.raise_if_ironpython()


__commandname__ = "IGS_unified_diagram"


def RunCommand(is_interactive):

    if 'IGS' not in sc.sticky:
        compas_rhino.display_message('IGS has not been initialised yet.')
        return

    scene = sc.sticky['IGS']['scene']

    objects = scene.find_by_name('Form')
    if not objects:
        compas_rhino.display_message("There is no FormDiagram in the scene.")
        return
    form = objects[0]

    objects = scene.find_by_name('Force')
    if not objects:
        compas_rhino.display_message("There is no ForceDiagram in the scene.")
        return
    force = objects[0]

    # translation
    form_center = centroid_points(form.vertex_xyz.values())
    force_center = centroid_points(force.vertex_xyz.values())

    translation = subtract_vectors(force_center, form_center)

    # get scale
    go = Rhino.Input.Custom.GetOption()
    go.SetCommandPrompt("Unified diagram options (press ESC to exit)")
    go.AcceptNothing(True)

    scale_opt = Rhino.Input.Custom.OptionDouble(0.5, 0.01, 1.00)

    go.AddOptionDouble("Alpha", scale_opt)

    # get scale and rotation
    def _draw_ud(form, force, translation=translation, scale=0.5):
        compas_rhino.clear_layer(force.layer)

        # 2. compute unified diagram geometries
        geometry = mesh_ud(form, force, translation=translation, scale=scale)

        if not geometry:
            return

        faces, bars = geometry

        # 3. draw
        for face, face_xyz in faces.items():
            compas_rhino.draw_mesh(face_xyz, [range(len(face_xyz))], layer=force.layer, name=str(face), redraw=False)

        bar_colors = {}
        for edge in force.diagram.edges_where_dual({'is_external': False}):
            if force.diagram.dual_edge_force(edge) > + force.settings['tol.forces']:
                bar_colors[edge] = force.settings['color.tension']
            elif force.diagram.dual_edge_force(edge) < - force.settings['tol.forces']:
                bar_colors[edge] = force.settings['color.compression']

        for bar, bar_xyz in bars.items():
            compas_rhino.draw_mesh(bar_xyz, [range(len(bar_xyz))], layer=force.layer, name=str(bar), color=bar_colors[bar], redraw=False)

    # unified diagram
    while True:

        rs.EnableRedraw(True)
        opt = go.Get()

        scale = scale_opt.CurrentValue

        if opt == Rhino.Input.GetResult.Cancel:  # esc
            keep = rs.GetBoolean("Keep unified diagram? (press ESC to exit)", [("Copy", "No", "Yes")], (False))
            scene.clear_layers()
            if keep and keep[0]:
                _draw_ud(form, force, translation=scale_vector(translation, 2.5), scale=scale)
            scene.update()
            scene.save()
            return

        _draw_ud(form, force, translation=translation, scale=scale)


# ==============================================================================
# Main
# ==============================================================================


if __name__ == '__main__':

    RunCommand(True)
