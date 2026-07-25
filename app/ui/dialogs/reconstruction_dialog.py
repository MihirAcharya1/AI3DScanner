from PySide6.QtWidgets import QMessageBox


class ReconstructionDialog:

    @staticmethod
    def finished(filename):

        QMessageBox.information(
            None,
            "AI3DScanner",
            f"Reconstruction completed.\n\nSaved to:\n{filename}",
        )