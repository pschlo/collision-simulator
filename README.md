# Kollisionsimulator 2000

### Builden

Das Programm wurde mit [pyinstaller](https://pyinstaller.org/en/stable/index.html) zu einem eigenständig laufenden Ordner verpackt:

```
pyinstaller --name kollisionsimulator-2000 --add-data 'src/kollisionsimulator-2000/resources:kollisionsimulator-2000/resources' --noconsole src/launch.py
```

Anschließend wurde der Inhalt des von pyinstaller generierten `dist/kollisionsimulator-2000`-Ordners mit WinRAR zum einer `.exe`-Datei (einem SFX archive) verpackt.
