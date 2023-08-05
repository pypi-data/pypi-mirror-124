import os

import pybullet as p

import igibson
from igibson.objects.stateful_object import StatefulObject


class YCBObject(StatefulObject):
    """
    YCB Object from assets/models/ycb
    Reference: https://www.ycbbenchmarks.com/
    """

    def __init__(self, name, scale=1):
        super(YCBObject, self).__init__()
        self.visual_filename = os.path.join(igibson.assets_path, "models", "ycb", name, "textured_simple.obj")
        self.collision_filename = os.path.join(igibson.assets_path, "models", "ycb", name, "textured_simple_vhacd.obj")
        self.scale = scale

    def _load(self):
        collision_id = p.createCollisionShape(p.GEOM_MESH, fileName=self.collision_filename, meshScale=self.scale)
        visual_id = p.createVisualShape(p.GEOM_MESH, fileName=self.visual_filename, meshScale=self.scale)

        body_id = p.createMultiBody(
            baseCollisionShapeIndex=collision_id,
            baseVisualShapeIndex=visual_id,
            basePosition=[0.2, 0.2, 1.5],
            baseMass=0.1,
        )
        self.body_id = body_id
        return body_id

    def get_body_id(self):
        return self.body_id
