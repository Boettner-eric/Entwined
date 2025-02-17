#!/usr/bin/env python3

# Turn an Entwined fairy circle definition file into an LXstudio fixture file(s)

import argparse
import json
from pathlib import Path

import numpy as np


class FairyCircle:
    MINICLUSTER_RADIUS = 18.0

    # the heights are different
    MINICLUSTER_HEIGHTS = [
                             12.0, 14.0, 14.0, 16.0,
                             16.0, 18.0, 18.0, 20.0,
                             20.0, 18.0, 18.0, 16.0,
                             16.0, 14.0, 14.0, 12.0,
                             ];

    MINICLUSTER_N_CUBES = 12;

    # this routine is for arcs

    def circle_add_cubes(self, config):
        cluster_rotation = 0
        for _ in range(len(self.ip_addrs)):  # walking through the ndbs
            ndb_cubes = []
            for _ in range(self.clusters_per_ndb):
                cluster_cubes = []
                stem_rotation = 0
                stem_rot_step = (2*np.pi)/float(self.MINICLUSTER_N_CUBES)
                cluster_rot_matrix = np.array([[np.cos(cluster_rotation), 0, np.sin(cluster_rotation)],
                                               [0, 1, 0],
                                               [-np.sin(cluster_rotation), 0, np.cos(cluster_rotation)]])
                for idx in range(self.MINICLUSTER_N_CUBES):
                    # initial position, relative to the minicluster center...
                    cube_pos = np.array([self.MINICLUSTER_RADIUS * np.cos(stem_rotation),
                                         self.MINICLUSTER_HEIGHTS[idx],
                                         self.MINICLUSTER_RADIUS * np.sin(stem_rotation)])
                    # change to relative to the center of the fairy circle
                    cube_pos = np.dot(cube_pos, cluster_rot_matrix)
                    cube_pos += np.array([self.radius * np.cos(cluster_rotation),
                                         0,
                                         self.radius * np.sin(cluster_rotation)])
                    # change to global coordinates
                    cube_pos = np.dot(cube_pos, self.rotation)
                    cube_pos += self.translation

                    cluster_cubes.append(cube_pos)
                    stem_rotation += stem_rot_step

                cluster_rotation += self.arc_step
                cluster_cubes.reverse()   # because apparently we wire these counterclockwise

                ndb_cubes.append(cluster_cubes)

        return(ndb_cubes)

    # this routine is for straight lines of babies / miniclusters
    # to use: tags: 'shape' is 'line'
    # 'separation' is between the babies/clusters
    # 'ry' is the rotation of the entire piece
    # line rotation: 0 degrees is where cluster 1 is aligned with positive X, then clockwise
    # X and Y position is the center of the line (where the NDB is)

    # ry is the rotation of each mini

    # can't really imagine there is more than one 

    def line_add_cubes(self, config):
        cluster_distance = - (self.distance * np.floor(self.clusters_per_ndb / 2))

        ndb_cubes = []
        for _ in range(self.clusters_per_ndb):
            # print(f'line: next cluster: distance {cluster_distance}')
            cluster_cubes = []
            stem_rotation = 0
            stem_rot_step = (2*np.pi)/float(self.MINICLUSTER_N_CUBES)

            for idx in range(self.MINICLUSTER_N_CUBES):
                # initial position, relative to the minicluster center...
                cube_pos = np.array([self.MINICLUSTER_RADIUS * np.cos(stem_rotation),
                                     self.MINICLUSTER_HEIGHTS[idx],
                                     self.MINICLUSTER_RADIUS * np.sin(stem_rotation)])
                # change to relative to the center of the line
                cube_pos += np.array([cluster_distance, 0, 0])
                # change to global coordinates
                cube_pos = np.dot(cube_pos, self.rotation)
                cube_pos += self.translation

                cluster_cubes.append(cube_pos)
                stem_rotation += stem_rot_step

            cluster_cubes.reverse()   # because apparently we wire these counterclockwise

            ndb_cubes.append(cluster_cubes)

            cluster_distance += self.distance

        return(ndb_cubes)


    def __init__(self, config):
        rot = np.radians( config['ry'] ) # get into radians
        self.rotation = np.array([[np.cos(rot), 0, np.sin(rot)],
                                  [0, 1, 0],
                                  [-np.sin(rot), 0, np.cos(rot)]])
        self.translation = np.array([config['x'], 0, config['z']])

        self.ip_addrs = config['ipAddresses']
        self.piece_id = config['pieceId']
        self.ry = config['ry'] # degrees
        if 'clustersPerNdb' in config:
            self.clusters_per_ndb = config['clustersPerNdb']
        else:
            self.clusters_per_ndb = 5
        self.cubes = []

        # default is circle (it was first), includes arcs
        if 'shape' not in config:
            config['shape'] = 'circle'

        if config['shape'] == 'line':
            if 'separation' not in config:
                print('shape line must have separation, distance between babies in inches')
                exit()
            self.distance = config['separation']  # distance between babies

            if len(self.ip_addrs) != 1:
                print(f'lines must have only one NDB not {len(self.ip_addrs)}')
                exit()          

            ndb_cubes = self.line_add_cubes(config)

        if (config['shape'] == 'circle') or (config['shape'] == 'arc'):
            if 'radius' not in config:
                print('shape circle must have radius, try gain')
                exit()

            self.radius = config['radius']
            if 'degrees' in config:
                arc = (np.pi * float(config['degrees'])) / 180.0
            else:
                arc = 2.0 * np.pi
            self.arc_step = arc / (self.clusters_per_ndb*len(self.ip_addrs)) # the number of ndbs is the size of the ip_addr array

            ndb_cubes = self.circle_add_cubes(config)

        # print(f' processed shape, ndb cubes is {ndb_cubes}')

        # there's an issue here about how the miniclusters are actually attached to the ndbs, which is not
        # in rotational order.  Instead of 1-2-3-4-5, it's 2-1-3-4-5 (for 5) but 1-2-3 (for 3)
        if (self.clusters_per_ndb == 5):
            self.cubes += ndb_cubes[1]
            self.cubes += ndb_cubes[0]
            self.cubes += ndb_cubes[2]
            self.cubes += ndb_cubes[3]
            self.cubes += ndb_cubes[4]
        elif (self.clusters_per_ndb == 3):
            self.cubes += ndb_cubes[0]
            self.cubes += ndb_cubes[1]
            self.cubes += ndb_cubes[2]
        else:
            print(f'only supports 3 and 5 clusters per ndb, not {self.clusters_per_ndb}')
            exit()

    def write_fixture_file(self, folder):
        folder_path = Path(folder)
        folder_path.mkdir(parents=True, exist_ok=True)
        filename = Path(self.piece_id + ".lxf")
        file_path = folder_path / filename
        lx_config = {'label': self.piece_id,
                     'tags': ['FAIRY_CIRCLE', self.piece_id],
                     'components': [{'type': 'points', 'coords': []}],
                     'outputs': [],
                     "meta": {"name": self.piece_id,
                              "base_x": int(self.translation[0]),
                              "base_y": int(self.translation[1]),
                              "base_z": int(self.translation[2]),
                              "ry": self.ry
                     }}
        coords = lx_config['components'][0]['coords']
        outputs = lx_config['outputs']
        for cube in self.cubes:
            # NB - the multiple leds in one cube issue does not occur with fairy circles...
            coords.append({'x': cube[0], 'y': cube[1], 'z': cube[2]})

        num_cubes_per_ndb = self.MINICLUSTER_N_CUBES * self.clusters_per_ndb
        total_cubes = 0
        for ip_addr in self.ip_addrs:
            outputs.append({'protocol': 'ddp',
                      'host': ip_addr,
                      'start': total_cubes,
                      'num' : num_cubes_per_ndb
                     })
            total_cubes += num_cubes_per_ndb

        with open(file_path, 'w+') as output_f:
            json.dump(lx_config, output_f, indent=4)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create newlx fixture configs from fairy circle  configuration file')
    parser.add_argument('-c', '--config', type=str, required=True, help='Input fairy circle JSON configuration file')
    parser.add_argument('-f', '--fixtures_folder', type=str, required=True, help='Folder to output lx configurations')
    args = parser.parse_args()

    # Read configuration file. (They're json files)
    with open(args.config) as sc_f:
        fc_configs = json.load(sc_f)  # XXX catch exceptions here.

    # Now let's create some circles and cubes ...
    for config in fc_configs:
        circle = FairyCircle(config)
        circle.write_fixture_file(args.fixtures_folder)
