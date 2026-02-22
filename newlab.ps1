param([string]$Name)

if (-not $Name) {
    Write-Host "Please provide a name! Example: .\newlab.ps1 -Name 'vision-api-lab'" -ForegroundColor Yellow
    return
}

# Create the new folder
New-Item -ItemType Directory -Path ".\$Name" -Force

# Create a starter README inside that folder
$Content = "# Lab: $Name`n`Started on: $(Get-Date)`n`## Learnings`n- "
Set-Content -Path ".\$Name\Readme.md" -Value $Content

Write-Host "Folder '$Name' created. Ready to start!" -ForegroundColor Green