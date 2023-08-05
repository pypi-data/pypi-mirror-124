import json
import logging
import math
import os
import random
import sys
import time
import xml.etree.ElementTree as ET

import cv2
import numpy as np
import pybullet as p
import trimesh

import igibson
from igibson.external.pybullet_tools.utils import (
    get_joint_info,
    get_joints,
    link_from_name,
    matrix_from_quat,
    quat_from_matrix,
    set_joint_position,
)
from igibson.object_states.factory import prepare_object_states
from igibson.object_states.texture_change_state_mixin import TextureChangeStateMixin
from igibson.object_states.utils import clear_cached_states
from igibson.objects.stateful_object import StatefulObject
from igibson.render.mesh_renderer.materials import ProceduralMaterial, RandomizedMaterial
from igibson.utils.urdf_utils import add_fixed_link, get_base_link_name, round_up, save_urdfs_without_floating_joints
from igibson.utils.utils import get_transform_from_xyz_rpy, quatXYZWFromRotMat, rotate_vector_3d

# Optionally import bddl for object taxonomy.
try:
    from bddl.object_taxonomy import ObjectTaxonomy

    OBJECT_TAXONOMY = ObjectTaxonomy()
except ImportError:
    print("BDDL could not be imported - object taxonomy / abilities will be unavailable.", file=sys.stderr)
    OBJECT_TAXONOMY = None


class ArticulatedObject(StatefulObject):
    """
    Articulated objects are defined in URDF files.
    They are passive (no motors).
    """

    def __init__(self, filename, scale=1, merge_fixed_links=True):
        super(ArticulatedObject, self).__init__()
        self.filename = filename
        self.scale = scale
        self.merge_fixed_links = merge_fixed_links

    def _load(self):
        """
        Load the object into pybullet
        """
        flags = p.URDF_USE_MATERIAL_COLORS_FROM_MTL | p.URDF_ENABLE_SLEEPING
        if self.merge_fixed_links:
            flags |= p.URDF_MERGE_FIXED_LINKS

        body_id = p.loadURDF(self.filename, globalScaling=self.scale, flags=flags)

        self.mass = p.getDynamicsInfo(body_id, -1)[0]
        self.body_id = body_id
        self.create_link_name_to_vm_map(body_id)
        return body_id

    def create_link_name_to_vm_map(self, body_id):
        self.link_name_to_vm = []
        link_name_to_vm_urdf = {}
        for visual_shape in p.getVisualShapeData(body_id):
            id, link_id, type, dimensions, filename, rel_pos, rel_orn, color = visual_shape[:8]
            try:
                if link_id == -1:
                    link_name = p.getBodyInfo(id)[0].decode("utf-8")
                else:
                    link_name = p.getJointInfo(id, link_id)[12].decode("utf-8")
                if not link_name in link_name_to_vm_urdf:
                    link_name_to_vm_urdf[link_name] = []
                else:
                    raise ValueError("link name clashing")
                link_name_to_vm_urdf[link_name].append(filename.decode("utf-8"))
            except:
                pass
        self.link_name_to_vm = [link_name_to_vm_urdf]

    def force_wakeup(self):
        """
        Force wakeup sleeping objects
        """
        for joint_id in range(p.getNumJoints(self.body_id)):
            p.changeDynamics(self.body_id, joint_id, activationState=p.ACTIVATION_STATE_WAKE_UP)
        p.changeDynamics(self.body_id, -1, activationState=p.ACTIVATION_STATE_WAKE_UP)

    def get_body_id(self):
        return self.body_id


class RBOObject(ArticulatedObject):
    """
    RBO object from assets/models/rbo
    Reference: https://tu-rbo.github.io/articulated-objects/
    """

    def __init__(self, name, scale=1):
        filename = os.path.join(igibson.assets_path, "models", "rbo", name, "configuration", "{}.urdf".format(name))
        super(RBOObject, self).__init__(filename, scale)


