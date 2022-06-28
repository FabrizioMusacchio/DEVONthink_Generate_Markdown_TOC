# DEVONthink Markdown TOC generator

This Applescript generates a table of contents (TOC) and Back-to-top links in DEVONthink's Markdown documents.

<div style="text-align: center;"><a href="Screenshot_preview.png"><img src="Screenshot_preview.png" style="width: 90%;"></a>
<a href="Screenshot_editview.png"><img src="Screenshot_editview.png" style="width: 90%;"></a>

The generated TOC in DEVONthink's Markdown preview (left) and edit (right) view. 
</div> 

## How to install
Download the two Applescript and Python files:

* TOC generate.scpt
* TOC remove.scpt
* generate_toc.py
* remove_toc.py

Place the Applescript files into DEVONthink's script folder.

<div style="text-align: center;"><a href="Screenshot_DEVONthink_script_folder.png"><img src="Screenshot_DEVONthink_script_folder.png" style="width: 100%;"></a>

Open DEVONthink's script folder via DEVONthink's script menu.
</div> 

Place the Python scripts to a folder of your choice. The Applescripts rely on these Python scripts, which work for both Python 2 and 3. The path to the folder containing the Python scripts must be specified in the Applescripts (in the `MyPythonScriptPath` variable).


## How the script works
The Applescript hands-over the document's content to the Python script, which scans for all lines starting with a `#`, collects the heading texts and adds a label at the end of each headline (e.g., `## Section 1 [h0]`). The labels – not visible in the preview mode – are required for a simple but unambiguous linking to the headlines and are automatically updated with each run of the script. A Back-to-top link is placed over each headline, which links to the TOC. 

The script also scans for an existing TOC. If available, that TOC is updated and its previous position in the document is retained. I.e., after the first run of the script, a TOC section (`<!-- TOC START -->...<!-- TOC END -->`) is inserted right after the first line of the document, and you can freely move that section within the document.

In the Python script, you can define the TOC-level to be considered by adjusting the `toc_level` variable:

```
toc_level defines at which toc-level to start, e.g.:
  2 - only account for headings h2 (##) and higher; requires that
      the first occuring heading is h2 (except the document
      heading in line 0 (headline_index))
  1 - account for headings h1 (#) and higher; requires that a
      the first occuring heading is h1 (except the document
      heading in line 0 (headline_index))
```

By default, the script ignores the first line of the document, so that the document's title will not be part of the TOC. 

The script respects a so-called reference
links section (`<!-- LINKS START -->...<!-- LINKS END -->?`, if available). This section is the result of another Applescript I apply for handling Markdown reference links.

When the Python script is done, the original content including the TOC and all other additions is hand-overed back to the Applescript, which replaces the document's current content with the updated one.

The "TOC remove" script removes the generated TOC, the added headline labels and the Back-to-top links.

## Use at your own risk
I checked both scripts for various possible formatting within a Markdown document and I tried to make them as failure-resistant as possible. Nevertheless, the scripts replace your document's content with an actually new version of the content, which contains the additions mentioned above. In extreme cases, formatting that have not yet been taken into account can change the content. **Therefore, please backup your files before you apply the scripts and first try them out with some Markdown files, that contain the some formatting that you usually apply to your documents**. Please report any bugs in the issue section.

