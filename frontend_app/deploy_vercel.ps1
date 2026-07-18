# Deploy do TaskQuest (frontend Flutter web) no Vercel.
# Uso:  .\deploy_vercel.ps1 -ApiUrl "https://SEU-BACKEND.up.railway.app"
param(
    [Parameter(Mandatory = $true)]
    [string]$ApiUrl
)

$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "1/3 Compilando Flutter web com API_URL=$ApiUrl ..."
C:\flutter\bin\flutter.bat build web --release --dart-define=API_URL=$ApiUrl

Write-Host "2/3 Copiando vercel.json para o build ..."
Copy-Item vercel.json build\web\vercel.json -Force

Write-Host "3/3 Publicando no Vercel ..."
Set-Location build\web
npx vercel deploy --prod

Write-Host "Pronto! Use o link que o Vercel imprimiu acima (funciona em celular e computador)."
