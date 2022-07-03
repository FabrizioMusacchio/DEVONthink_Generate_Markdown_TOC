-- Remove the table of contents (TOC) in DEVONthink's Markdown documents, that has been created by the Applescript "TOC generate".
--
-- This script relies on an external Python script (works for both, Python 2 and 3). The path to the folder, that contains that Python script, must be added to this Applescript (in 'MyPythonScriptPath').
--
-- author: Fabrizio Musacchio (https://www.fabriziomusacchio.com)
-- date: Feb 18, 2022

-- Please specify the path to the folder, where you've saved the Python script:
set MyPythonScriptPath to "<SET PATH TO THE PYTHON SCRIPT FOLDER>"
if MyPythonScriptPath = "<SET PATH TO THE PYTHON SCRIPT FOLDER>" then error "Error: Variable 'MyPythonScriptPath' not set. Please set the path of the folder, that contains the convert_wikilinks_to_markdown_links.py Python script."

-- On macOS < 12.3, set LocalPython to "/usr/bin/python". For higher macOS versions, install Python (e.g., via Anaconda.com or python.org), find out the path of your new Python installation (open a terminal and type "which python") and set LocalPython to the given result. The default setting below links to the Anaconda installation; in case you're also using Anaconda, please replace "<USER>" with your user name.
set LocalPython to "/Users/<USER>/opt/anaconda3/bin/python"

tell application id "DNtp"
	try
		set theNum to count of every selected record
		if theNum is 0 then error "Please select some documents."
		
		repeat with theRecord in every selected record
			if type of theRecord is markdown then
				set theText to plain text of theRecord
				set theShellScript to LocalPython & " " & MyPythonScriptPath & "remove_toc.py " & quoted form of theText
				set TheNewText to do shell script theShellScript
				--["Result ", TheNewText]
				set plain text of theRecord to TheNewText
				--TheNewText
			end if
		end repeat
	end try
end tell