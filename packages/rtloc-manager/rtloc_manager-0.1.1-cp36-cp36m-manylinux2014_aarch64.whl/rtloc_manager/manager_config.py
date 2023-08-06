"""
    RTLOC - Manager Lib

    rtloc_manager/manager_config.py

    (c) 2021 RTLOC/Callitrix NV. All rights reserved.

    Jasper Wouters <jasper@rtloc.com>

"""

import yaml
import json
from bunch import Bunch
import paho.mqtt.subscribe as mqtt

class ManagerConfig(Bunch):
    def __init__(self, config_dict):
        super().__init__(config_dict)

    @staticmethod
    def from_yaml(yaml_file):
        """ Create a manager config object from the given yaml file.

        Args:
            yaml_file (str): path to yaml config file

        Returns:
            ManagerConfig: manager configuration object
        """
        with open(yaml_file) as yaml_fh:
            config_dict = yaml.safe_load(yaml_fh)
            return ManagerConfig(config_dict)

    @staticmethod
    def from_mqtt(mqtt_settings_file, local_config_file):
        # load initial mqtt settings from hub-style json
        with open(mqtt_settings_file, "rb") as fp:
            mqtt_settings = json.load(fp)
        mqtt_settings = Bunch(mqtt_settings)

        # TODO get root topic from mqtt_settings
        root_topic = "kart/"
        config_topic = root_topic + "config"

        if mqtt_settings.port == 1883:
            transport = "tcp"
            tls=None
        elif mqtt_settings.port == 8083:
            # TODO: needs fix
            transport = "websockets"
            tls=None
        elif mqtt_settings.port == 8883:
            # TODO: supply certificate
            transport = "tcp"
            tls = {"ca_certs": ""}

        try:
            config_payload = mqtt.simple(config_topic, hostname=mqtt_settings.host, port=mqtt_settings.port,
                                         auth={"username": mqtt_settings.username, "password": mqtt_settings.password},
                                         retained=True, transport=transport, tls=tls).payload
            remote_payload_received = True
        except Exception as e:
            print("[MQTT issue]:", e)

            print("[Given MQTT settings]:")
            print(mqtt_settings.host)
            print(mqtt_settings.port)
            print(mqtt_settings.username)
            print(mqtt_settings.password)

            remote_payload_received = False

        # load local config
        with open(local_config_file, "rb") as fp:
            config_dict = yaml.safe_load(fp)

        if remote_payload_received:
            remote_config_dict = json.loads(config_payload)
            # print(remote_config_dict)

            # remote payload was succesfully received, so copy mqtt settings to locally sourced dict
            config_dict["mqtt_hostname"] = mqtt_settings.host
            config_dict["mqtt_port"] = mqtt_settings.port
            config_dict["mqtt_username"] = mqtt_settings.username
            config_dict["mqtt_password"] = mqtt_settings.password
            config_dict["mqtt_root"] = root_topic

        config_dict = ManagerConfig._parse_remote_config(remote_config_dict, config_dict)

        # dump adapted config
        with open(local_config_file, "w") as fp:
            yaml.dump(config_dict, fp)

        return ManagerConfig(config_dict)

    def distancing_parameters_invalid(self):
        invalid = False

        if len(self.tags + self.anchors) >= self.nb_slots:
            print("ERROR: Too many tags and anchors were given for the available number of slots.")
            invalid = True

        return invalid

    def positioning_parameters_invalid(self):
        invalid = False

        nb_anchors = len(self.anchors)
        if nb_anchors < 3:
            print("ERROR: A minimum of 3 anchors is needed for positioning. Only {} was/were given.".format(nb_anchors))
            invalid = True

        return invalid

    def is_complete(self):
        return self.config_complete

    @staticmethod
    def _parse_remote_config(remote_config, local_config):
        # parse anchors
        try:
            anchors_dict = remote_config["devices"]["anchors"]

            anchors = list(anchors_dict.keys())
            anchors_int = [int(anchor) for anchor in anchors]

            local_config["anchors"] = anchors_int
            local_config["anchor_positions"] = {}

            for anchor in anchors:
                x = float(remote_config["devices"]["anchors"][anchor]["x"])
                y = float(remote_config["devices"]["anchors"][anchor]["y"])
                z = 0.0

                local_config["anchor_positions"][int(anchor)] = [x, y, z]
        except KeyError:
            pass

        # parse other characteristics
        pass

        return local_config
