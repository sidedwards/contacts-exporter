# Contacts Exporter

This is a Python script to export contacts from the macOS Contacts app in vCard format to Markdown files with structured data. The script is compatible with Python 3.

## Installation

Clone this repository or download the script file `main.py`.

This script requires the `vobject` and `dateutil` Python packages. To install them, run:

```
pip3 install vobject python-dateutil
```


## Usage

1. Open the Contacts app on your macOS.
2. Create or select a contact group that you want to export.
3. Open a terminal window and navigate to the directory where you saved `main.py`.
4. Run the script with `python3 main.py`.

By default, the script exports the contacts from a default "Obsidian" group and saves the Markdown files in the "📇 Contacts" folder. You can customize these settings by setting the `CONTACT_GROUP` and `OUTPUT_FOLDER` environment variables, respectively.

## Output

The script exports each contact as a Markdown file with the following structure:

```md
## 👤 Name
- 📧 Email: [email@example.com](mailto:email@example.com)
- ☎️ Phone: [+1 (555) 123-4567](tel:+15551234567)
- 🎂 Birthday: [[20000101]]
- 💍 Anniversary: [[20100101]]
- 🏢 Organization: Example Inc.
- 📝 Note: Some notes about the contact.
- 🌐 Website: [example.com](http://example.com)
- 📍 Location: 37.7749° N, 122.4194° W
- 💼 Role: Some role
- 📛 Title: Some title
- ♀️ Gender: F
- 🗣️ Language: English
- 🏠 Address: 123 Main St, Suite 100, San Francisco
```


The script supports the following vCard fields:
- `fn`
- `email`
- `tel`
- `bday`
- `x_anniversary`
- `org`
- `note`
- `url`
- `geo`
- `role`
- `title`
- `x_gender`
- `lang`
- `adr`

## Notes

If a vCard field is not present in a contact, the corresponding section will not be included in the Markdown file.

The script replaces any illegal characters (`\`, `/`, `*`, `?`, `:`, `"`, `<`, `>`, `|`) in the contact name with underscores (`_`) to avoid issues with file naming.
