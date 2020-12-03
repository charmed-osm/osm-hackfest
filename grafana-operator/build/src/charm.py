#!/usr/bin/env python3
# Copyright 2020 Ubuntu
# See LICENSE file for licensing details.

import logging

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import ActiveStatus, MaintenanceStatus

logger = logging.getLogger(__name__)


class GrafanaCharm(CharmBase):
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.config_changed, self.configure_pod)
        self.framework.observe(
            self.on.prometheus_relation_changed, self.get_prometheus_info
        )

    def get_prometheus_info(self, event):
        ip = event.relation.data[event.unit].get("ip")
        self.unit.status = ActiveStatus(f"Prometheus relation data: ip={ip}")

    def configure_pod(self, _):
        if not self.unit.is_leader():
            self.unit.status = ActiveStatus()
            return
        self.unit.status = MaintenanceStatus("Building pod spec")
        tag = "latest"
        spec = {
            "version": 3,
            "containers": [
                {
                    "name": self.framework.model.app.name,
                    "image": f'grafana/grafana:{tag}',
                    "ports": [
                        {
                            "name": "port",
                            "containerPort": 3000,
                            "protocol": "TCP",
                        }
                    ],
                }
            ],
        }
        self.model.pod.set_spec(spec)
        self.unit.status = ActiveStatus("Pod started")


if __name__ == "__main__":
    main(GrafanaCharm)
