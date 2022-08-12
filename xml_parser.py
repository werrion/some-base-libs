import xmltodict
import os
from pathlib import Path

"""
Use case:
    # get data from quests.xml
    quests_raw_data = XmlParser(file_name='quests.xml', root_key='root', path=Path(os.getcwd()))
    ALL_QUESTS_ID_FROM_XML = quests_raw_data.create_named_dict(key_group_data='tree', key_data='o')['o']
    
    quests_raw_data.create_named_dict - form a dictionary from the specified section in such a way as to form
    from the line <o id="10081" parent_id="0" name="House_On_Reef_Quest_0" icon_factory_id="176113" >
    row like  {"10081": [{id="10081" parent_id="0" name="House_On_Reef_Quest_0" icon_factory_id="176113"}]}

    if there will be dubbing id: 
    <o id="10081" parent_id="0" name="House_On_Reef_Quest_0" icon_factory_id="176113" >
    <o id="10081" parent_id="21341" name="Reef_Quest_8" icon_factory_id="67688999" >
    we get value:
    {"10081": [{id="10081" parent_id="0" name="House_On_Reef_Quest_0" icon_factory_id="176113"}, 
               {id="10081" parent_id="21341" name="Reef_Quest_8" icon_factory_id="67688999"}]}
"""


class XmlParser:

    def __init__(self, file_name, root_key, path=None):
        """
        Read xml file like dict
        :param file_name: xml file name - string
        :param root_key: root key - string
        :param path: path to xml folder - string or path
        """
        self.path = path
        self.root_key = root_key
        self.file_name = file_name
        if path is None:
            self.path = Path(os.getcwd())

        # create dict from xml data
        self.xm_file_path = self.path / Path(self.file_name)
        with open(self.xm_file_path, encoding="utf8") as xml_data:
            data = xml_data.read()
            self.xml_dict = xmltodict.parse(data)

    # formate dict from xml to dict type - id: value(id: **, data1: ** ... )
    # and if one ID have more than one string - convert like list of data in value
    def create_named_dict(self, key_data, key_group_data=None):
        initial_dict = {}
        if key_group_data is not None:
            initial_dict = self.xml_dict[self.root_key][key_group_data][key_data]
        if key_group_data is None:
            initial_dict = self.xml_dict[self.root_key][key_data]

        id_name = list(initial_dict[0].keys())[0]

        temp_props_dict = {}
        list_one_elem = []
        id_last_item = ''

        for award in initial_dict:
            if award[id_name] == id_last_item:
                # check for not last element
                if award != initial_dict[-1]:
                    list_one_elem.append(award)
                # if last add it to dict
                else:
                    list_one_elem.append(award)
                    temp_props_dict[f"{id_last_item}"] = list_one_elem
            else:
                if len(list_one_elem) > 0:
                    temp_props_dict[f"{id_last_item}"] = list_one_elem
                    list_one_elem = []

                # check for existed key in our dict (when add old award in end of doc)
                if temp_props_dict.get(award[id_name]) is None:
                    id_last_item = award[id_name]
                    list_one_elem.append(award)
                else:
                    data_existed_key = temp_props_dict.get(award[id_name])
                    data_existed_key.append(award)
                    id_last_item = award[id_name]
                    list_one_elem.extend(data_existed_key)
        if list_one_elem != initial_dict[-1]:
            temp_props_dict[f"{id_last_item}"] = list_one_elem

        dict_final = dict()
        dict_final[key_data] = temp_props_dict
        return dict_final
