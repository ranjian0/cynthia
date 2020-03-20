import bmesh
from bmesh.types import BMEdge
from ...utils import (
    add_facemap_for_groups,
    sort_verts,
    filter_geom,
    map_new_faces,
    FaceMap,
    local_xyz,
    arc_edge,
)


def fill_arch(bm, face, prop):
    """ Fill arch
    """
    if prop.fill_type == "GLASS_PANES":
        add_facemap_for_groups(FaceMap.DOOR_PANES)
        pane_arch_face(bm, face, prop.glass_fill)


def create_arch(bm, face, top_edges, frame_faces, arch_prop, frame_thickness):
    """ Create arch using top edges of extreme frames
    """
    verts = sort_verts([v for e in top_edges for v in e.verts], local_xyz(face)[1])
    arc_edges = [
        bmesh.ops.connect_verts(bm, verts=[verts[0],verts[3]])['edges'].pop(),
        bmesh.ops.connect_verts(bm, verts=[verts[1],verts[2]])['edges'].pop(),
    ]

    upper_arc = filter_geom(arc_edge(bm, arc_edges[0], arch_prop.resolution, arch_prop.height, arch_prop.offset, arch_prop.function)["geom_split"], BMEdge)
    lower_arc = filter_geom(arc_edge(bm, arc_edges[1], arch_prop.resolution, arch_prop.height-frame_thickness, arch_prop.offset, arch_prop.function)["geom_split"], BMEdge)
    arc_edges = [
        *upper_arc,
        *lower_arc,
    ]

    arch_frame_faces = bmesh.ops.bridge_loops(bm, edges=arc_edges)["faces"]
    arch_face = min(lower_arc[arch_prop.resolution//2].link_faces, key=lambda f: f.calc_center_median().z)
    return arch_face, arch_frame_faces


@map_new_faces(FaceMap.DOOR_PANES)
def pane_arch_face(bm, face, prop):
    bmesh.ops.inset_individual(
        bm, faces=[face], thickness=prop.pane_margin * 0.75, use_even_offset=True
    )
    bmesh.ops.translate(
        bm, verts=face.verts, vec=-face.normal * prop.pane_depth
    )


def arch_add_depth(bm, arch_face, depth, normal):
    """ Add depth to arch face
    """
    if depth != 0:
        arch_face = bmesh.ops.extrude_discrete_faces(bm, faces=[arch_face]).get("faces").pop()
        verts = [v for v in arch_face.verts]
        bmesh.ops.translate(bm, verts=verts, vec=-normal * depth)
        return arch_face
