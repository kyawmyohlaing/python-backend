@echo off
:: Manual authentication testing script for Windows using curl

echo === Manual Authentication Testing ===

:: Configuration
set BASE_URL=http://localhost:8088
set LOGIN_URL=%BASE_URL%/api/auth/login
set MENU_URL=%BASE_URL%/api/menu
set ORDER_URL=%BASE_URL%/api/orders

echo 1. Testing authentication with valid credentials...
:: Note: This requires jq for Windows or PowerShell to parse JSON
for /f "tokens=*" %%i in ('curl -s -X POST "%LOGIN_URL%" -H "Content-Type: application/x-www-form-urlencoded" -d "username=admin&password=adminpassword" ^| jq -r ".access_token"') do set TOKEN=%%i

if "%TOKEN%"=="null" (
    echo FAILED: Could not obtain authentication token
    exit /b 1
)

if "%TOKEN%"=="" (
    echo FAILED: Could not obtain authentication token
    exit /b 1
)

echo SUCCESS: Obtained authentication token
echo.

echo 2. Testing GET request to /api/menu WITHOUT authentication...
curl -s -o nul -w "Status Code: %%{http_code}\n" "%MENU_URL%"
echo.

echo 3. Testing POST request to /api/menu WITHOUT authentication...
curl -s -o nul -w "Status Code: %%{http_code}\n" -X POST "%MENU_URL%" -H "Content-Type: application/json" -d "{\"name\":\"Test Item\",\"price\":10.99,\"category\":\"Test\"}"
echo.

echo 4. Testing GET request to /api/menu WITH authentication...
curl -s -o nul -w "Status Code: %%{http_code}\n" "%MENU_URL%" -H "Authorization: Bearer %TOKEN%"
echo.

echo 5. Testing POST request to /api/menu WITH authentication...
curl -s -o nul -w "Status Code: %%{http_code}\n" -X POST "%MENU_URL%" -H "Content-Type: application/json" -H "Authorization: Bearer %TOKEN%" -d "{\"name\":\"Test Item\",\"price\":10.99,\"category\":\"Test\"}"
echo.

echo 6. Testing GET request to /api/orders WITHOUT authentication...
curl -s -o nul -w "Status Code: %%{http_code}\n" "%ORDER_URL%"
echo.

echo 7. Testing POST request to /api/orders WITHOUT authentication...
curl -s -o nul -w "Status Code: %%{http_code}\n" -X POST "%ORDER_URL%" -H "Content-Type: application/json" -d "{\"order\":[{\"name\":\"Test Item\",\"price\":10.99,\"category\":\"Test\",\"modifiers\":[]}],\"total\":10.99}"
echo.

echo 8. Testing GET request to /api/orders WITH authentication...
curl -s -o nul -w "Status Code: %%{http_code}\n" "%ORDER_URL%" -H "Authorization: Bearer %TOKEN%"
echo.

echo 9. Testing POST request to /api/orders WITH authentication...
curl -s -o nul -w "Status Code: %%{http_code}\n" -X POST "%ORDER_URL%" -H "Content-Type: application/json" -H "Authorization: Bearer %TOKEN%" -d "{\"order\":[{\"name\":\"Test Item\",\"price\":10.99,\"category\":\"Test\",\"modifiers\":[]}],\"total\":10.99}"
echo.

echo === Manual Testing Complete ===