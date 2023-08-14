import vobject
import os
import sys
import re
import subprocess
from dateutil.parser import parse

# Default Contact group
os.environ["CONTACT_GROUP"] = "Obsidian"
# Default output folder path
os.environ["OUTPUT_FOLDER"] = "📇 Contacts"

APPLESCRIPT = """
set AppleScript's text item delimiters to {delimiter}

tell application "Contacts"

    if not running then
        run
        delay 1
    end if

    set vCardText to (get vcard of every person in group "{group}") as text

end tell
""".format(delimiter='""', group=os.environ["CONTACT_GROUP"])

def vcard_to_markdown(vcard):
    markdown = f"## 👤 {vcard.fn.value}\n"

    if hasattr(vcard, 'email'):
        markdown += f"- 📧 Email: [{vcard.email.value}](mailto:{vcard.email.value})\n"

    if hasattr(vcard, 'tel'):
        for tel in vcard.tel_list:
            markdown += f"- ☎️ Phone: [{tel.value}](tel:{tel.value})\n"

    if hasattr(vcard, 'bday'):
        bday = parse(vcard.bday.value).strftime("%Y%m%d")
        markdown += f"- 🎂 Birthday: [[{bday}]]\n"

    if hasattr(vcard, 'x_anniversary'):
        anniversary = parse(vcard.x_anniversary.value).strftime("%Y%m%d")
        markdown += f"- 💍 Anniversary: [[{anniversary}]]\n"

    if hasattr(vcard, 'org'):
        markdown += f"- 🏢 Organization: {vcard.org.value[0]}\n"

    if hasattr(vcard, 'note'):
        markdown += f"- 📝 Note: {vcard.note.value}\n"

    if hasattr(vcard, 'url'):
        markdown += f"- 🌐 Website: [{vcard.url.value}]({vcard.url.value})\n"

    if hasattr(vcard, 'geo'):
        markdown += f"- 📍 Location: {vcard.geo.value}\n"

    if hasattr(vcard, 'role'):
        markdown += f"- 💼 Role: {vcard.role.value}\n"

    if hasattr(vcard, 'title'):
        markdown += f"- 📛 Title: {vcard.title.value}\n"

    if hasattr(vcard, 'x_gender'):
        gender_emoji = "♀️" if vcard.x_gender.value.lower() == "f" else "♂️"
        markdown += f"- {gender_emoji} Gender: {vcard.x_gender.value}\n"

    if hasattr(vcard, 'lang'):
        markdown += f"- 🗣️ Language: {vcard.lang.value}\n"

    if hasattr(vcard, 'adr'):
        for adr in vcard.adr_list:
            markdown += f"- 🏠 Address: {adr.value}\n"

    return markdown.rstrip()

def process_grouped_vcard(vcard_data):
    vcards = vobject.readComponents(vcard_data)

    output_folder = os.environ["OUTPUT_FOLDER"]
    os.makedirs(output_folder, exist_ok=True)

    for vcard in vcards:
        if hasattr(vcard, 'fn'):
            file_name = re.sub(r'[\\/*?:"<>|]', '_', vcard.fn.value) + '.md'
            file_path = os.path.join(output_folder, file_name)
            with open(file_path, 'w') as md_file:
                md_file.write(vcard_to_markdown(vcard))
                print(f"Saved {file_path}")

def get_grouped_vcard_from_applescript():
    result = subprocess.run(
        ["osascript", "-e", APPLESCRIPT],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout

if __name__ == "__main__":
    vcard_data = get_grouped_vcard_from_applescript()
    process_grouped_vcard(vcard_data)
