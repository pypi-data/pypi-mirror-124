# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['sqlalchemy_neo4j']

package_data = \
{'': ['*']}

install_requires = \
['sqlalchemy>=1.0,<1.4']

setup_kwargs = {
    'name': 'sqlalchemy-neo4j',
    'version': '0.1.dev0',
    'description': 'SQL Alchemy dialect for Neo4j',
    'long_description': '# SQL Alchemy dialect for Neo4j\n\nThis package provides the SQL dialect for Neo4j, using the official JDBC driver (the Neo4j "BI Connector" )\n\n## Installation\n```bash\npip install sqlalchemy-neo4j\n```\n\n## Prerequisites\n- Java 8 / 11\n- Download the [Neo4j BI Connector](https://neo4j.com/bi-connector/)\n  > The reason the JAR is not included in the package is due to licensing concerns. I may add the jar into the bundle in the future.\n- Add the jar to the classpath, either directly via the ``CLASSPATH`` environment variable or while initializing the JVM\n  > You can also use the ``NEOJDBC_WARMUP`` environment variable, which will ensure we reuse an existing jpype instance or create a new one ( with default parameters )\n\n\n## Getting started \n```python\n\nfrom sqlalchemy import create_engine\nfrom \n\n# This happens automatically if you set the NEOJDBC_WARMUP environment variable\njpype.startJVM()\n\neng = create_engine("neo4j+jdbc://neo4j-neo4j:7687/neo4j?UID=neo4j&PWD=QUOTED_PASSWORD&LogLevel=6&StrictlyUseBoltScheme=false")\n\nexecute = engine.execute("select * from Node.YOUR_NODE limit 1")\nrows = execute.fetchall()\nfor row in rows:\n    print(row)\n```\n\nSee more [examples](./examples/)\n\n\n## Related projects\n* [Neo4j Metabase Driver](https://github.com/bbenzikry/metabase-neo4j-driver) - Use Neo4j with Metabase. Use both SQL and Cypher ( the driver uses the same underlying BI connector for SQL queries )\n* [Superset Neo4j Support ( WIP )]() - based on this dialect\n\n## Future\n- Add Cypher support\n- Add support for Cypher views in JDBC driver\n\n\n\n\n',
    'author': 'Beni Ben Zikry',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/bbenzikry/sqlalchemy-neo4j',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
