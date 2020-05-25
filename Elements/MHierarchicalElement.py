class MHierarchicalElement:
    def __init__(self, content=None):
        super().__init__()

        self.child_containers = []
        self.parent_container = None
        self.uid = None
    # def get_content(self, *args):
    #     raise NotImplementedError("MContainer derivatives must implement get_content")
    #
    # def set_content(self, *args):
    #     raise NotImplementedError("MContainer derivatives must implement set_content")

    def get_uid(self):
        return self.uid

    def set_uid(self, uid):
        self.uid = uid

    def get_parent_he(self):
        return self.parent_container

    def get_child_he(self):
        return self.child_containers

    def set_parent_he(self, new_parent_window):

        # Remove self from old parent
        if self.parent_container is not None:
            self.parent_container._remove_child_he(self)

        # Add self to new parent
        if(new_parent_window is not None):
            new_parent_window._add_child_he(self)

        # Set local reference to parent
        self.parent_container = new_parent_window

    def _remove_child_he(self, child_window):
        self.child_containers.remove(child_window)

    def _add_child_he(self, child_window):
        self.child_containers.append(child_window)

