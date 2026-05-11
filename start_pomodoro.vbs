' 番茄钟启动脚本 - 无黑窗口启动
Dim shell, fso, scriptPath, pythonPath
Set shell = CreateObject("WScript.Shell")
Set fso = CreateObject("Scripting.FileSystemObject")

scriptPath = fso.GetParentFolderName(WScript.ScriptFullName) & "\pomodoro.py"

' 按优先级尝试不同的 Python 路径
pythonPath = ""

If fso.FileExists("C:\Users\Ningzz\AppData\Local\Programs\Python\Python312\pythonw.exe") Then
    pythonPath = "C:\Users\Ningzz\AppData\Local\Programs\Python\Python312\pythonw.exe"
ElseIf fso.FileExists("C:\Users\Ningzz\AppData\Local\Programs\Python\Python312\python.exe") Then
    pythonPath = "C:\Users\Ningzz\AppData\Local\Programs\Python\Python312\python.exe"
End If

If pythonPath <> "" Then
    shell.Run """" & pythonPath & """ """ & scriptPath & """", 0, False
End If

Set fso = Nothing
Set shell = Nothing
