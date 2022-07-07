"""
This script generates a TOC and Back-to-top links in Markdown documents.
It scans for an existing TOC (and if available, updates it and keeps the
position of that existing TOC) and also respects the so-called reference
links section (if any, "<!-- LINKS START -->...<!-- LINKS END -->?").

The script is tailored to work in combination with an Applescript to add
the TOC to DEVONthink Markdown documents.

author: Fabrizio Musacchio (https://www.fabriziomusacchio.com)
date:  19.02.2022
"""
# %% IMPORTS
import sys
import re
text = sys.argv[1]
# %% DEFINE TOC-LEVEL
toc_level = 2
"""
define at which toc-level to start, e.g.:
  2 - only account for headings h2 (##) and higher; requires that
      the first occurring heading is h2 (except the document
      heading in line 0)
  1 - account for headings h1 (#) and higher; requires that a
      the first occurring heading is h1 (except the document
      heading in line 0)
"""
# %% MAIN ROUTINE
Current_Markdown_Text = sys.argv[1]
"""
    The following text conversion and re-conversion has to be performed,
    as the shell echo of multiline text within the Applescript introduces
    a a type of linebreaks other than "\n", which is not interpretable by
    Python. The following procedure re-introduces the "\n"-linebreaks:
"""
Current_Markdown_New_Text = Current_Markdown_Text.splitlines()
Current_Markdown_New_Text_tmp = [Current_Markdown_New_Text[0]]
# Current_Markdown_New_Text_tmp.append(Current_Markdown_New_Text[0])

# Scan the text for "#" and collect the TOC entries:
headline_index = 0
TOC_collector_list = []
for line_idx, line in enumerate(Current_Markdown_New_Text[1:]):
    line_idx+=1
    """
    line_idx starts with the value 1 and therefore the first line of the document 
    (the document's title) is skipped.
    """
    if line.startswith("#"):
        # remove any id in headlines from a previous run:
        line_cleaned = re.sub(r'\s*\[.*\]', '', line)

        # construct the new TOC entry:
        current_heading = re.sub(r'(^\#*\s)', '', line_cleaned)
        current_toc_entry=len(re.findall(r'[\#]', line_cleaned[toc_level:]))*("\t") + '1. ' + '['+current_heading+']'
        current_toc_link = '(#h'+str(headline_index)+')'
        TOC_collector_list.append(current_toc_entry+current_toc_link)

        # update the current heading and add the id:
        #newlines = '\n\n'
        Current_Markdown_New_Text_tmp.append(line_cleaned + ' [h'+str(headline_index)+']')
        headline_index += 1
    else:
        Current_Markdown_New_Text_tmp.append(line)

# scan for existing TOC and link sections:
toc_start_idx = 0
toc_end_idx   = 0
link_start_idx= 0
for line_idx, line in enumerate(Current_Markdown_New_Text_tmp):
    if line == '<!-- TOC START -->':
        toc_start_idx = line_idx
    if line == '<!-- TOC END -->':
        toc_end_idx = line_idx
    if line == '<!-- LINKS START -->':
        link_start_idx= line_idx

# insert the TOC:
if toc_start_idx==0 and toc_end_idx==0:
    Current_Markdown_New_Text_tmp2 = []
    Current_Markdown_New_Text_tmp2+=[Current_Markdown_New_Text_tmp[0]]
    Current_Markdown_New_Text_tmp2.append('\n<!-- TOC START -->')
    Current_Markdown_New_Text_tmp2.append("<a class='top-link hide' href='#toc'>↑</a>")
    Current_Markdown_New_Text_tmp2.append("<a name='toc'></a>")
    Current_Markdown_New_Text_tmp2.append("<div class='TOC'>\n")
    for toc_entry in TOC_collector_list:
        Current_Markdown_New_Text_tmp2.append(toc_entry)
    Current_Markdown_New_Text_tmp2.append('\n</div>\n<!-- TOC END -->')
else:
    Current_Markdown_New_Text_tmp2 = []
    Current_Markdown_New_Text_tmp2+=Current_Markdown_New_Text_tmp[0:toc_start_idx]
    Current_Markdown_New_Text_tmp2.append('<!-- TOC START -->')
    Current_Markdown_New_Text_tmp2.append("<a class='top-link hide' href='#toc'>↑</a>")
    Current_Markdown_New_Text_tmp2.append("<a name='toc'></a>")
    Current_Markdown_New_Text_tmp2.append("<div class='TOC'>\n")
    for toc_entry in TOC_collector_list:
        Current_Markdown_New_Text_tmp2.append(toc_entry)
    Current_Markdown_New_Text_tmp2.append('\n</div>\n<!-- TOC END -->')
Current_Markdown_New_Text_tmp2 += Current_Markdown_New_Text_tmp[toc_end_idx+1:]

# rejoin the processed text:
Current_Markdown_New_Text = '\n'.join(Current_Markdown_New_Text_tmp2)

# echo it back to the shell:
print(Current_Markdown_New_Text)