class URDFObject(StatefulObject):
    """
    URDFObjects are instantiated from a URDF file. They can be composed of one
    or more links and joints. They should be passive. We use this class to
    parse our modified link tag for URDFs that embed objects into scenes
    """

    def __init__(
        self,
        filename,
        name="object_0",
        category="object",
        abilities=None,
        model_path=None,
        bounding_box=None,
        scale=None,
        fit_avg_dim_volume=False,
        connecting_joint=None,
        initial_pos=None,
        initial_orn=None,
        avg_obj_dims=None,
        joint_friction=None,
        in_rooms=None,
        texture_randomization=False,
        overwrite_inertial=True,
        scene_instance_folder=None,
        bddl_object_scope=None,
        visualize_primitives=False,
        joint_positions=None,
        merge_fixed_links=True,
        ignore_visual_shape=False,
    ):
        """
        :param filename: urdf file path of that object model
        :param name: object name, unique for each object instance, e.g. door_3
        :param category: object category, e.g. door
        :param model_path: folder path of that object model
        :param bounding_box: bounding box of this object
        :param scale: scaling factor of this object
        :param: fit_avg_dim_volume: whether to fit the object to have the same volume as the average dimension while keeping the aspect ratio
        :param connecting_joint: connecting joint to the scene that defines the object's initial pose (optional)
        :param initial_pos: initial position of the object (lower priority than connecting_joint)
        :param initial_orn: initial orientation of the object (lower priority than connecting_joint)
        :param avg_obj_dims: average object dimension of this object
        :param joint_friction: joint friction for joints in this object
        :param in_rooms: which room(s) this object is in. It can be in more than one rooms if it sits at room boundary (e.g. doors)
        :param texture_randomization: whether to enable texture randomization
        :param overwrite_inertial: whether to overwrite the inertial frame of the original URDF using trimesh + density estimate
        :param scene_instance_folder: scene instance folder to split and save sub-URDFs
        :param bddl_object_scope: bddl object scope name, e.g. chip.n.04_2
        :param visualize_primitives: whether to render geometric primitives
        :param joint_positions: Joint positions, keyed by body index and joint name, in the form of
            List[Dict[name, position]]
        """
        super(URDFObject, self).__init__()

        self.name = name
        self.category = category
        self.in_rooms = in_rooms
        self.connecting_joint = connecting_joint
        self.initial_pos = initial_pos
        self.initial_orn = initial_orn
        self.texture_randomization = texture_randomization
        self.overwrite_inertial = overwrite_inertial
        self.scene_instance_folder = scene_instance_folder
        self.bddl_object_scope = bddl_object_scope
        self.joint_positions = joint_positions
        self.merge_fixed_links = merge_fixed_links
        self.room_floor = None
        self.ignore_visual_shape = ignore_visual_shape

        # Load abilities from taxonomy if needed & possible
        if abilities is None:
            if OBJECT_TAXONOMY is not None:
                taxonomy_class = OBJECT_TAXONOMY.get_class_name_from_igibson_category(self.category)
                if taxonomy_class is not None:
                    abilities = OBJECT_TAXONOMY.get_abilities(taxonomy_class)
                else:
                    abilities = {}
            else:
                abilities = {}

        assert isinstance(abilities, dict), "Object abilities must be in dictionary form."
        self.abilities = abilities

        # Friction for all prismatic and revolute joints
        if joint_friction is not None:
            self.joint_friction = joint_friction
        else:
            if self.category in ["oven", "dishwasher"]:
                self.joint_friction = 30
            elif self.category in ["toilet"]:
                self.joint_friction = 3
            else:
                self.joint_friction = 10

        # These following fields have exactly the same length (i.e. the number
        # of sub URDFs in this object)
        # urdf_paths, string
        self.urdf_paths = []
        # object poses, 4 x 4 numpy array
        self.poses = []
        # pybullet body ids, int
        self.body_ids = []
        # whether this object is fixed or not, boolean
        self.is_fixed = []
        self.main_body = -1

        logging.info("Category " + self.category)
        self.filename = filename
        dirname = os.path.dirname(filename)
        urdf = os.path.basename(filename)
        urdf_name, _ = os.path.splitext(urdf)
        simplified_urdf = os.path.join(dirname, urdf_name + "_simplified.urdf")
        if os.path.exists(simplified_urdf):
            self.filename = simplified_urdf
            filename = simplified_urdf
        logging.info("Loading the following URDF template " + filename)
        self.object_tree = ET.parse(filename)  # Parse the URDF

        if not visualize_primitives:
            for link in self.object_tree.findall("link"):
                for element in link:
                    if element.tag == "visual" and len(element.findall(".//box")) > 0:
                        link.remove(element)

        self.model_path = model_path
        if self.model_path is None:
            self.model_path = os.path.dirname(filename)

        # Change the mesh filenames to include the entire path
        for mesh in self.object_tree.iter("mesh"):
            mesh.attrib["filename"] = os.path.join(self.model_path, mesh.attrib["filename"])

        # Apply the desired bounding box size / scale
        # First obtain the scaling factor
        if bounding_box is not None and scale is not None:
            logging.error("You cannot define both scale and bounding box size when creating a URDF Objects")
            exit(-1)

        meta_json = os.path.join(self.model_path, "misc", "metadata.json")
        bbox_json = os.path.join(self.model_path, "misc", "bbox.json")
        # In the format of {link_name: [linkX, linkY, linkZ]}
        self.metadata = {}
        meta_links = dict()
        if os.path.isfile(meta_json):
            with open(meta_json, "r") as f:
                self.metadata = json.load(f)
                bbox_size = np.array(self.metadata["bbox_size"])
                base_link_offset = np.array(self.metadata["base_link_offset"])

                if "orientations" in self.metadata and len(self.metadata["orientations"]) > 0:
                    self.orientations = self.metadata["orientations"]
                else:
                    self.orientations = None

                if "links" in self.metadata:
                    meta_links = self.metadata["links"]

        elif os.path.isfile(bbox_json):
            with open(bbox_json, "r") as bbox_file:
                bbox_data = json.load(bbox_file)
                bbox_max = np.array(bbox_data["max"])
                bbox_min = np.array(bbox_data["min"])
                bbox_size = bbox_max - bbox_min
                base_link_offset = (bbox_min + bbox_max) / 2.0
        else:
            bbox_size = None
            base_link_offset = np.zeros(3)

        if bbox_size is not None:
            if fit_avg_dim_volume:
                if avg_obj_dims is None:
                    scale = np.ones(3)
                else:
                    spec_vol = avg_obj_dims["size"][0] * avg_obj_dims["size"][1] * avg_obj_dims["size"][2]
                    cur_vol = bbox_size[0] * bbox_size[1] * bbox_size[2]
                    volume_ratio = spec_vol / cur_vol
                    size_ratio = np.cbrt(volume_ratio)
                    scale = np.array([size_ratio] * 3)
                bounding_box = bbox_size * scale
            elif bounding_box is not None:
                # Obtain the scale as the ratio between the desired bounding box size
                # and the original bounding box size of the object at scale (1, 1, 1)
                scale = bounding_box / bbox_size
            else:
                if scale is None:
                    scale = np.ones(3)
                bounding_box = bbox_size * scale

        self.scale = scale
        self.bounding_box = bounding_box

        # If no bounding box, cannot compute dynamic properties from density
        if self.bounding_box is None:
            self.overwrite_inertial = False

        logging.info("Scale: " + np.array2string(scale))

        # We need to know where the base_link origin is wrt. the bounding box
        # center. That allows us to place the model correctly since the joint
        # transformations given in the scene urdf are wrt. the bounding box
        # center. We need to scale this offset as well.
        self.scaled_bbxc_in_blf = -self.scale * base_link_offset

        self.avg_obj_dims = avg_obj_dims

        self.rename_urdf()

        self.meta_links = {}
        self.add_meta_links(meta_links)

        self.scale_object()
        self.compute_object_pose()
        self.remove_floating_joints(self.scene_instance_folder)

        prepare_object_states(self, abilities, online=True)
        self.prepare_visual_mesh_to_material()

    def set_ignore_visual_shape(self, value):
        self.ignore_visual_shape = value

    def compute_object_pose(self):
        if self.connecting_joint is not None:
            joint_type = self.connecting_joint.attrib["type"]
            joint_xyz = np.array([float(val) for val in self.connecting_joint.find("origin").attrib["xyz"].split(" ")])
            if "rpy" in self.connecting_joint.find("origin").attrib:
                joint_rpy = np.array(
                    [float(val) for val in self.connecting_joint.find("origin").attrib["rpy"].split(" ")]
                )
            else:
                joint_rpy = np.array([0.0, 0.0, 0.0])
        else:
            joint_type = "floating"
            if self.initial_pos is not None:
                joint_xyz = self.initial_pos
            else:
                joint_xyz = np.array([0.0, 0.0, 0.0])
            if self.initial_orn is not None:
                joint_rpy = self.initial_orn
            else:
                joint_rpy = np.array([0.0, 0.0, 0.0])

        # The joint location is given wrt the bounding box center but we need it wrt to the base_link frame
        # scaled_bbxc_in_blf is in object local frame, need to rotate to global (scene) frame
        x, y, z = self.scaled_bbxc_in_blf
        roll, pitch, yaw = joint_rpy
        x, y, z = rotate_vector_3d(self.scaled_bbxc_in_blf, roll, pitch, yaw, False)
        joint_xyz += np.array([x, y, z])

        # We save the transformation of the joint to be used when we load the
        # embedded urdf
        self.joint_frame = get_transform_from_xyz_rpy(joint_xyz, joint_rpy)

        self.main_body_is_fixed = joint_type == "fixed"

    def load_supporting_surfaces(self):
        self.supporting_surfaces = {}

        # Supporting surfaces can potentially refer to the names of the fixed links that are
        # merged into the world. These links will become inaccessible after the merge, e.g.
        # link_from_name will raise an error and we won't have any correspounding link id to
        # invoke get_link_state later.
        if self.merge_fixed_links:
            return

        heights_file = os.path.join(self.model_path, "misc", "heights_per_link.json")
        if not os.path.isfile(heights_file):
            return

        with open(heights_file, "r") as f:
            heights = json.load(f)

        original_object_tree = ET.parse(self.filename)
        sub_urdfs = [ET.parse(urdf_path) for urdf_path in self.urdf_paths]
        for predicate in heights:
            height_maps_dir = os.path.join(self.model_path, "misc", "height_maps_per_link", "{}".format(predicate))

            height_maps = {}
            for link_name in heights[predicate]:
                link_dir = os.path.join(height_maps_dir, link_name)

                # Get collision mesh of the link in the original urdf
                link = original_object_tree.find(".//link[@name='{}']".format(link_name))
                link_col_mesh = link.find("collision/geometry/mesh")
                col_mesh_path = os.path.join(self.model_path, link_col_mesh.attrib["filename"])

                # Try to find the body_id (after splitting) and the new link name (after renaming)
                # by matching the collision mesh file path
                new_link = None
                new_body_id = None
                assert len(sub_urdfs) == len(self.body_ids)
                for sub_urdf, body_id in zip(sub_urdfs, self.body_ids):
                    for link in sub_urdf.findall("link"):
                        link_col_mesh = link.find("collision/geometry/mesh")
                        if link_col_mesh is None:
                            continue
                        if link_col_mesh.attrib["filename"] == col_mesh_path:
                            new_link = link.attrib["name"]
                            new_body_id = body_id
                            break
                    if new_link is not None:
                        break

                assert new_link is not None
                new_link_id = link_from_name(new_body_id, new_link)

                height_maps[(new_body_id, new_link_id)] = []

                for i, z_value in enumerate(heights[predicate][link_name]):
                    img_fname = os.path.join(link_dir, link_dir, "{}.png".format(i))
                    xy_map = cv2.imread(img_fname, 0)
                    height_maps[(new_body_id, new_link_id)].append((z_value, xy_map))
            self.supporting_surfaces[predicate] = height_maps

    def sample_orientation(self):
        if self.orientations is None:
            raise ValueError("No orientation probabilities set")
        indices = list(range(len(self.orientations)))
        orientations = [np.array(o["rotation"]) for o in self.orientations]
        probabilities = [o["prob"] for o in self.orientations]
        probabilities = np.array(probabilities) / np.sum(probabilities)
        chosen_orientation_idx = np.random.choice(indices, p=probabilities)
        chosen_orientation = orientations[chosen_orientation_idx]
        # Randomize yaw based on the variation annotation
        # variation = [o['variation'] for o in self.orientations]
        # min_rotation = 0.05
        # rotation_variance = max(
        #     variation[chosen_orientation_idx], min_rotation)
        # rot_num = np.random.random() * rotation_variance

        # Randomize yaw from -pi to pi
        rot_num = np.random.uniform(-1, 1)
        rot_matrix = np.array(
            [
                [math.cos(math.pi * rot_num), -math.sin(math.pi * rot_num), 0.0],
                [math.sin(math.pi * rot_num), math.cos(math.pi * rot_num), 0.0],
                [0.0, 0.0, 1.0],
            ]
        )
        rotated_quat = quat_from_matrix(np.dot(rot_matrix, matrix_from_quat(chosen_orientation)))
        return rotated_quat

    def get_prefixed_joint_name(self, name):
        return self.name + "_" + name

    def rename_urdf(self):
        """
        Helper function that renames the file paths in the object urdf
        from relative paths to absolute paths
        """
        base_link_name = get_base_link_name(self.object_tree)

        # Change the links of the added object to adapt to the given name
        for link_emb in self.object_tree.iter("link"):
            # If the original urdf already contains world link, do not rename
            if link_emb.attrib["name"] == "world":
                pass
            elif link_emb.attrib["name"] == base_link_name:
                # The base_link get renamed as the link tag indicates
                # Just change the name of the base link in the embedded urdf
                link_emb.attrib["name"] = self.name
            else:
                # The other links get also renamed to add the name of the link tag as prefix
                # This allows us to load several instances of the same object
                link_emb.attrib["name"] = self.name + "_" + link_emb.attrib["name"]

        # Change the joints of the added object to adapt them to the given name
        for joint_emb in self.object_tree.iter("joint"):
            # We change the joint name
            joint_emb.attrib["name"] = self.get_prefixed_joint_name(joint_emb.attrib["name"])
            # We change the child link names
            for child_emb in joint_emb.findall("child"):
                # If the original urdf already contains world link, do not rename
                if child_emb.attrib["link"] == "world":
                    pass
                elif child_emb.attrib["link"] == base_link_name:
                    child_emb.attrib["link"] = self.name
                else:
                    child_emb.attrib["link"] = self.name + "_" + child_emb.attrib["link"]
            # and the parent link names
            for parent_emb in joint_emb.findall("parent"):
                # If the original urdf already contains world link, do not rename
                if parent_emb.attrib["link"] == "world":
                    pass
                elif parent_emb.attrib["link"] == base_link_name:
                    parent_emb.attrib["link"] = self.name
                else:
                    parent_emb.attrib["link"] = self.name + "_" + parent_emb.attrib["link"]

    def scale_object(self):
        """
        Scale the object according to the given bounding box
        """
        # We need to scale 1) the meshes, 2) the position of meshes, 3) the position of joints, 4) the orientation
        # axis of joints. The problem is that those quantities are given wrt. its parent link frame, and this can be
        # rotated wrt. the frame the scale was given in Solution: parse the kin tree joint by joint, extract the
        # rotation, rotate the scale, apply rotated scale to 1, 2, 3, 4 in the child link frame

        # First, define the scale in each link reference frame
        # and apply it to the joint values
        base_link_name = get_base_link_name(self.object_tree)
        scales_in_lf = {base_link_name: self.scale}
        all_processed = False
        while not all_processed:
            all_processed = True
            for joint in self.object_tree.iter("joint"):
                parent_link_name = joint.find("parent").attrib["link"]
                child_link_name = joint.find("child").attrib["link"]
                if parent_link_name in scales_in_lf and child_link_name not in scales_in_lf:
                    scale_in_parent_lf = scales_in_lf[parent_link_name]
                    # The location of the joint frame is scaled using the scale in the parent frame
                    for origin in joint.iter("origin"):
                        current_origin_xyz = np.array([float(val) for val in origin.attrib["xyz"].split(" ")])
                        new_origin_xyz = np.multiply(current_origin_xyz, scale_in_parent_lf)
                        new_origin_xyz = np.array([round_up(val, 10) for val in new_origin_xyz])
                        origin.attrib["xyz"] = " ".join(map(str, new_origin_xyz))

                    # scale the prismatic joint
                    if joint.attrib["type"] == "prismatic":
                        limits = joint.findall("limit")
                        assert len(limits) == 1
                        limit = limits[0]
                        axes = joint.findall("axis")
                        assert len(axes) == 1
                        axis = axes[0]
                        axis_np = np.array([float(elem) for elem in axis.attrib["xyz"].split()])
                        major_axis = np.argmax(np.abs(axis_np))
                        # assume the prismatic joint is roughly axis-aligned
                        limit.attrib["upper"] = str(float(limit.attrib["upper"]) * scale_in_parent_lf[major_axis])
                        limit.attrib["lower"] = str(float(limit.attrib["lower"]) * scale_in_parent_lf[major_axis])

                    # Get the rotation of the joint frame and apply it to the scale
                    if "rpy" in joint.keys():
                        joint_frame_rot = np.array([float(val) for val in joint.attrib["rpy"].split(" ")])
                        # Rotate the scale
                        scale_in_child_lf = rotate_vector_3d(scale_in_parent_lf, *joint_frame_rot, cck=True)
                        scale_in_child_lf = np.absolute(scale_in_child_lf)
                    else:
                        scale_in_child_lf = scale_in_parent_lf

                    # print("Adding: ", joint.find("child").attrib["link"])

                    scales_in_lf[joint.find("child").attrib["link"]] = scale_in_child_lf

                    # The axis of the joint is defined in the joint frame, we scale it after applying the rotation
                    for axis in joint.iter("axis"):
                        current_axis_xyz = np.array([float(val) for val in axis.attrib["xyz"].split(" ")])
                        new_axis_xyz = np.multiply(current_axis_xyz, scale_in_child_lf)
                        new_axis_xyz /= np.linalg.norm(new_axis_xyz)
                        new_axis_xyz = np.array([round_up(val, 10) for val in new_axis_xyz])
                        axis.attrib["xyz"] = " ".join(map(str, new_axis_xyz))

                    # Iterate again the for loop since we added new elements to the dictionary
                    all_processed = False

        all_links = self.object_tree.findall("link")
        # compute dynamics properties
        if self.overwrite_inertial and self.category not in ["walls", "floors", "ceilings"]:
            all_links_trimesh = []
            total_volume = 0.0
            for link in all_links:
                meshes = link.findall("collision/geometry/mesh")
                if len(meshes) == 0:
                    all_links_trimesh.append(None)
                    continue
                # assume one collision mesh per link
                assert len(meshes) == 1, (self.filename, link.attrib["name"])
                # check collision mesh path
                collision_mesh_path = os.path.join(meshes[0].attrib["filename"])
                trimesh_obj = trimesh.load(file_obj=collision_mesh_path, force="mesh")
                all_links_trimesh.append(trimesh_obj)
                volume = trimesh_obj.volume
                # a hack to artificially increase the density of the lamp base
                if link.attrib["name"] == base_link_name:
                    if self.category in ["lamp"]:
                        volume *= 10.0
                total_volume += volume

            # avg L x W x H and Weight is given for this object category
            if self.avg_obj_dims is not None:
                avg_density = self.avg_obj_dims["density"]

            # otherwise, use the median density across all existing object categories
            else:
                avg_density = 67.0

            # Scale the mass based on bounding box size
            # TODO: how to scale moment of inertia?
            total_mass = avg_density * self.bounding_box[0] * self.bounding_box[1] * self.bounding_box[2]
            # print('total_mass', total_mass)

            density = total_mass / total_volume
            # print('avg density', density)
            for trimesh_obj in all_links_trimesh:
                if trimesh_obj is not None:
                    trimesh_obj.density = density

            assert len(all_links_trimesh) == len(all_links)

        # Now iterate over all links and scale the meshes and positions
        for i, link in enumerate(all_links):
            if self.overwrite_inertial and self.category not in ["walls", "floors", "ceilings"]:
                link_trimesh = all_links_trimesh[i]
                # assign dynamics properties
                inertials = link.findall("inertial")
                if len(inertials) == 0:
                    inertial = ET.SubElement(link, "inertial")
                else:
                    assert len(inertials) == 1
                    inertial = inertials[0]

                masses = inertial.findall("mass")
                if len(masses) == 0:
                    mass = ET.SubElement(inertial, "mass")
                else:
                    assert len(masses) == 1
                    mass = masses[0]

                inertias = inertial.findall("inertia")
                if len(inertias) == 0:
                    inertia = ET.SubElement(inertial, "inertia")
                else:
                    assert len(inertias) == 1
                    inertia = inertias[0]

                origins = inertial.findall("origin")
                if len(origins) == 0:
                    origin = ET.SubElement(inertial, "origin")
                else:
                    assert len(origins) == 1
                    origin = origins[0]

                if link_trimesh is not None:
                    # a hack to artificially increase the density of the lamp base
                    if link.attrib["name"] == base_link_name:
                        if self.category in ["lamp"]:
                            link_trimesh.density *= 10.0

                    if link_trimesh.is_watertight:
                        center = np.copy(link_trimesh.center_mass)
                    else:
                        center = np.copy(link_trimesh.centroid)

                    collision_mesh = [col for col in link.findall("collision") if col.find("geometry/mesh") is not None]
                    assert len(collision_mesh) == 1, "more than one collision mesh in one link"
                    collision_mesh = collision_mesh[0]
                    collision_mesh_origin = collision_mesh.find("origin")
                    if collision_mesh_origin is not None:
                        offset = np.array([float(val) for val in collision_mesh_origin.attrib["xyz"].split(" ")])
                        center += offset

                    # The inertial frame origin will be scaled down below.
                    # Here, it has the value BEFORE scaling
                    origin.attrib["xyz"] = " ".join(map(str, center))
                    origin.attrib["rpy"] = " ".join(map(str, [0.0, 0.0, 0.0]))

                    mass.attrib["value"] = str(round_up(link_trimesh.mass, 10))
                    moment_of_inertia = link_trimesh.moment_inertia
                    inertia.attrib["ixx"] = str(moment_of_inertia[0][0])
                    inertia.attrib["ixy"] = str(moment_of_inertia[0][1])
                    inertia.attrib["ixz"] = str(moment_of_inertia[0][2])
                    inertia.attrib["iyy"] = str(moment_of_inertia[1][1])
                    inertia.attrib["iyz"] = str(moment_of_inertia[1][2])
                    inertia.attrib["izz"] = str(moment_of_inertia[2][2])
                else:
                    # empty link that does not have any mesh
                    origin.attrib["xyz"] = " ".join(map(str, [0.0, 0.0, 0.0]))
                    origin.attrib["rpy"] = " ".join(map(str, [0.0, 0.0, 0.0]))
                    mass.attrib["value"] = str(0.0)
                    inertia.attrib["ixx"] = str(0.0)
                    inertia.attrib["ixy"] = str(0.0)
                    inertia.attrib["ixz"] = str(0.0)
                    inertia.attrib["iyy"] = str(0.0)
                    inertia.attrib["iyz"] = str(0.0)
                    inertia.attrib["izz"] = str(0.0)

            scale_in_lf = scales_in_lf[link.attrib["name"]]
            # Apply the scale to all mesh elements within the link (original scale and origin)
            for mesh in link.iter("mesh"):
                if "scale" in mesh.attrib:
                    mesh_scale = np.array([float(val) for val in mesh.attrib["scale"].split(" ")])
                    new_scale = np.multiply(mesh_scale, scale_in_lf)
                    new_scale = np.array([round_up(val, 10) for val in new_scale])
                    mesh.attrib["scale"] = " ".join(map(str, new_scale))
                else:
                    new_scale = np.array([round_up(val, 10) for val in scale_in_lf])
                    mesh.set("scale", " ".join(map(str, new_scale)))

            for box in link.iter("box"):
                if "size" in box.attrib:
                    box_scale = np.array([float(val) for val in box.attrib["size"].split(" ")])
                    new_scale = np.multiply(box_scale, scale_in_lf)
                    new_scale = np.array([round_up(val, 10) for val in new_scale])
                    box.attrib["size"] = " ".join(map(str, new_scale))

            for origin in link.iter("origin"):
                origin_xyz = np.array([float(val) for val in origin.attrib["xyz"].split(" ")])
                new_origin_xyz = np.multiply(origin_xyz, scale_in_lf)
                new_origin_xyz = np.array([round_up(val, 10) for val in new_origin_xyz])
                origin.attrib["xyz"] = " ".join(map(str, new_origin_xyz))

    def remove_floating_joints(self, folder=None):
        """
        Split a single urdf to multiple urdfs if there exist floating joints
        """
        if folder is None:
            timestr = time.strftime("%Y%m%d-%H%M%S")
            folder = os.path.join(
                igibson.ig_dataset_path,
                "scene_instances",
                "{}_{}_{}".format(timestr, random.getrandbits(64), os.getpid()),
            )
            os.makedirs(folder, exist_ok=True)

        # Deal with floating joints inside the embedded urdf
        file_prefix = os.path.join(folder, self.name)
        urdfs_no_floating = save_urdfs_without_floating_joints(self.object_tree, self.main_body_is_fixed, file_prefix)

        # append a new tuple of file name of the instantiated embedded urdf
        # and the transformation (!= identity if its connection was floating)
        for i, urdf in enumerate(urdfs_no_floating):
            self.urdf_paths.append(urdfs_no_floating[urdf][0])
            transformation = np.dot(self.joint_frame, urdfs_no_floating[urdf][1])
            self.poses.append(transformation)
            self.is_fixed.append(urdfs_no_floating[urdf][2])
            if urdfs_no_floating[urdf][3]:
                self.main_body = i

    def prepare_visual_mesh_to_material(self):
        # mapping between visual objects and possible textures
        # multiple visual objects can share the same material
        # if some sub URDF does not have visual object or this URDF is part of
        # the building structure, it will have an empty dict
        # [
        #     {                                             # 1st sub URDF
        #         'visual_1.obj': randomized_material_1
        #         'visual_2.obj': randomized_material_1
        #     },
        #     {},                                            # 2nd sub URDF
        #     {                                              # 3rd sub URDF
        #         'visual_3.obj': randomized_material_2
        #     }
        # ]

        self.visual_mesh_to_material = [{} for _ in self.urdf_paths]

        # a list of all materials used for RandomizedMaterial
        self.randomized_materials = []
        # mapping from material class to friction coefficient
        self.material_to_friction = None

        # procedural material that can change based on state changes
        self.procedural_material = None

        self.texture_procedural_generation = False
        for state in self.states:
            if issubclass(state, TextureChangeStateMixin):
                self.texture_procedural_generation = True
                break

        if self.texture_randomization and self.texture_procedural_generation:
            raise ValueError("Cannot support both randomized and procedural texture")

        if self.texture_randomization:
            self.prepare_randomized_texture()
        if self.texture_procedural_generation:
            self.prepare_procedural_texture()

        self.create_link_name_vm_mapping()

    def create_link_name_vm_mapping(self):
        self.link_name_to_vm = []

        for i in range(len(self.urdf_paths)):
            link_name_to_vm_urdf = {}
            sub_urdf_tree = ET.parse(self.urdf_paths[i])

            links = sub_urdf_tree.findall(".//link")
            for link in links:
                name = link.attrib["name"]
                if name in link_name_to_vm_urdf:
                    raise ValueError("link name collision")
                link_name_to_vm_urdf[name] = []
                for visual_mesh in link.findall("visual/geometry/mesh"):
                    link_name_to_vm_urdf[name].append(visual_mesh.attrib["filename"])
            self.link_name_to_vm.append(link_name_to_vm_urdf)

    def randomize_texture(self):
        """
        Randomize texture and material for each link / visual shape
        """
        for material in self.randomized_materials:
            material.randomize()
        self.update_friction()

    def update_friction(self):
        """
        Update the surface lateral friction for each link based on its material
        """
        if self.material_to_friction is None:
            return
        for i in range(len(self.urdf_paths)):
            # if the sub URDF does not have visual meshes
            if len(self.visual_mesh_to_material[i]) == 0:
                continue
            body_id = self.body_ids[i]
            sub_urdf_tree = ET.parse(self.urdf_paths[i])

            for j in np.arange(-1, p.getNumJoints(body_id)):
                # base_link
                if j == -1:
                    link_name = p.getBodyInfo(body_id)[0].decode("UTF-8")
                else:
                    link_name = p.getJointInfo(body_id, j)[12].decode("UTF-8")
                link = sub_urdf_tree.find(".//link[@name='{}']".format(link_name))
                link_materials = []
                for visual_mesh in link.findall("visual/geometry/mesh"):
                    link_materials.append(self.visual_mesh_to_material[i][visual_mesh.attrib["filename"]])
                link_frictions = []
                for link_material in link_materials:
                    if link_material.random_class is None:
                        friction = 0.5
                    elif link_material.random_class not in self.material_to_friction:
                        friction = 0.5
                    else:
                        friction = self.material_to_friction.get(link_material.random_class, 0.5)
                    link_frictions.append(friction)
                link_friction = np.mean(link_frictions)
                p.changeDynamics(body_id, j, lateralFriction=link_friction)

    def prepare_randomized_texture(self):
        """
        Set up mapping from visual meshes to randomizable materials
        """
        if self.category in ["walls", "floors", "ceilings"]:
            material_groups_file = os.path.join(
                self.model_path, "misc", "{}_material_groups.json".format(self.category)
            )
        else:
            material_groups_file = os.path.join(self.model_path, "misc", "material_groups.json")

        assert os.path.isfile(material_groups_file), "cannot find material group: {}".format(material_groups_file)
        with open(material_groups_file) as f:
            material_groups = json.load(f)

        # create randomized material for each material group
        all_material_categories = material_groups[0]
        all_materials = {}
        for key in all_material_categories:
            all_materials[int(key)] = RandomizedMaterial(all_material_categories[key])

        # make visual mesh file path absolute
        visual_mesh_to_idx = material_groups[1]
        for old_path in list(visual_mesh_to_idx.keys()):
            new_path = os.path.join(self.model_path, "shape", "visual", old_path)
            visual_mesh_to_idx[new_path] = visual_mesh_to_idx[old_path]
            del visual_mesh_to_idx[old_path]

        # check each visual object belongs to which sub URDF in case of splitting
        for i, urdf_path in enumerate(self.urdf_paths):
            sub_urdf_tree = ET.parse(urdf_path)
            for visual_mesh_path in visual_mesh_to_idx:
                # check if this visual object belongs to this URDF
                if sub_urdf_tree.find(".//mesh[@filename='{}']".format(visual_mesh_path)) is not None:
                    self.visual_mesh_to_material[i][visual_mesh_path] = all_materials[
                        visual_mesh_to_idx[visual_mesh_path]
                    ]

        self.randomized_materials = list(all_materials.values())

        friction_json = os.path.join(igibson.ig_dataset_path, "materials", "material_friction.json")
        if os.path.isfile(friction_json):
            with open(friction_json) as f:
                self.material_to_friction = json.load(f)

    def prepare_procedural_texture(self):
        """
        Set up mapping from visual meshes to procedural materials
        Assign all visual meshes to the same ProceduralMaterial
        """
        procedural_material = ProceduralMaterial(material_folder=os.path.join(self.model_path, "material"))

        for i, urdf_path in enumerate(self.urdf_paths):
            sub_urdf_tree = ET.parse(urdf_path)
            for visual_mesh in sub_urdf_tree.findall("link/visual/geometry/mesh"):
                filename = visual_mesh.attrib["filename"]
                self.visual_mesh_to_material[i][filename] = procedural_material

        for state in self.states:
            if issubclass(state, TextureChangeStateMixin):
                procedural_material.add_state(state)
                self.states[state].material = procedural_material

        self.procedural_material = procedural_material

    def _load(self):
        """
        Load the object into pybullet and set it to the correct pose
        """
        flags = p.URDF_ENABLE_SLEEPING
        if self.merge_fixed_links:
            flags |= p.URDF_MERGE_FIXED_LINKS

        if self.ignore_visual_shape:
            flags |= p.URDF_IGNORE_VISUAL_SHAPES

        for idx in range(len(self.urdf_paths)):
            logging.info("Loading " + self.urdf_paths[idx])
            is_fixed = self.is_fixed[idx]
            body_id = p.loadURDF(self.urdf_paths[idx], flags=flags, useFixedBase=is_fixed)
            # flags=p.URDF_USE_MATERIAL_COLORS_FROM_MTL)
            transformation = self.poses[idx]
            pos = transformation[0:3, 3]
            orn = np.array(quatXYZWFromRotMat(transformation[0:3, 0:3]))
            logging.info("Moving URDF to (pos,ori): " + np.array_str(pos) + ", " + np.array_str(orn))
            dynamics_info = p.getDynamicsInfo(body_id, -1)
            inertial_pos, inertial_orn = dynamics_info[3], dynamics_info[4]
            pos, orn = p.multiplyTransforms(pos, orn, inertial_pos, inertial_orn)
            p.resetBasePositionAndOrientation(body_id, pos, orn)
            p.changeDynamics(body_id, -1, activationState=p.ACTIVATION_STATE_ENABLE_SLEEPING)

            for j in get_joints(body_id):
                info = get_joint_info(body_id, j)
                jointType = info.jointType
                if jointType in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC]:
                    p.setJointMotorControl2(
                        body_id, j, p.VELOCITY_CONTROL, targetVelocity=0.0, force=self.joint_friction
                    )

                    # Only need to restore revolute and prismatic joints
                    if self.joint_positions:
                        joint_name = str(info.jointName, encoding="utf-8")
                        joint_position = self.joint_positions[idx][joint_name]
                        set_joint_position(body_id, j, joint_position)

            self.body_ids.append(body_id)

        self.load_supporting_surfaces()

        return self.body_ids

    def force_wakeup(self):
        """
        Force wakeup sleeping objects
        """
        for body_id in self.body_ids:
            for joint_id in range(p.getNumJoints(body_id)):
                p.changeDynamics(body_id, joint_id, activationState=p.ACTIVATION_STATE_WAKE_UP)
            p.changeDynamics(body_id, -1, activationState=p.ACTIVATION_STATE_WAKE_UP)

    def reset(self):
        """
        Reset the object to its original pose and joint configuration
        """
        for idx in range(len(self.body_ids)):
            body_id = self.body_ids[idx]
            transformation = self.poses[idx]
            pos = transformation[0:3, 3]
            orn = np.array(quatXYZWFromRotMat(transformation[0:3, 0:3]))
            logging.info("Resetting URDF to (pos,ori): " + np.array_str(pos) + ", " + np.array_str(orn))
            dynamics_info = p.getDynamicsInfo(body_id, -1)
            inertial_pos, inertial_orn = dynamics_info[3], dynamics_info[4]
            pos, orn = p.multiplyTransforms(pos, orn, inertial_pos, inertial_orn)
            p.resetBasePositionAndOrientation(body_id, pos, orn)

            # reset joint position to 0.0
            for j in range(p.getNumJoints(body_id)):
                info = p.getJointInfo(body_id, j)
                jointType = info[2]
                if jointType in [p.JOINT_REVOLUTE, p.JOINT_PRISMATIC]:
                    p.resetJointState(body_id, j, targetValue=0.0, targetVelocity=0.0)
                    p.setJointMotorControl2(
                        body_id, j, p.VELOCITY_CONTROL, targetVelocity=0.0, force=self.joint_friction
                    )

    def get_position(self):
        """
        Get object position

        :return: position in xyz
        """
        body_id = self.get_body_id()
        pos, _ = p.getBasePositionAndOrientation(body_id)
        return pos

    def get_orientation(self):
        """
        Get object orientation

        :return: quaternion in xyzw
        """
        body_id = self.get_body_id()
        _, orn = p.getBasePositionAndOrientation(body_id)
        return orn

    def get_position_orientation(self):
        """
        Get object position and orientation

        :return: position in xyz
        :return: quaternion in xyzw
        """
        body_id = self.get_body_id()
        pos, orn = p.getBasePositionAndOrientation(body_id)
        return pos, orn

    def get_base_link_position_orientation(self):
        """
        Get object base link position and orientation

        :return: position in xyz
        :return: quaternion in xyzw
        """
        # TODO: not used anywhere yet, but probably should be put in ObjectBase
        body_id = self.get_body_id()
        pos, orn = p.getBasePositionAndOrientation(body_id)
        dynamics_info = p.getDynamicsInfo(body_id, -1)
        inertial_pos = dynamics_info[3]
        inertial_orn = dynamics_info[4]
        inv_inertial_pos, inv_inertial_orn = p.invertTransform(inertial_pos, inertial_orn)
        pos, orn = p.multiplyTransforms(pos, orn, inv_inertial_pos, inv_inertial_orn)
        return pos, orn

    def set_position(self, pos):
        """
        Set object position

        :param pos: position in xyz
        """
        body_id = self.get_body_id()
        if self.main_body_is_fixed:
            logging.warning("cannot set_position for fixed objects")
            return

        _, old_orn = p.getBasePositionAndOrientation(body_id)
        p.resetBasePositionAndOrientation(body_id, pos, old_orn)
        clear_cached_states(self)

    def set_orientation(self, orn):
        """
        Set object orientation

        :param orn: quaternion in xyzw
        """
        body_id = self.get_body_id()
        if self.main_body_is_fixed:
            logging.warning("cannot set_orientation for fixed objects")
            return

        old_pos, _ = p.getBasePositionAndOrientation(body_id)
        p.resetBasePositionAndOrientation(body_id, old_pos, orn)
        clear_cached_states(self)

    def set_position_orientation(self, pos, orn):
        """
        Set object position and orientation
        :param pos: position in xyz
        :param orn: quaternion in xyzw
        """
        body_id = self.get_body_id()
        if self.main_body_is_fixed:
            logging.warning("cannot set_position_orientation for fixed objects")
            return

        p.resetBasePositionAndOrientation(body_id, pos, orn)
        clear_cached_states(self)

    def set_base_link_position_orientation(self, pos, orn):
        body_id = self.get_body_id()
        if self.main_body_is_fixed:
            logging.warning("cannot set_base_link_position_orientation for fixed objects")
            return
        dynamics_info = p.getDynamicsInfo(body_id, -1)
        inertial_pos, inertial_orn = dynamics_info[3], dynamics_info[4]
        pos, orn = p.multiplyTransforms(pos, orn, inertial_pos, inertial_orn)
        self.set_position_orientation(pos, orn)
        clear_cached_states(self)

    def get_body_id(self):
        return self.body_ids[self.main_body]

    def add_meta_links(self, meta_links):
        """
        Adds the meta links (e.g. heating element position, water source position) from the metadata file
        into the URDF tree for this object prior to loading.

        :param meta_links: Dictionary of meta links in the form of {link_name: [linkX, linkY, linkZ]}
        :return: None.
        """
        for meta_link_name, link_info in meta_links.items():
            if link_info["geometry"] is not None:
                # Objects with geometry actually need to be added into the URDF for collision purposes.
                # These objects cannot be imported with fixed links.
                self.merge_fixed_links = False
                add_fixed_link(self.object_tree, meta_link_name, link_info)
            else:
                # Otherwise, the "link" is just an offset, so we save its position.
                self.meta_links[meta_link_name] = np.array(link_info["xyz"])

    # TODO: remove after split floors
    def set_room_floor(self, room_floor):
        assert self.category == "floors"
        self.room_floor = room_floor
