# Setup script for MediaCrawler on H: drive
$env:PLAYWRIGHT_BROWSERS_PATH = "H:\C#\tool\MediaCrawler\.playwright-browsers"

Write-Host "Installing dependencies..."
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

Write-Host "Installing Playwright browsers to H: drive..."
.\.venv\Scripts\python.exe -m playwright install chromium

Write-Host "Setting up .env file..."
if (-not (Test-Path .env)) {
    Copy-Item .env.example .env
}

Write-Host "Setup complete! Please remember to set PLAYWRIGHT_BROWSERS_PATH when running the crawler."
