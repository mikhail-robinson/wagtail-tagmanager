# Wagtail Tag Manager

**Wagtail Tag Manager** is an extension for managing tag usage across your Wagtail site. It provides tools to:

- View and manage all objects using a given tag
- Add or remove tags from multiple pages
- Bulk merge tags
- Works across Pages, Documents, Images, and other tagged models that use `django-taggit`

![Demo screenshot here if available]

---

## Features

- Admin interface for managing tags
- Bulk remove tags from selected objects
- Add tags to untagged pages
- Full object search and filtering
- View object types (Page, Image, etc.)
- Bulk merge tags
- Compatible with custom tag models

---

## Installation

1. Install via pip:

```
pip install wagtail-tagmanager
```

2. Add to your INSTALLED_APPS:
```
INSTALLED_APPS = [
    ...
    "wagtail_tagmanager",
]
```

3. Configure your custom page tagging model in your settings file:

```
WAGTAIL_TAGMANAGER_PAGE_TAG_MODEL = "yourapp.CustomPageTag"
```

## Usage

Once installed, go to the "Tags" section in the Wagtail admin.

From there, you can:

- Click a tag to view and manage all tagged objects

- Add/remove the tag from Pages

- Search across tagged objects

- Merge multiple tags into one