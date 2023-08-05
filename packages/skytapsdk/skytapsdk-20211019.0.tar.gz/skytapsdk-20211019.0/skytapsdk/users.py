from restfly.endpoint import APIEndpoint


class Users(APIEndpoint):
    _path = "users"

    def list(self):
        """GET action on 'users' API for a specific user ID"""
        return self._get().json()

    def get_user(self, uid: int):
        _path = f"{self._path}/{uid}"
        return self._get().json()
