# Dynamic Model Serializer for Django Profiles

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Django](https://img.shields.io/badge/django-3.2%2B-green)](https://www.djangoproject.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 📝 Description

**Dynamic Model Serializer** is a lightweight, flexible utility for Django applications that allows you to serialize **any model** on the fly based on a `Profile` configuration entry. Instead of writing separate serializers for each model, you define a profile record that points to an app and model name, and the serializer automatically fetches and converts the data – filtered by the current user – into a clean dictionary, ready for JSON responses.

This tool is especially useful for building **dynamic user profiles**, **dashboard widgets**, or **pluggable data endpoints** where the structure of the data can change without code changes.

---

## ✨ Features

- **Dynamic model resolution** – load any registered Django model by `app_name` and `model_name`.
- **User‑aware filtering** – automatically filters records by the current user (if the target model has a `user` field).
- **Automatic foreign key expansion** – resolves related objects and serializes them recursively.
- **Security‑first** – excludes sensitive fields (passwords, tokens, etc.) by default; you can add or remove fields from the blacklist.
- **Easy to integrate** – works with any view (function‑based, class‑based, or DRF).
- **Lightweight and self‑contained** – no extra dependencies beyond Django itself.

---

## 🎯 Who is this for?

- **Django developers** who need to expose dynamic model data in user profiles.
- **Backend engineers** building configurable dashboards or admin panels.
- **Teams** that want to reduce boilerplate code for serializing multiple models.
- **Startups** looking for a quick way to prototype user‑specific data endpoints.

If you often find yourself writing repetitive serializers for different models, this tool will save you time and keep your codebase clean.

---

## 🚀 Installation

1. **Clone the repository** or copy the `serializer.py` file into your Django project.

```bash
git clone https://github.com/yourusername/dynamic-model-serializer.git
```

2. Place the ```serializer.py``` inside a utility folder (e.g., ```utils/serializer.py```) or within an existing app.

3. Ensure the ```Profile``` model exists in your project (see Quick Start below).

4. No extra ```pip``` install needed – it uses only built‑in Django modules.

---

## 🧪 Quick Start
## 1. Define the Profile model
Create a model that stores the configuration for each profile type:
```python
from django.db import models

class Profile(models.Model):
    title = models.CharField(max_length=100, blank=True, null=True)
    fa_title = models.CharField(max_length=100, blank=True, null=True)
    model_app = models.CharField(max_length=100)          # e.g., 'auth'
    model_name = models.CharField(max_length=100)         # e.g., 'User'

    def __str__(self):
        return self.title or f"{self.model_app}.{self.model_name}"
```
Note: You can name the model differently; adjust the import accordingly.

## 2. Use the serializer in a view
```python
from django.http import JsonResponse
from .models import Profile
from utils.serializer import Serializer

def profile_data_view(request, title):
    profile = Profile.objects.filter(title=title).first()
    if not profile:
        return JsonResponse({'error': 'Profile not found'}, status=404)

    serializer = Serializer(profile, request.user.id)
    data = serializer.serializedData()
    return JsonResponse(data, safe=False)
```
That’s it! The ```serializedData()``` method returns a dictionary where keys are record indices (or IDs) and values are the serialized records with all fields (except blacklisted ones).

---

## 📖 Usage Guide

### The `Serializer` Class

**Constructor:**  
`Serializer(profile_instance, user_id)`

- `profile_instance` – an object with `model_app` and `model_name` attributes.
- `user_id` – the primary key of the current user (used for filtering).

### Available Methods

| Method | Description |
|--------|-------------|
| `getFields()` | Returns a list of all field objects of the target model. |
| `recordObj()` | Returns a `QuerySet` of records filtered by `user_id`. |
| `recordsValues()` | Returns the same `QuerySet` as a `ValuesQuerySet` (dictionaries). |
| `getModel(app, name)` | Helper to load a model dynamically. |
| `addDenyField(field_name)` | Adds a field to the blacklist (excluded from output). |
| `removeDenyField(field_name)` | Removes a field from the blacklist. |
| `safeDecode(obj)` | Converts a model instance to a dict, converting all values to strings and skipping blacklisted fields. |
| `getRecord(id)` | **Caution:** This method is buggy in the initial version; see “Known Issues”. |
| `serializedData()` | Main method that returns a fully serialized dictionary of all user‑specific records. |

### Blacklist Management

By default, these fields are excluded:  
`password`, `code`, `otp`, `is_active`, `is_staff`, `is_superuser`, `groups`, `user_permissions`.

To add or remove fields per instance:

```python
serializer = Serializer(profile, user_id)
serializer.addDenyField('email')        # now 'email' will be hidden
serializer.removeDenyField('is_active') # now 'is_active' will appear
```

---

## 💡 Example
Assume you have a `BlogPost` model with `title`, `content`, `author` (ForeignKey to `User`), and `created_at`.
You create a `Profile` record:

```python
Profile.objects.create(
    title='blog_posts',
    model_app='blog',
    model_name='BlogPost'
)
```

Then in your view:
```python
serializer = Serializer(profile, request.user.id)
result = serializer.serializedData()
```
`result` will look like:
```json
{
    "0": {
        "id": "1",
        "title": "My First Post",
        "content": "Hello world!",
        "author": {
            "id": "5",
            "username": "john_doe",
            "email": "john@example.com"
        },
        "created_at": "2025-01-15 10:30:00"
    }
}
```
Foreign keys are automatically expanded (the related object is serialized recursively).

## ⚠️ Known Issues (Initial Version)

- The `getRecord(id)` method has a bug – it references `self.recordObj.objects` instead of `self.MyModel.objects`. Please avoid using it or override it.
- The `setSlugToLink` method is not implemented yet.
- Performance: the `serializedData()` method executes one query per record for each foreign key. For large datasets, consider using `select_related` and `prefetch_related` in a custom implementation.
- The blacklist is a class‑level attribute; changing it via `addDenyField` will affect all instances. To make it instance‑safe, copy the list inside `__init__`.

We are actively working on improvements – feel free to contribute!

---

## 🤝 Contributing

Contributions are welcome! If you find a bug, have a feature request, or want to improve the code, please:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/amazing-feature`).
3. Commit your changes (`git commit -m 'Add amazing feature'`).
4. Push to the branch (`git push origin feature/amazing-feature`).
5. Open a Pull Request.

Please make sure to update the README and add tests if applicable.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` file for more information.

---

## 📬 Contact

Project Link: https://github.com/MohammadReza-py/Django-Dynamic-Profile(https://github.com/MohammadReza-py/Django-Dynamic-Profile)  
Feel free to open an issue or reach out if you have any questions!

---

**Happy coding!** 🚀
