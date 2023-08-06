# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['redasql']

package_data = \
{'': ['*']}

install_requires = \
['prettytable>=2.2.0,<3.0.0',
 'prompt-toolkit>=3.0.20,<4.0.0',
 'requests>=2.26.0,<3.0.0']

entry_points = \
{'console_scripts': ['redasql = redasql.command:main']}

setup_kwargs = {
    'name': 'redasql',
    'version': '0.1.0.1',
    'description': '',
    'long_description': '# RedaSQL\n![redasql](https://user-images.githubusercontent.com/4572217/138585742-dc82c105-8f43-46f4-a611-27fe49577a5b.png)\n\n\nRedaSQL is querying tool for redash.\nI like `psql`(PostgreSQL CLI). so redasql resemble psql in some respects.\n\n## Install\n\n```bash\npip install redasql\n```\n\n## How To Use\n\nredasql need some arguments or environment variables.\nredasql prioritizes arguments over environment variables.\n\n\n|argument|env|mean|required|\n|---|---|---|---|\n|-k/--api-key|REDASQL_REDASH_APIKEY|API KEY(user api key)|True|\n|-s/--server-host|REDASQL_REDASH_ENDPOINT|Redash server hostname. ex) https://your.redash.server.host/|True|\n|-p/--proxy|REDASQL_HTTP_PROXY|if your redash server restricted by Proxy, set url format. ex)http://user:pass@your.proxy.server:proxy-port|False|\n|-d/--data-source||initial connect datasource name.|False|\n\nif you want to use redasql with direnv, rename `.envrc.sample` to `.envrc` and set attributes.\n\n### special commands\n\nredasql has management commands.\n\n```\n\\?: HELP META COMMANDS.\n\\d: DESCRIBE TABLE\n\\c: SELECT DATASOURCE.\n\\x: QUERY RESULT TOGGLE PIVOT.\n\\q: EXIT.\n```\n\n### execute query\n\nsee below\n\n#### start\n```\n$ redasql\n\n____          _                 _\n|  _ \\ ___  __| | __ _ ___  __ _| |\n| |_) / _ \\/ _` |/ _` / __|/ _` | |\n|  _ <  __/ (_| | (_| \\__ \\ (_| | |\n|_| \\_\\___|\\__,_|\\__,_|___/\\__, |_|\n                              |_|\n    - redash query cli tool -\n\nSUCCESS CONNECT\n- server version 8.0.0+b32245\n- client version 0.1.0.0\n\n(No DataSource)=#\n```\n\n#### connect datasource\n\nuse `\\c data_source_name`. if not provide data_source_name, show all available data sources. \n\n```\n(No DataSource)=# \\c metadata\nmetadata=#\n```\n\n#### describe table\n\nuse `\\d table_name`. if not provide table_name, show all table names. if provide table_name with wildcard(\\*), show describe matched tables.\n\n```\nmetadata=# \\d\naccess_permissions\nalembic_version\n:\nqueries\nquery_results\nquery_snippets\nusers\nvisualizations\nwidgets\nmetadata=# \\d queries\n## queries\n- schedule\n- updated_at\n- api_key\n- name\n- id\n- version\n- is_draft\n- query\n- is_archived\n- tags\n- last_modified_by_id\n- org_id\n- options\n- query_hash\n- description\n- latest_query_data_id\n- search_vector\n- data_source_id\n- schedule_failures\n- created_at\n- user_id\nmetadata=# \\d query_*\n## query_results\n- id\n- data\n- org_id\n- query_hash\n- data_source_id\n- runtime\n- query\n- retrieved_at\n## query_snippets\n- updated_at\n- id\n- description\n- created_at\n- user_id\n- trigger\n- snippet\n- org_id\n\n```\n\n#### execute query\n\nenter your SQL and semicolon.\n\n```bash\nmetadata=# select count(*) from queries;\n+-------+\n| count |\n+-------+\n|  3606 |\n+-------+\n\n1 row returned.\nTime: 0.0159s\n\n```\n\n`\\x` pivot result.\n\n\n\n```\nmetadata=# \\x\nset pivot format\n\nmetadata=# select id, user_id from queries limit 3;\n-[RECORD 1]-------\n     id: 543\nuser_id: 40\n-[RECORD 2]-------\n     id: 717\nuser_id: 40\n-[RECORD 3]-------\n     id: 515\nuser_id: 38\n\n\n3 rows returned.\nTime: 0.0281s\n\n```\n\n### quit\n\n`ctrl + D` or `\\q` quit redasql.\n\n```\nmetadata=# \\q                                                                                                                                                                        \nSayonara!\n```\n\n',
    'author': 'denzow',
    'author_email': 'denzow@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/denzow/redasql',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
