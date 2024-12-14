from multipledispatch import dispatch
import xml.etree.ElementTree as ET

from app.maze_solution import MazeSolution
from app.utilities import call_command

class Solver:
    @dispatch(str, str, bool)
    def __init__(self, name, command, checked):
        self.name = name
        self.command = command
        self.checked = checked

    @dispatch(ET.Element)
    def __init__(self, xml_config_tree_root):
        self.load(xml_config_tree_root)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if type(name) != str:
            raise ValueError("Name must be string")
        if len(name) == 0:
            raise ValueError("Name can't be empty string")
        self._name = name

    @property
    def command(self):
        return self._command

    @command.setter
    def command(self, command):
        if type(command) != str:
            raise ValueError("Command must be string")
        if len(command) == 0:
            raise ValueError("Command can't be empty string")
        self._command = command

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, checked):
        if type(checked) != bool:
            raise ValueError("Checked must be boolean")
        self._checked = checked

    def load(self, xml_config_tree_root):
        self.name = xml_config_tree_root.find("name").text
        self.command = xml_config_tree_root.find("command").text
        self.checked = (xml_config_tree_root.find("checked").text == "True")

    def save(self, xml_config_tree_root):
        ET.SubElement(xml_config_tree_root, "name").text = self.name
        ET.SubElement(xml_config_tree_root, "command").text = self.command
        if self.checked:
            ET.SubElement(xml_config_tree_root, "checked").text = "True"
        else:
            ET.SubElement(xml_config_tree_root, "checked").text = "False"

    def run(self, maze):
        output_frame = call_command(self.command, maze.get_frame_for_solver())
        solution = MazeSolution(output_frame)
        return solution