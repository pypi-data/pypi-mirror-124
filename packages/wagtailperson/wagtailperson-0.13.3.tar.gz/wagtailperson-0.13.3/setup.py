# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtailperson', 'wagtailperson.migrations']

package_data = \
{'': ['*'],
 'wagtailperson': ['locale/fr/LC_MESSAGES/*',
                   'locale/fr_CH/LC_MESSAGES/*',
                   'static/wagtailperson/css/*',
                   'static/wagtailperson/js/*',
                   'templates/wagtailperson/*',
                   'templates/wagtailperson/blocks/*']}

install_requires = \
['wagtail>=2.14.2,<3.0.0']

setup_kwargs = {
    'name': 'wagtailperson',
    'version': '0.13.3',
    'description': 'Add a person and a persons index pages to Wagtail as well as a person block for StreamFields',
    'long_description': 'Wagtail Person\n==============\n\nOn a CMS, we regularly need to represent an author, a speaker, a\nperson. To avoid repetition and duplication of datas about this, this\napp add a person model to Wagtail, with admin UI. Do not hesitate to\nuse it on your blog or lectures appilaciton.\n\nThis model is accompanied by a Person page model and a Persons index\npage model. Each Person page is linked to a Person model to see it on\nyour website.\n\nThis app also provide a basic CSS and templates, feel free to\ncustomize it.\n\n\nImportant\n---------\n\nSince version 0.9.8, the Person Page model has been split in 2 models:\n- A Person model\n- A Person page model, with a many2one to a Person model\n\n\nInstall\n-------\n\nSimply install it from pypi.org:\n\n``` {.bash}\npip install wagtailperson\n```\n\nAdd this app to django installed app in your settings.py:\n\n``` {.python}\nINSTALLED_APPS = [\n    # …\n    \'wagtailperson\',\n    # …\n    \'wagtail.contrib.modeladmin\',\n    # …\n    ]\n```\n\nThen, finally, apply migration scripts:\n\n``` {.bash}\n./manage.py migrate wagtailperson\n```\n\n\nUse\n---\n\nThis application add a new entry to the administration menu, called\n"Author or Person". From this menu, you can add a new author or\nperson.\n\nIf you want to link one of your wagtail page models, or django models,\nto a person: Simply add a many2one field linked to\n`wagtailperson.models.Person`.\n\nThis application also provide 2 pages models:\n\n-   A Person page: Show puplicly someone, can be used mostly\n    everywhere in the pages tree\n-   A Persons index page: A root page for Persons pages, it list each\n    of Persons pages it had as children pages and can only have Person\n    pages as children\n\nThe person index page can be useful to group persons, globally or per\ngroup.\n\nA person got multiple fields:\n-   Picture\n-   Name\n-   Tags\n-   Introduction\n-   Abstract\n\nThis application also provide a person block for StreamField, at\n`wagtailperson.blocks.PersonBlock`. Feel free to use it on your models\nStreamField.\n\n\nDevelopment\n-----------\n\nThe source code repository provide a full Django project, so you can\neasily work with wagtailperson for testing you modifications.\n\nSimply use these two steps in the source code working directory:\n\n``` {.bash}\n./manage.py migrate\n./manage.py runserver\n```\n\n\nLicence\n-------\n\nLGPLv3\n\n\nAuthor\n------\n\nSébastien Gendre \\<seb\\@k-7.ch\\>\n',
    'author': 'Sébastien Gendre',
    'author_email': 'seb@k-7.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://framagit.org/SebGen/wagtailperson',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
