# InformatiCup-2020 Handbuch

Im Folgenden wird beschrieben, wie die Lösung verwendet werden kann. Die Applikation besteht aus mehreren Teilen und kann auf verschiedene Weisen benutzt werden. 

## Setup
Zum Ausführen der Lösung muss Docker installiert sein. Alle Container müssen auf Linux basierend sein. 

## Automatischer Spielmodus

1. Starten Sie im Deployment Package Ordner die automatic_solution.bat. Ein Dockercontainer wird hochgefahren, auf dem eine Python API gestartet wird.  
2. Warten Sie auf die Beendigung aller Schritte 
3. Anschließend kann die game.exe gestartet werden, um Spiele an die Python API zu schicken und Aktionen als Antwort zu erhalten. Die API nutzt den Standard Port der game.exe (50123), Anpassungen in der Ziel-URL sollten nicht notwendig sein

## Manueller Spielmodus

1. Starten Sie im Deployment Package Ordner die manual_solution.bat 
2. Es sollten sich drei Fenster öffnen. Warten Sie, bis in allen Fenstern alle Schritte durchlaufen wurden 
3. Öffnen Sie einen Browser und navigieren zu „localhost:4200“ 
4. Drücken Sie links „Manual“ und anschließend „Start Game“ 
5. Starten Sie die game.exe mit den folgenden flags:  a. „-t 0“ b. „-u „http://192.168.0.192:8000/game““  Die zu übergebende IP-Adresse könnte abweichen, sie sollte Ihnen in einem der drei Fenster mitgeteilt werden.  
6. Nach Spielende können Sie den Vorgang mit dem „Neustart“-Button wiederholen. Beginnen Sie dann wieder mit Schritt 4 

## Automatischer Spielmodus mit Visualisierung 
1. Starten sie die automatic_solution.bat wie in „Automatischer Spielmodus“ (OHNE SCHRITT 3) 
2. Befolgen Sie dieselben Schritte wie in „Manueller Spielmodus“, außer dass Sie in Schritt 4 im Frontend „Automatic“ anstatt „Manual“ wählen 

## Troubleshooting

Falls Probleme auftreten, sollten folgende Dinge überprüft werden:

### Port/IP-Adresse Probleme bei Manuellem oder automatischem Spielmodus mit Visualisierung
In der Datei „./Deployment Package/ManualSolution/manual_solution/src/app/services/api.service.ts“ in der Zeile 13 sollte als serverUrl die lokale IP Adresse stehen. Falls nicht ist die dort stehende IP zu ersetzen im Format: http://192.168.0.192:8000 

### Port Probleme bei automatischem Spielmodus
Sollte der Port 50123 belegt sein, muss dieser in der GameAPI („Deployment Package/Automatic-Solution/api.py“ in Zeile 72) angepasst werden. Außerdem muss die game.exe mit selbigem Port als Ziel-URL gestartet werden 
 
