#!/usr/bin/python3
"""
Simple templating programme.

This module contains a function that generates personalised invitation files
from a template and a list of attendee dictionaries.
"""

import os


def generate_invitations(template, attendees):
    """
    Generate invitation files from a template and attendee data.

    Args:
        template: A string containing placeholders.
        attendees: A list of dictionaries containing attendee information.
    """

    if not isinstance(template, str):
        print("Invalid input: template must be a string.")
        return

    if not isinstance(attendees, list):
        print("Invalid input: attendees must be a list of dictionaries.")
        return

    if not all(isinstance(attendee, dict) for attendee in attendees):
        print("Invalid input: attendees must be a list of dictionaries.")
        return

    if template.strip() == "":
        print("Template is empty, no output files generated.")
        return

    if len(attendees) == 0:
        print("No data provided, no output files generated.")
        return

    placeholders = ["name", "event_title", "event_date", "event_location"]

    for index, attendee in enumerate(attendees, start=1):
        invitation = template

        for key in placeholders:
            value = attendee.get(key, "N/A")

            if value is None:
                value = "N/A"

            invitation = invitation.replace("{" + key + "}", str(value))

        output_filename = f"output_{index}.txt"

        if os.path.exists(output_filename):
            os.remove(output_filename)

        try:
            with open(output_filename, "w", encoding="utf-8") as file:
                file.write(invitation)
        except OSError as error:
            print(f"Error writing {output_filename}: {error}")
