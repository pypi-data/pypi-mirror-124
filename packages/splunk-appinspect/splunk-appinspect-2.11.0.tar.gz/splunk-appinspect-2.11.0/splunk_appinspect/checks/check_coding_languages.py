# Copyright 2021 Splunk Inc. All rights reserved.

"""
### Checks that inspect the file contents and metadata to derive what coding languages are present. 

"""

# Python Standard Libraries
import os
import json
import importlib.resources as pkg_resources
import logging

# Third-Party Libraries
import guesslang

# Custom Libraries
import splunk_appinspect
from splunk_appinspect import resources


LOG = logging.getLogger(__name__)
PARSE_ERROR = "parse_error"
LANGUAGE_WHITELIST = ["javascript", "python", PARSE_ERROR]


@splunk_appinspect.tags("cloud", "security", "splunk_appinspect", "future")
@splunk_appinspect.cert_version(min="2.11.0")
def check_coding_languages(app, reporter):
    """Check to see what coding languages are present in the app. Flag for manual review in cases where *either* a
    language is detected that does not have automated checks or where the file extension does not match what is
    expected.
    """
    file_key = "file"
    size_key = "size"
    language_key = "language"
    extension_key = "file_extension"
    recognized_extensions_key = "recognized"
    other_unsupported_extensions_key = "other"
    language_null = "language_null"
    extensions_file = "semgrep_recognized_extensions.json"
    sorting_hat = guesslang.Guess()  # https://youtu.be/xQZFWA2KDbw?t=80
    language_data_list = []
    application_files = list(app.iterate_files())

    # apply language analysis against every file app
    #
    for directory, file, ext in application_files:
        full_filename = os.path.join(app.app_dir, directory, file)
        language_data = {}
        language_data[file_key] = full_filename
        language_data[extension_key] = ext
        try:
            with open(full_filename, 'r') as f:
                # in try/except because broken symlinks will cause getsize to fail
                language_data[size_key] = os.path.getsize(full_filename)
                data = f.read()
                language = sorting_hat.language_name(data)
                # in case someone submits an emtpy file - we need to check for None
                language_data[language_key] = language.lower() if language is not None else language_null
        except (OSError, guesslang.GuesslangError, UnicodeDecodeError, Exception) as e:
            language_data[language_key] = PARSE_ERROR
        finally:
            language_data_list.append(language_data)

    # flag anything for review that isn't currently covered by automated checks
    # parse_error is included in whitelist to prevent every non-executable file in the app from triggering a review.
    #
    manual_check_list = [
        language_data
        for language_data
        in language_data_list
        if language_data[language_key] not in LANGUAGE_WHITELIST
    ]

    if manual_check_list:
        reporter_output = f"Coding languages detected that are not supported by AppInspect: {manual_check_list}"
        reporter.warn(reporter_output, manual_check_list)  # TODO change to manual_check after trial period

    # check to see if there is anything that has a file extension that either won't be recognized by semgrep or isn't
    # what would be expected for a file of that type
    #
    try:
        extensions = pkg_resources.read_text(resources, extensions_file)
        known_extensions_dict = json.loads(extensions)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        LOG.error(f"exception when loading semgrep extensions file: {e}")
        raise e

    for language_data in language_data_list:
        language = language_data[language_key]
        # a parse error usually means the file is not a code file. there are other checks to detect compiled code which
        # we will rely on to tell us when a human needs to dive deeper into something. conversely, if this check pops
        # a flag on every file guesslang can't parse, almost every app will require human review as almost every app
        # has things in it like jpg files or other static assets that aren't parsable code.
        if language == PARSE_ERROR or language == language_null:
            continue

        # for this we DO want a human review because it means the language analysis tool has detected an instance of a
        # language that is not presently parseable by semgrep (the thing used to do the compliance analysis)
        if language not in known_extensions_dict.keys():
            reporter_output = f"Unable to parse file: {language_data[file_key]}"
            reporter.warn(reporter_output) # TODO change to manual_check after trial period
            continue

        recognized_extensions = known_extensions_dict[language][recognized_extensions_key]
        other_unsupported_extensions = known_extensions_dict[language][other_unsupported_extensions_key]
        file_extension = language_data[extension_key]

        if file_extension not in recognized_extensions and file_extension in other_unsupported_extensions:
            reporter_output = f"Unable to parse a file of this type encoded in this way: {language_data}"
            reporter.warn(reporter_output) # TODO change to manual_check after trial period

        if file_extension not in recognized_extensions and file_extension not in other_unsupported_extensions:
            reporter_output = f"File extension is unknown for a file of this type: {language_data}"
            reporter.warn(reporter_output) # TODO change to manual_check after trial period
