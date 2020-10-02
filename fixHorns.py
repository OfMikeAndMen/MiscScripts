import os
import xml.etree.ElementTree as et

class CommentedTreeBuilder(et.TreeBuilder):
    def comment(self, data):
        self.start(et.Comment, {})
        self.data(data)
        self.end(et.Comment)

parser = et.XMLParser(target=CommentedTreeBuilder())

# get all Honks from sultan2
honks = []
for item in et.parse("./sultan2/carcols.meta").getroot().find("Kits").find("Item").find("statMods").findall("Item"):
    if item.find("type").text == "VMT_HORN":
        honks.append(item)

# find all carcols.meta files in subdirectories
for (dirpath, dirnames, filenames) in os.walk("./"):
    if "carcols.meta" in filenames:

        # read xml
        tree = et.parse(dirpath + "/carcols.meta", et.XMLParser(target=CommentedTreeBuilder()))
        root = tree.getroot()

        # check if statmods exist
        try:
            stats = root.find("Kits").find("Item").find("statMods")

            # find all horns and remove them
            for item in stats.findall("Item"):
                if item.find("type").text == "VMT_HORN":
                    stats.remove(item)

            # append all sultan2 honks
            for honk in honks:
                stats.append(honk)

            # save file
            tree.write(dirpath + "/carcols.meta", encoding="UTF-8", xml_declaration=True)
            print(dirpath + "/carcols.meta - done")

        except AttributeError:
            print(dirpath + "/carcols.meta - statMods doesn't exist")
    else:
        print(dirpath + "/carcols.meta doesnt exist")
