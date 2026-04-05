# Import Active Directory module
Import-Module ActiveDirectory

# VAriables
$csvPath = "C:\nfl_rosters.csv"
$defaultPassword = ConvertTo-SecureString "NFLlab123!" -AsPlainText -Force
$domain = "DC=nfllab,DC=local"

# Create top-level OUs
$ous = @(
    "OU=NFL,$domain",
    "OU=Admins,$domain",
    "OU=AFC,OU=NFL,$domain",
    "OU=NFC,OU=NFL,$domain"
)

foreach ($ou in $ous) {
    $name = ($ou -split ",")[0] -replace "OU=", ""
    $path = ($ou -split ",", 2)[1]
    if (-not (Get-ADOrganizationalUnit -Filter "DistinguishedName -eq '$ou'" -ErrorAction SilentlyContinue)) {
        New-ADOrganizationalUnit -Name $name -Path $path
        Write-Host "Created OU: $name"
    }
}

# Import players and create divison/team OUs and users
$players = Import-Csv $csvPath

foreach ($player in $players) {
    $conference = $player.Conference
    $division = $player.Division
    $team = $player.Team

    $conferenceOU = "OU=$conference,OU=NFL,$domain"
    $divisionOU = "OU=$division,OU=$conference,OU=NFL,$domain"
    $teamOU = "OU=$team,OU=$division,OU=$conference,OU=NFL,$domain"

    # Create division OU if doesn't exist
    if (-not (Get-ADOrganizationalUnit -Filter "DistinguishedName -eq '$divisionOU'" -ErrorAction SilentlyContinue)) {
        New-ADOrganizationalUnit -Name $division -Path $conferenceOU
        Write-Host "Created OU: $division"
    }

    # Create team OU if doesn't exist
    if (-not (Get-ADOrganizationalUnit -Filter "DistinguishedName -eq '$teamOU'" -ErrorAction SilentlyContinue)) {
        New-ADOrganizationalUnit -Name $team -Path $divisionOU
        Write-Host "Created OU: $team"
    }

    # Create user
    $username = $player.Username
    if (-not (Get-ADUser -Filter "SamAccountName -eq '$username'" -ErrorAction SilentlyContinue)) {
        New-ADUser `
            -GivenName $player.FirstName `
            -Surname $player.LastName `
            -Name "$($player.FirstName) $($player.LastName)" `
            -SamAccountName $username `
            -UserPrincipalName "$username@nfllab.local" `
            -Path $teamOU `
            -Department $player.Department `
            -Company $player.Company `
            -Title $player.Position `
            -AccountPassword $defaultPassword `
            -ChangePasswordAtLogon $true `
            -Enabled $true
        Write-Host "Created user: $username"
    }
}

Write-Host "Done! All OUs and users created."