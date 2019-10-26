import bpy

bl_info = {
    "name": "node-group-replacer",
    "description": "Simple addon to mass replace node groups",
    "author": "Lateasusual",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "Node Editor",
    "category": "Nodes"
}


class NODE_PT_NodeGroupReplacePanel(bpy.types.Panel):
    """ Panel for replacing node groups """
    bl_label = "Node Group Replace"
    bl_idname = "NODE_PT_Node_Group_Replace_Panel"

    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_category = "Misc"

    def draw(self, context):
        layout = self.layout
        layout.prop_search(context.scene, "node_tree_old", bpy.data, "node_groups")
        layout.prop_search(context.scene, "node_tree_new", bpy.data, "node_groups")
        op = layout.operator("nodes.replace_tree")
        op.old_tree = context.scene.node_tree_old
        op.new_tree = context.scene.node_tree_new


class NODE_OT_ReplaceNodeTree(bpy.types.Operator):
    """ Replaces all instances of a target shader node tree """
    bl_idname = "nodes.replace_tree"
    bl_label = "Replace Node Group"
    bl_options = {'REGISTER', 'UNDO'}

    old_tree: bpy.props.StringProperty("old group")
    new_tree: bpy.props.StringProperty("new group")

    @classmethod
    def poll(cls, context):
        return context is not None

    def execute(self, context):
        for mat in bpy.data.materials:
            for node in mat.node_tree.nodes:
                if node.type == 'GROUP':
                    if node.node_tree.name == self.old_tree:
                        node.node_tree = bpy.data.node_groups[self.new_tree]
        return {'FINISHED'}


classes = {
    NODE_PT_NodeGroupReplacePanel,
    NODE_OT_ReplaceNodeTree
}


def register():
    for c in classes:
        bpy.utils.register_class(c)
    bpy.types.Scene.node_tree_old = bpy.props.StringProperty(name="Old group", default="", options={'SKIP_SAVE'})
    bpy.types.Scene.node_tree_new = bpy.props.StringProperty(name="New group", default="", options={'SKIP_SAVE'})


def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
    del bpy.types.Scene.node_tree_old
    del bpy.types.Scene.node_tree_new


if __name__ == '__main__':
    register()