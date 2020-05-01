class MContainer:
    def __init__(self):
        super().__init__()

        self.child_containers = []
        self.parent_container = None

    def get_parent_container(self):
        return self.parent_container

    def get_child_container(self):
        return self.child_containers

    def set_parent_container(self, new_parent_window):
        # Remove self from old parent
        if self.parent_container is not None:
            self.parent_container._remove_child_container(self)

        # Add self to new parent
        if(new_parent_window is not None):
            new_parent_window._add_child_container(self)

        # Set local reference to parent
        self.parent_container = new_parent_window

    def _remove_child_container(self, child_window):
        self.child_containers.remove(child_window)

    def _add_child_container(self, child_window):
        self.child_containers.append(child_window)

