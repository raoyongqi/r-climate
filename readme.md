pip freeze | ForEach-Object { $_.split('=')[0] } | Out-File -FilePath requirements.txt -Encoding utf8