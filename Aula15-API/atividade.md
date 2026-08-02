
## Inserção de livros

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros `
-Method POST `
-ContentType "application/json" `
-Body '{"titulo":"Dom Casmurro","autor":"Machado de Assis","ano":1899}'
```

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros `
-Method POST `
-ContentType "application/json" `
-Body '{"titulo":"O Hobbit","autor":"J. R. R. Tolkien","ano":1937}'
```

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros `
-Method POST `
-ContentType "application/json" `
-Body '{"titulo":"1984","autor":"George Orwell","ano":1949}'
```

## Atualização

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros/1 `
-Method PUT `
-ContentType "application/json" `
-Body '{"titulo":"Cotemig","autor":"3A1","ano":2026}'
```


## Consulta

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros
```

## Exclusão

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros/1 -Method DELETE
Invoke-RestMethod http://127.0.0.1:5000/api/livros/2 -Method DELETE
Invoke-RestMethod http://127.0.0.1:5000/api/livros/3 -Method DELETE
```

## Consulta Final

```powershell
Invoke-RestMethod http://127.0.0.1:5000/api/livros
```