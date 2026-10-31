param(
    [string]$Services = "postgres redis backend",
    [int]$WaitSeconds = 120
)

Write-Host "Bringing up Docker Compose services: $Services"
docker compose up -d $Services

Write-Host "Waiting for services to become healthy (up to $WaitSeconds seconds)..."
$elapsed = 0
while ($elapsed -lt $WaitSeconds) {
    $ps = docker compose ps --format "json" | ConvertFrom-Json
    $allHealthy = $true
    foreach ($svc in $ps) {
        if ($svc.State -ne 'running') { $allHealthy = $false }
    }
    if ($allHealthy) { break }
    Start-Sleep -Seconds 3
    $elapsed += 3
}

Write-Host "Applying Alembic migrations inside backend container..."
docker compose exec -T backend /bin/sh -c "alembic upgrade head"

Write-Host "Alembic finished. To inspect DB run: docker compose exec -T postgres psql -U $env:POSTGRES_USER -d $env:POSTGRES_DB -c \"\d\""
