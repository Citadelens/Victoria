    $watcher = New-Object System.IO.FileSystemWatcher
# Set folder to watch. Change this path.
    $watcher.Path = "C:\Users\Teo\Documents\Paradox Interactive\Victoria II\HPM\save games\"
# Watch the autosave file
    $watcher.Filter = "autosave.v2"
    $watcher.IncludeSubdirectories = $false
    $watcher.EnableRaisingEvents = $true
# Setup a counter for the number of saves.
# I did this in an external text file, instead of in the code, because I was playing around with multiple processes monitoring the same file.
New-Item -Path "C:\Users\Teo\Documents\Paradox Interactive\Victoria II\HPM\save games\" -Name "num.txt" -ItemType "file" -Value "0" -Force

    $action = {
# Wait for the autosave file to actually be written.
# If you do not wait here, you might end up getting corrupted saves
		sleep 40
# Initialize
		$num = 0
# Read, increment, write
		$num = Get-Content -Path "C:\Users\Teo\Documents\Paradox Interactive\Victoria II\HPM\save games\num.txt"
		$num = [System.Decimal]::Parse($num)+1
		$num | Out-File "C:\Users\Teo\Documents\Paradox Interactive\Victoria II\HPM\save games\num.txt"
# Save file
                Copy-Item "C:\Users\Teo\Documents\Paradox Interactive\Victoria II\HPM\save games\autosave.v2" -Destination $num
              }
# Wait until the autosave file is created
    Register-ObjectEvent $watcher "Created" -Action $action
# Infinite loop
    while ($true) {sleep 10}