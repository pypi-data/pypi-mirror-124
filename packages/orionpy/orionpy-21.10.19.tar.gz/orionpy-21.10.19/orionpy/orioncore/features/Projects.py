# coding=utf-8

# =============================================================================
# IMPORTS
# =============================================================================

from .Items import Items
from .Project import Project

# =============================================================================
# CLASS
# =============================================================================


class Projects(Items):
    def __init__(self):
        super().__init__("Document Link", "aob_project", lambda data: Project(data))

    def add_item(self, owner, title, text, snippet=None, app_id=None):
        """
        Add a project in aob
        :param title: title of the project
        :param text: content for the project
        :param snippet:
        :return: result of the query (a boolean for "success", the id of the project and the id of the folder)
        """
        tags = self.tags
        if app_id:
            tags = ",aob_appId_" + app_id
        url = self.url_manager.add_item_feature_url(self.type, owner)
        data = {
            "title": title,
            "snippet": snippet,
            "text": text,
            "type": self.type,
            "tags": tags,
        }
        req = self.request.post(url, data).json()
        self._verify(
            req,
            'Item "' + str(title) + '" was added successfully.\nitemId : ' + str(req.get("id")),
            'WARNING : Item "' + str(title) + '" was NOT added successfully',
        )
        return req

    def update_item(self, item_id, title, text, snippet=None):
        """
        Update a project in aob
        :param itemId: id of the project you want to update
        :param title: new title of the project
        :param text: content for the project to be updated
        :param snippet:
        :return: result of the query (a boolean for "success" and the id of the project)
        """
        url = self.url_manager.update_item_feature_url(
            self.type, self._get_owner_from_id(item_id), item_id
        )
        json_search = self.search(q="id:" + item_id)
        json_url = json_search[0].get("url")
        data = {
            "title": title,
            "snippet": snippet,
            "text": text,
            "type": self.type,
            "tags": self.tags_complement,
            "url": json_url,
        }
        req = self.request.post(url, data).json()
        self._verify(
            req,
            'Item with id: "' + item_id + '" was updated successfully\nTitle : ' + title,
            'WARNING : Item with id: "' + item_id + '" was NOT updated successfully',
        )
        return req
