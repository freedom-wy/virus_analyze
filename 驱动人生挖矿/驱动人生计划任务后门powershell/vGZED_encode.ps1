Write-Host $(New-Object IO.StreamReader ($(New-Object IO.Compression.DeflateStream ($(New-Object IO.MemoryStream (,$([Convert]::FromBase64String('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')))), [IO.Compression.CompressionMode]::Decompress)), [Text.Encoding]::ASCII)).ReadToEnd();