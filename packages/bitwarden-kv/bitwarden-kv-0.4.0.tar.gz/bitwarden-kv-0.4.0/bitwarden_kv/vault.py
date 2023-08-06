import os
import json
import logging
import subprocess
import typing as t

# Setup logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - BitWarden KeyVault: %(message)s')


class BitWardenKeyVault(object):
    _bw_errors = {
        'ALREADY_LOGGED': 'You are already logged in as',
        'DUPLICATES': 'More than one result was found'
    }
    
    def __init__(
        self,
        namespace_name: t.Optional[str] = None,
        cache_namespaces: bool = False
    ) -> None:
        # Namespaces
        self.namespace_name = namespace_name
        self.cache_namespaces = cache_namespaces
        self.namespace_cache = {}
        
        # Credentials
        self.EMAIL = os.getenv('BW_EMAIL', '')
        self.PASSWORD = os.getenv('BW_PASSWORD', '')
        self.CLIENT_SECRET = os.getenv('BW_CLIENT_SECRET', '')
        self.SESSION_ID = None

    def bw_cli(self, *args: t.List[str], input: str = '') -> t.Tuple[str, str]:
        cli_args = self.bw_args(*args)
        try:
            result = subprocess.run(cli_args, input=input.encode('utf-8'), capture_output=True)
                
            logging.debug(result.stdout.decode('utf-8'))
            logging.debug(result.stderr.decode('utf-8'))
            
            if result.stderr and '\\x1b' not in str(result.stderr): 
                logging.warning(result.stderr.decode('utf-8'))
            
            return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
        except Exception as exc:
            logging.warning(exc)

    def bw_args(self, *args: t.List[str]) -> t.List[str]:
        cli_args = ['bw', '--raw']
        
        if self.SESSION_ID:
            cli_args += ['--session', self.SESSION_ID]
        
        return cli_args + list(args)

    def login(self) -> bool:
        bw_args = ['login', self.EMAIL, self.PASSWORD]
        
        _, err = self.bw_cli(*bw_args, input=self.CLIENT_SECRET)
        
        if self._bw_errors['ALREADY_LOGGED'] in err and self.EMAIL not in err:
            logging.error('You are logged in BitWarden with the wrong user')
            return False
            
        self.sync_vault()
        self.unlock_vault()

        return True

    def get_object(self, key: str, namespace_name: t.Optional[str] = None) -> t.Optional[dict]:
        namespace_str = self.namespace_cache.get(namespace_name) or self.is_namespace_exists(namespace_name or self.namespace_name)
       
        if namespace_str:
            namespace = json.loads(namespace_str)

            bw_args = ['list', 'items', '--search', key]
            key_search_result_str, err = self.bw_cli(*bw_args, input=self.PASSWORD)
            
            if err:
                return None

            if key_search_result_str:
                key_search_result = json.loads(key_search_result_str)
                key_result =  [
                    {'key': note['name'], 'value': note['notes']}
                    for note in key_search_result
                    if note['folderId'] == namespace['id'] and note['name'] == key
                ]
                
                if key_result:
                    return key_result[0]
                else:
                    return None

        return None

    def is_namespace_exists(self, namespace_name: str) -> t.Optional[str]:
        bw_args = ['get', 'folder', namespace_name]
        
        namespace, err = self.bw_cli(*bw_args, input=self.PASSWORD)
        
        if self._bw_errors['DUPLICATES'] in err:
            logging.warning('Several identical folders. Delete or rename one of them.')
            return None
        else:
            if self.cache_namespaces and namespace_name not in self.namespace_cache:
                self.namespace_cache[namespace_name] = namespace
            
            return namespace
    
    def sync_vault(self) -> bool:
        bw_args = ['sync']
        
        self.bw_cli(*bw_args, input=self.PASSWORD)
        logging.info('The key vault is synchronized')
        
        return True
    
    def unlock_vault(self) -> bool:
        bw_args = ['unlock', '--passwordenv', 'BW_PASSWORD']
        
        res, err = self.bw_cli(*bw_args)
        
        if err:
            return False
        
        self.SESSION_ID = f'"{res}"'
        logging.info('The key vault is unlocked')

        return True
