#!/usr/bin/env python3
# Copyright 2020 Ubuntu
# See LICENSE file for licensing details.

import logging
import subprocess

from ops.charm import CharmBase
from ops.main import main
from ops.framework import StoredState
from ops.model import (
    ActiveStatus,
    MaintenanceStatus,
)

logger = logging.getLogger(__name__)


class MachineCharm(CharmBase):
    _stored = StoredState()

    def __init__(self, *args):
        super().__init__(*args)
        self.framework.observe(self.on.install, self._on_install)
        self.framework.observe(self.on.start, self._on_start)
        self.framework.observe(self.on.prometheus_relation_changed, self._provide_info)

    def _on_install(self, _):
        self.unit.status = MaintenanceStatus("Installing prometheus")
        subprocess.run(["snap", "install", "prometheus"])

    def _on_start(self, _):
        self.unit.status = MaintenanceStatus("Starting prometheus")
        subprocess.run(["service", "snap.prometheus.prometheus", "start"])
        self.unit.status = ActiveStatus("Prometheus started")

    def _provide_info(self, event):
        self.unit.status = MaintenanceStatus("Sending prometheus information")
        event.relation.data[self.unit]["ip"] = "fake_ip"
        self.unit.status = ActiveStatus("Information sent")

if __name__ == "__main__":
    main(MachineCharm)
