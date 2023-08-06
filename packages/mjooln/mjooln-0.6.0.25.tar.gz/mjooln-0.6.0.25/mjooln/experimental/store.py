from mjooln import *


class Store:
    _folder = HOME / 'store'
    _extension = 'txt'
    _is_compressed = False
    _is_encrypted = False
    _type = None

    @classmethod
    def file(cls, key):
        key = Key.glass(key)
        type = cls._type if cls._type is not None else key.first()
        return File.make(folder=cls._folder.append(type),
                         stub=key.seed(),
                         extension=cls._extension,
                         is_compressed=cls._is_compressed,
                         is_encrypted=cls._is_encrypted)

    @classmethod
    def exists(cls, key):
        return cls.file(key).exists()

    @classmethod
    def get(cls, key, crypt_key=None, password=None):
        file = cls.file(key)
        return file.read(mode='rt',
                         crypt_key=crypt_key,
                         password=password)

    @classmethod
    def put(cls, key, data, crypt_key=None, password=None):
        file = cls.file(key)
        file.write(data=data,
                   mode='wt',
                   crypt_key=crypt_key,
                   password=password)


class DocStore(Store):
    _folder = Store._folder.append('doc')
    _extension = 'json'

    @classmethod
    def get(cls, key, crypt_key=None, password=None):
        file = cls.file(key)
        return file.read_json(crypt_key=crypt_key,
                              password=password)

    @classmethod
    def put(cls, key, data, crypt_key=None, password=None):
        file = cls.file(key)
        file.write_json(data=data,
                        password=password,
                        crypt_key=crypt_key)


class ConfigStore(Store):
    _folder = Store._folder.append('config')
    _extension = 'yaml'

    @classmethod
    def get(cls, key, crypt_key=None, password=None):
        file = cls.file(key)
        return file.read_yaml(crypt_key=crypt_key,
                              password=password)

    @classmethod
    def put(cls, key, data, crypt_key=None, password=None):
        file = cls.file(key)
        file.write_yaml(data=data,
                        password=password,
                        crypt_key=crypt_key)


class CryptKeyStore(Store):
    _folder = Store._folder.append('crypt_key')
    _extension = 'txt'
    _is_encrypted = True
    _is_compressed = True
