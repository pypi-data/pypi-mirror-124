# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['worktory',
 'worktory.connection',
 'worktory.connection.wrappers',
 'worktory.device',
 'worktory.inventory',
 'worktory.parsers',
 'worktory.parsers.wrappers']

package_data = \
{'': ['*']}

install_requires = \
['asyncssh>=2.7.2,<3.0.0',
 'genie>=21.7,<22.0',
 'netmiko>=3.4.0,<4.0.0',
 'ntc-templates>=2.3.2,<3.0.0',
 'pyats>=21.7,<22.0',
 'scrapli-community>=2021.7.30,<2022.0.0',
 'scrapli[ssh2]>=2021.7.30,<2022.0.0']

setup_kwargs = {
    'name': 'worktory',
    'version': '0.1.0',
    'description': 'Network Automation Inventory',
    'long_description': 'Welcome to Worktory\'s documentation!\n====================================\n\nWorktory is a python library created with the single purpose of simplifying the inventory management of network automation scripts.\n\nAs the network automation ecosystem grows, several connection plugins and parsers are available, and several times choosing a library or a connection plugin restricts all the devices to the same connection method.\n\nWorktory tries to solve that problem giving the developer total flexibility for choosing the connector plugin and parsers for each device, at the same time that exposes a single interface for every plugin.\n\nInstalling \n-----------------------------\n\nWorktory is available in PyPI, to install run: ::\n\n   $ pip install worktory\n   \nUsing worktory\n=======================\n\nSample Inventory\n--------------------------\n\n.. code-block:: python \n\n    devices = [\n                {\n                \'name\': \'sandbox-iosxr-1\',\n                \'hostname\': \'sandbox-iosxr-1.cisco.com\',\n                \'platform\': \'cisco_iosxr\',\n                \'username\': \'admin\',\n                \'password\': \'C1sco12345\',\n                \'groups\': [\'CORE\'],\n                \'connection_manager\': \'scrapli\',\n                \'select_parsers\' : \'genie\',\n                \'mode\': \'async\',\n                \'transport\': \'asyncssh\',\n                },\n                {\n                \'name\': \'sandbox-nxos-1\',\n                \'hostname\': \'sandbox-nxos-1.cisco.com\',\n                \'platform\': \'cisco_nxos\',\n                \'username\': \'admin\',\n                \'password\': \'Admin_1234!\',\n                \'groups\': [\'CORE\'],\n                \'select_parsers\' : \'ntc\',\n                \'connection_manager\': \'scrapli\',\n                \'mode\': \'async\',\n                \'transport\': \'asyncssh\'\n                },\n                {\n                \'name\': \'sandbox-nxos-2\',\n                \'hostname\': \'sandbox-nxos-1.cisco.com\',\n                \'platform\': \'nxos\',\n                \'username\': \'admin\',\n                \'password\': \'Admin_1234!\',\n                \'groups\': [\'EDGE\'],\n                \'connection_manager\': \'unicon\',\n                \'mode\': \'sync\',\n                \'transport\': \'ssh\',\n                \'GRACEFUL_DISCONNECT_WAIT_SEC\': 0,\n                \'POST_DISCONNECT_WAIT_SEC\': 0,\n                },\n                {\n                \'name\': \'sandbox-iosxr-2\',\n                \'hostname\': \'sandbox-iosxr-1.cisco.com\',\n                \'platform\': \'cisco_iosxr\',\n                \'username\': \'admin\',\n                \'password\': \'C1sco12345\',\n                \'groups\': [\'CORE\'],\n                \'connection_manager\': \'scrapli\',\n                \'select_parsers\' : \'genie\',\n                \'mode\': \'sync\',\n                },\n            ]\n\nCollecting Running config from async devices\n-------------------------------------------------------\n\n.. code-block:: python \n\n    from worktory import InventoryManager\n    import asyncio\n    inventory = InventoryManager(devices)\n\n    device_configs = {}\n    async def get_config(device):\n        await device.connect()\n        config = await device.execute("show running-config")\n        device_configs[device.name] = config\n        await device.disconnect()\n\n    async def async_main():\n        coros = [get_config(device) for device in inventory.filter(mode=\'async\')]\n        await asyncio.gather(*coros)\n\n    loop = asyncio.get_event_loop()\n    loop.run_until_complete(async_main())\n\n\nCollecting Running config from sync devices\n-------------------------------------------------------\n\n.. code-block:: python \n\n    from worktory import InventoryManager\n    from multiprocessing import Pool\n    inventory = InventoryManager(devices)\n\n    def get_config(device_name):\n        inventory = InventoryManager(devices)\n        device = inventory.devices[device_name]\n        device.connect()\n        config = device.execute("show running-config")\n        device.disconnect()\n        return ( device.name , config )\n\n    def main():\n        devs = [device.name for device in inventory.filter(mode=\'sync\')]\n        with Pool(2) as p:\n            return p.map(get_config, devs)\n\n    \n    output = main()\n',
    'author': 'Renato Almeida de Oliveira',
    'author_email': 'renato.almeida.oliveira@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/renatoalmeidaoliveira/Worktory',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
