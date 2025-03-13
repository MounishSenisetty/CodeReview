const vscode = require('vscode');
const fetch = require('node-fetch');

async function analyzeCode() {
    const editor = vscode.window.activeTextEditor;
    if (!editor) {
        vscode.window.showErrorMessage("No active editor found!");
        return;
    }

    const code = editor.document.getText();
    try {
        const response = await fetch('http://localhost:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });

        const data = await response.json();
        const analysisText = data.report;

        if (!analysisText) {
            throw new Error("Invalid response format from server");
        }

        vscode.window.showInformationMessage("Analysis of the code complete.");

        const doc = await vscode.workspace.openTextDocument({
            content: analysisText,
            language: 'markdown'
        });
        
        await vscode.window.showTextDocument(doc, {
            viewColumn: vscode.ViewColumn.Beside,
            preview: true
        });
        
        await vscode.commands.executeCommand('markdown.showPreview', doc.uri);
    } catch (error) {
        vscode.window.showErrorMessage("Error analyzing code: " + error.message);
    }
}

function activate(context) {
    let disposable = vscode.commands.registerCommand('Finderrors', analyzeCode);
    context.subscriptions.push(disposable);
}

function deactivate() {}

module.exports = {
    activate,
    deactivate
};
