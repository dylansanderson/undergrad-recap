$ErrorActionPreference = 'Stop'
$v2 = $PSScriptRoot
$cw = 'C:\Users\user\Desktop\school_notes_projects_etc\Coursework'
$o = "$v2\out"
foreach ($f in 'Undergrad_Recap_Lectures.mp4', 'Undergrad_Recap_Lectures.srt', 'Undergrad_Recap_Lectures_chapters.txt', 'Undergrad_Recap_Lectures_Image_Credits.txt', 'Undergrad_Recap_Lectures_timeline.json') {
    if (-not (Test-Path "$o\$f")) { throw "missing build output $f" }
}
Copy-Item "$o\Undergrad_Recap_Lectures.mp4" "$cw\Undergrad_Recap_Lectures.mp4" -Force
Copy-Item "$o\Undergrad_Recap_Lectures.srt" "$cw\Undergrad_Recap_Lectures.srt" -Force
Copy-Item "$o\Undergrad_Recap_Lectures_chapters.txt" "$cw\Undergrad_Recap_Lectures_YouTube_Chapters.txt" -Force
Copy-Item "$o\Undergrad_Recap_Lectures_Image_Credits.txt" "$cw\Image_Credits.txt" -Force
Copy-Item "$o\Undergrad_Recap_Lectures_timeline.json" "$cw\Ask-the-Narrator\timeline.json" -Force
robocopy "$o\courses" $cw /E /NFL /NDL /NJH /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed $LASTEXITCODE" }
"installed"
