# Wagtail Tag Manager
![PyPI](https://img.shields.io/pypi/v/wagtail-tagmanager.svg)
![Python](https://img.shields.io/pypi/pyversions/wagtail-tagmanager.svg)
![License](https://img.shields.io/pypi/l/wagtail-tagmanager.svg)
![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-brightgreen)

**Wagtail Tag Manager** is an admin interface for managing tag usage across your Wagtail site:

- View and manage all objects (Page, Image, Document, etc.) using a given tag
- Works across Pages, Documents, Images, and other tagged models that use `django-taggit`
- Add or remove tags from multiple object types
- Bulk merge and delete tags
- Add multiple pages to a given tag
- Edit tag names and slugs
- Compatible with custom tag models and page models

## Supported versions

- Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13
- Django 4.2, 5.0, 5.1, 5.2
- Wagtail 5.2, 6.1, 6.2, 6.3, 6.4

While these are the officially supported versions, `wagtail-tagmanager` may work on older versions of Python, Django, or Wagtail as it avoids reliance on newer features. Please note that issues on unsupported versions might not be prioritized.

## Installation

1. Install via pip:

    ```
    pip install wagtail-tagmanager
    ```

2. Add to your `INSTALLED_APPS`:

    ```python
    INSTALLED_APPS = [
        ...
        "wagtail_tagmanager",
    ]
    ```

3. Configure your settings:

   1. Specify the model you use that inherits from `TaggedItemBase`. If you use tags for pages, you would have set this up already. More information [here](https://docs.wagtail.org/en/latest/advanced_topics/tags.html#adding-tags-to-a-page-model). **You must define this setting to use this tag manager** :

        ```python
          WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL = "yourapp.BlogPageTag"
        ```

    2. If you want to be able add pages to a specific tag in bulk, specify the page model you want to add tags to. If you want to add tags to all pages, set it to your first concrete model that inherits Page (if the model is abstract, this will not work). **You must define this setting to add pages to a tag**

          ```python
          WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL = "yourapp.BlogPage"
          ```

## Usage
Once installed, go to the "Tags" section in the Wagtail admin.

There are four main views:

### Tag Index View
- View all tags in the project and how many objects are tagged with each tag
- Add and Delete tags
- Merge multiple tags into one
- Click each tag to go to Tag Edit View

![Tags Index View](images/tag_index_view.png)

### Tag Edit View
- Edit tag `Name` and `Slug`
- Button to view all objects tagged with that tag

![Tag Edit View](images/tag_edit_view.png)

### Manage Tags View
- View and search all objects tagged with the selected tag
- Remove the tag from multiple objects
- Button to add pages to this tag (Note: This button only appears if `WAGTAIL_TAGMANAGER_BASE_PAGE_MODEL` is defined)

![Manage Tags View](images/manage_tags_view.png)

###  Add Pages to Tag View
- Add pages in bulk to the specified tag
- Search for a specific page by title

![Add Pages to Tag View](images/add_pages_to_tag_view.png)

## Known Issues

- The object count for each tag will count objects even if their model was deleted (since deleting a model does not delete it's corresponding `ContentType`). This can lead to incorrect object counts on the Tag Index Page. This `model` is defined in the `ContentType` model

## Contributing

If you would like to contribute, feel free to create a pull request. All changes to main must go through a pull request and be reviewed. Direct pushes, merges without review, or force pushes are blocked by branch protection rules.

### Install

  Clone this repository:

  ```bash
  git clone https://github.com/mikhail-robinson/wagtail-tagmanager.git
  cd wagtail-tagmanager
  ```

  From inside your preferred virtual environment:

  ```bash
  cd wagtail-tagmanager
  pip install -r requirements.txt
  ```

  ### pre-commit
  Note that this project uses [pre-commit](https://github.com/pre-commit/pre-commit) to enforce [ruff](https://github.com/astral-sh/ruff) formatting. This will check that you have run `ruff format` and `ruff check` before committing. If you forget, pre-commit will throw the error `Git: [WARNING] Unstaged files detected` when committing to remind you. To setup locally:

  ```bash
  cd wagtail-tagmanager
  pre-commit install
  ```
  ### How to run tests

  ```bash
  cd wagtail-tagmanager
  python3 runtests.py
  ```


