import json
import pathlib
import re
from handlers.DebugHandlers import (print_debug, pprint_debug)

def _parse_project_godot(s, config_key="name"):
    main_regex = r"config\/"+config_key+r"=\"(.*?)\""
    result = re.findall(main_regex, s)
    if len(result) > 0:
        return result[0]
    else:
        return "N/A"

class ProjectHandler:
    def __init__(self):
        self.categories = {}
        self.selected_categories = []
        #load config
        self._config = self.config_load(pathlib.Path("./config.json"))
        self.projects_dir = pathlib.Path(self._config["projectsDir"])
        #check if projects.json is not generated
        project_json_dir = pathlib.Path(self._config["saveProjectsDir"])
        self.project_data = {}
        if project_json_dir.exists():
            ##load json
            with open(project_json_dir, "r", encoding="utf-8") as f:
                self.project_data = json.loads(f.read())
            #load categories
            self.selected_categories = self.project_data["last_categories"]
            self.categories = self.project_data["definitions"]["categories"]
            missing_projects = set(self._get_valid_projects()) - set(list(self.project_data["projects"].keys()))
            for project in missing_projects:
                self.project_data["projects"].update({
                    project: {
                        "categories": [],
                        "favorite": False
                    }
                })
            self.save_projects_json()
        else:
            self.project_data = self.create_first_json(self._get_valid_projects())
        invalid_keys = []
        for key in self.project_data["projects"].keys():
            tmp_val = ""
            tmp_image_path = ""
            path = pathlib.Path(key)
            if path.exists():
                with open(key, "r", encoding="utf-8") as f:
                    data = f.read()
                    tmp_val = _parse_project_godot(data)
                    tmp_image_path = _parse_project_godot(data, "icon")
                tmp_image_path = path.parent / tmp_image_path.split("res://")[1]
                tmp_image_path = str(tmp_image_path)
                self.project_data["projects"][key].update({"name": tmp_val, "icon": tmp_image_path})
            else:
                invalid_keys += [key]
        #delete invalid keys - probably deleted from drive
        for key in invalid_keys:
            self.project_data["projects"].pop(key)
        pprint_debug(self.project_data)

    def _get_valid_projects(self):
        valid_projects = self.projects_dir.glob("*/project.godot")
        valid_projects = [str(project) for project in valid_projects]
        return valid_projects

    def config_load(self, path):
        data = ""
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
        return json.loads(data)

    def save_projects_json(self):
        self.project_data["definitions"]["categories"] = self.categories
        self.project_data["last_categories"] = self.selected_categories
        with open(self._config["saveProjectsDir"], "w", encoding="utf-8") as f:
            f.write(json.dumps(self.project_data, indent=4))

    def create_first_json(self, valid_projects):
        output_dict = {}
        for project in valid_projects:
            output_dict.update({
                project: {
                    "categories": [],
                    "favorite": False
                }
            })
        output_dict = {
            "last_categories": [],
            "definitions": {
                "categories": {},
            },
            "projects": output_dict
        }
        pprint_debug(output_dict)
        with open(self._config["saveProjectsDir"], "w", encoding="utf-8") as f:
            f.write(json.dumps(output_dict, indent=4))
        return output_dict

    def get_filtered_projects(self, categories):
        tmp_projects = {}
        if len(categories) == 0:
            return self.project_data["projects"]
        for key in self.project_data["projects"].keys():
            item = self.project_data["projects"][key]
            if not(set(categories) <= set(item["categories"])):
                continue
            tmp_projects.update({key: item})
        return tmp_projects