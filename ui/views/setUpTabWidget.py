import logging

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QGroupBox,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

from config import BLOCK_ADDRESS, BLOCK_PORT, BLOCK_CTRL_DEV, BLOCK_BIAS_DEV, VNA_ADDRESS, VNA_TEST_MAP
from interactors.block import Block
from interactors.vna import VNABlock

logger = logging.getLogger(__name__)


class SetUpTabWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)
        self.createGroupBlock()
        self.createGroupVna()
        self.layout.addWidget(self.groupBlock)
        self.layout.addWidget(self.groupVna)
        self.setLayout(self.layout)

    def createGroupBlock(self):
        self.groupBlock = QGroupBox("Block config")
        layout = QGridLayout()

        self.vnaIPLabel = QLabel(self)
        self.vnaIPLabel.setText("Block IP:")
        self.vna_ip = QLineEdit(self)
        self.vna_ip.setText(BLOCK_ADDRESS)

        self.blockPortLabel = QLabel(self)
        self.blockPortLabel.setText("Block Port:")
        self.block_port = QLineEdit(self)
        self.block_port.setText(str(BLOCK_PORT))

        self.ctrlDevLabel = QLabel(self)
        self.biasDevLabel = QLabel(self)
        self.ctrlDev = QLineEdit(self)
        self.biasDev = QLineEdit(self)
        self.ctrlDevLabel.setText("CTRL Device:")
        self.biasDevLabel.setText("BIAS Device:")
        self.ctrlDev.setText(BLOCK_CTRL_DEV)
        self.biasDev.setText(BLOCK_BIAS_DEV)

        self.btnCheckBlock = QPushButton("Check Block")
        self.btnCheckBlock.clicked.connect(self.check_block)

        layout.addWidget(self.vnaIPLabel, 1, 0)
        layout.addWidget(self.vna_ip, 1, 1)
        layout.addWidget(self.blockPortLabel, 2, 0)
        layout.addWidget(self.block_port, 2, 1)
        layout.addWidget(self.ctrlDevLabel, 3, 0)
        layout.addWidget(self.ctrlDev, 3, 1)
        layout.addWidget(self.biasDevLabel, 4, 0)
        layout.addWidget(self.biasDev, 4, 1)
        layout.addWidget(self.btnCheckBlock, 5, 0, 1, 2)

        self.groupBlock.setLayout(layout)

    def createGroupVna(self):
        self.groupVna = QGroupBox("VNA config")
        layout = QGridLayout()

        self.vnaIPLabel = QLabel(self)
        self.vnaIPLabel.setText("VNA IP:")
        self.vna_ip = QLineEdit(self)
        self.vna_ip.setText(VNA_ADDRESS)

        self.vnaStatusLabel = QLabel(self)
        self.vnaStatusLabel.setText("VNA status:")
        self.vnaStatus = QLabel(self)
        self.vnaStatus.setText("VNA is not checked yet!")

        self.btnCheckVna = QPushButton("Test VNA")
        self.btnCheckVna.clicked.connect(self.check_vna)

        layout.addWidget(self.vnaIPLabel, 1, 0)
        layout.addWidget(self.vna_ip, 1, 1)
        layout.addWidget(self.vnaStatusLabel, 2, 0)
        layout.addWidget(self.vnaStatus, 2, 1)
        layout.addWidget(self.btnCheckVna, 3, 0, 1, 2)

        self.groupVna.setLayout(layout)

    def check_block(self):
        block = Block()
        block.update(host=self.vna_ip.text(), port=self.block_port.text())
        result = block.get_bias_data()
        logger.info(f"Health check SIS block {result}")

    def check_vna(self):
        vna = VNABlock()
        result = vna.test()
        self.vnaStatus.setText(VNA_TEST_MAP.get(result, "Error"))
