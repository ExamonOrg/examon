import logging


class SettingsManager:
    def __init__(self, content_mode=None, file_mode=None,
                 packages=None, active_packages=None,
                 mongodb_config=None):
        self.packages = [] if packages is None else packages
        self.active_packages = [] if active_packages is None else active_packages
        self.content_mode = content_mode
        self.file_mode = file_mode
        self.mongodb_config = mongodb_config

    def reset(self):
        self.packages = []
        self.active_packages = []

    def add_mongodb_config(self, domain: str, protocol: str, user: str, password: str):
        self.mongodb_config = {
            "domain": domain,
            "protocol": protocol,
            "user": user,
            "password": password
        }

    def add(self, package_name: str, url: str = None) -> None:
        if package_name is None or package_name == "":
            logging.debug("Cannot add package not specified")
            return

        data = {"name": package_name}
        if url:
            data |= {"url": url}

        if package_name not in [package["name"] for package in self.packages]:
            self.packages.append(data)

    def add_active(self, package: str):
        if package not in self.active_packages:
            self.active_packages.append(package)

    def remove(self, package: str) -> None:
        index = next(
            (index for (index, d) in enumerate(self.packages) if d["name"] == package),
            None,
        )
        logging.debug(f"Removing package {package}")
        if index is not None:
            del self.packages[index]
        self.remove_active(package)

    def remove_active(self, package: str):
        if package in self.active_packages:
            self.active_packages.remove(package)

    def mongodb_uri(self) -> str:
        return f"{self.mongodb_config['protocol']}://{self.mongodb_config['user']}:" \
               f"{self.mongodb_config['password']}@{self.mongodb_config['domain']}/?retryWrites=true&w=majority"

    def as_dict(self) -> dict:
        config = {
            "content_mode": self.content_mode,
            "file_mode": self.file_mode,
            "packages": {"all": self.packages, "active": self.active_packages},
        }
        if self.mongodb_config is not None:
            config['mongodb_config'] = self.mongodb_config

        return config
