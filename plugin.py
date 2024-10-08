#############################################################################
# Copyright (C) 2024 CrowdWare
#
# This file is part of EbookCreator.
#
#  EbookCreator is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  EbookCreator is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with EbookCreator.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################


class Plugins:
    generator_plugins = {}
    
    def __init__(self):
        pass

    @staticmethod
    def generatorPluginNames():
        return Plugins.generator_plugins.keys()

    @staticmethod
    def addGeneratorPlugin(name, plugin):
        Plugins.generator_plugins[name] = plugin

    @staticmethod
    def getGeneratorPlugin(name):
        return Plugins.generator_plugins[name]