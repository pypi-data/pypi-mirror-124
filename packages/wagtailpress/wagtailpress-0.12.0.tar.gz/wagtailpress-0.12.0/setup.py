# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['wagtailpress', 'wagtailpress.migrations']

package_data = \
{'': ['*'],
 'wagtailpress': ['locale/fr/LC_MESSAGES/*',
                  'static/wagtailpress/Fork-Awesome/*',
                  'static/wagtailpress/Fork-Awesome/.github/ISSUE_TEMPLATE/*',
                  'static/wagtailpress/Fork-Awesome/css/*',
                  'static/wagtailpress/Fork-Awesome/fonts/*',
                  'static/wagtailpress/Fork-Awesome/less/*',
                  'static/wagtailpress/Fork-Awesome/scss/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/_includes/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/_includes/accessibility/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/_includes/code/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/_includes/community/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/_includes/examples/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/_includes/icons/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/_includes/modals/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/_includes/products/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/_includes/tests/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/_layouts/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/_plugins/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/css/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/fork-awesome/less/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/fork-awesome/scss/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/ico/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/images/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/js/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/less/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/less/bootstrap-3.3.5/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/less/bootstrap-3.3.5/mixins/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/less/gandy-grid/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/less/site/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/less/site/bootstrap/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/assets/less/site/responsive/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/test/*',
                  'static/wagtailpress/Fork-Awesome/src/doc/test/height/*',
                  'static/wagtailpress/Fork-Awesome/src/icons/*',
                  'static/wagtailpress/Fork-Awesome/src/icons/svg/*',
                  'static/wagtailpress/css/*',
                  'static/wagtailpress/css/blocks/*',
                  'templates/wagtailpress/*',
                  'templates/wagtailpress/blocks/*']}

install_requires = \
['wagtail>=2.14.2,<3.0.0', 'wagtailperson>=0.13.3,<0.14.0']

setup_kwargs = {
    'name': 'wagtailpress',
    'version': '0.12.0',
    'description': 'A Blog build with Wagtail.',
    'long_description': "Wagtailpress\n============\n\nA Blog build with Wagtail. Its name is not a reference to Wordpress,\nbut the name wagtail_blog is already taken.\n\n\nFeatures\n--------\n\n- Index page model\n- Article page model\n- Authors are defined using [Wagtail person](https://framagit.org/SebGen/wagtailperson)\n- Tags\n- RSS feed for index pages\n- Delivred with acceptable templates\n\n\nInstall\n-------\n\nSimply install it from pypi.org:\n```bash\npip install wagtailpress\n```\n\nAdd this app and dependencies to django installed app in your\nsettings.py:\n```bash\nINSTALLED_APPS = [\n    # …\n    'wagtail.contrib.routable_page',\n    'wagtailperson',\n    'wagtailpress',\n    # …\n    ]\n```\n\nThen, finally, apply migration scripts:\n```bash\n./manage.py migrate wagtailpress\n```\n\n\nUse\n---\n\nThis application provide 2 pages models:\n\n-   A blog article page: A simple article\n-   A blog index page: The index of your blog, it list its children\n    articles, their tags and provide a RSS feed\n\nA blog article page got multiple fields:\n-   Title\n-   Publication date\n-   One or some authors\n-   An intro \n-   An optional header image\n-   The content of the article\n\n\nDevelopment\n-----------\n\nThis source code repository provide a full Django project, so you can\neasily work with wagtailperson for testing you modifications.\n\nSimply use these two steps in the source code working directory: \n```bash\n./manage.py migrate \n./manage.py runserver \n```\n\n\nTest\n----\n\nTo run test, simply run this in the root of the source code working directory:\n```bash\n./manage.py test\n```\n\n\nLicence \n-------\n\nLGPLv3\n\n\nAuthor(s)\n---------\n\nSébastien Gendre <seb@k-7.ch>\n\n\n\n",
    'author': 'Sébastien Gendre',
    'author_email': 'seb@k-7.ch',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://framagit.org/SebGen/wagtailpress',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
